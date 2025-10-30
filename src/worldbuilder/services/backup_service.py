"""Backup and Restore service for WorldBuilder databases."""
import os
import shutil
import zipfile
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import sqlite3


class BackupService:
    """Service for creating and managing database backups."""
    
    def __init__(self, db_path: str, backup_dir: str = None):
        """Initialize backup service.
        
        Args:
            db_path: Path to the main database file
            backup_dir: Directory to store backups. If None, uses ~/.worldbuilder/backups
        """
        self.db_path = db_path
        
        if backup_dir:
            self.backup_dir = Path(backup_dir)
        else:
            self.backup_dir = Path.home() / '.worldbuilder' / 'backups'
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration file for backup settings
        self.config_file = self.backup_dir / 'backup_config.json'
        self._load_config()
    
    def _load_config(self):
        """Load backup configuration."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            # Default configuration
            self.config = {
                "auto_backup_enabled": False,
                "backup_frequency_days": 7,
                "max_backups": 10,
                "last_backup": None
            }
            self._save_config()
    
    def _save_config(self):
        """Save backup configuration."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def create_backup(self, description: str = None, compress: bool = True) -> Dict[str, Any]:
        """Create a backup of the database.
        
        Args:
            description: Optional description for the backup
            compress: Whether to compress the backup into a ZIP file
        
        Returns:
            Dictionary with backup information
        
        Raises:
            ValueError: If database file doesn't exist
        """
        if not os.path.exists(self.db_path):
            raise ValueError(f"Database file not found: {self.db_path}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        
        # Create backup directory for this backup
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        # Copy database file
        db_filename = Path(self.db_path).name
        backup_db_path = backup_path / db_filename
        shutil.copy2(self.db_path, backup_db_path)
        
        # Create metadata file
        metadata = {
            "backup_name": backup_name,
            "timestamp": datetime.now().isoformat(),
            "description": description or "Manual backup",
            "original_db_path": str(self.db_path),
            "db_size_bytes": os.path.getsize(self.db_path),
            "compressed": compress
        }
        
        metadata_path = backup_path / "backup_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Compress if requested
        if compress:
            zip_path = self.backup_dir / f"{backup_name}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(backup_db_path, db_filename)
                zipf.write(metadata_path, "backup_metadata.json")
            
            # Remove uncompressed directory
            shutil.rmtree(backup_path)
            
            metadata["backup_file"] = str(zip_path)
            metadata["backup_size_bytes"] = os.path.getsize(zip_path)
        else:
            metadata["backup_directory"] = str(backup_path)
            metadata["backup_size_bytes"] = os.path.getsize(backup_db_path)
        
        # Update config
        self.config["last_backup"] = datetime.now().isoformat()
        self._save_config()
        
        # Clean up old backups if exceeding max
        self._cleanup_old_backups()
        
        return metadata
    
    def restore_backup(self, backup_identifier: str, target_path: str = None) -> Dict[str, Any]:
        """Restore a backup.
        
        Args:
            backup_identifier: Name or path of the backup to restore
            target_path: Where to restore the database. If None, restores to original location
        
        Returns:
            Dictionary with restore information
        
        Raises:
            ValueError: If backup not found or invalid
        """
        # Find backup
        backup_path = None
        
        # Check if it's a direct path
        if os.path.exists(backup_identifier):
            backup_path = Path(backup_identifier)
        else:
            # Look in backup directory
            possible_zip = self.backup_dir / f"{backup_identifier}.zip"
            possible_dir = self.backup_dir / backup_identifier
            
            if possible_zip.exists():
                backup_path = possible_zip
            elif possible_dir.exists():
                backup_path = possible_dir
        
        if not backup_path:
            raise ValueError(f"Backup not found: {backup_identifier}")
        
        # Determine target
        if not target_path:
            target_path = self.db_path
        
        # Create backup of current database before restoring
        if os.path.exists(target_path):
            current_backup = self.create_backup(
                description="Pre-restore backup",
                compress=True
            )
        
        # Extract and restore
        if backup_path.suffix == '.zip':
            # Extract from ZIP
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Read metadata
                with zipf.open('backup_metadata.json') as f:
                    metadata = json.load(f)
                
                # Extract database file
                db_files = [name for name in zipf.namelist() if name.endswith('.db')]
                if not db_files:
                    raise ValueError("No database file found in backup")
                
                db_filename = db_files[0]
                zipf.extract(db_filename, self.backup_dir / 'temp')
                
                # Copy to target
                temp_db_path = self.backup_dir / 'temp' / db_filename
                shutil.copy2(temp_db_path, target_path)
                
                # Clean up temp
                shutil.rmtree(self.backup_dir / 'temp')
        else:
            # Copy from directory
            metadata_path = backup_path / "backup_metadata.json"
            if not metadata_path.exists():
                raise ValueError("Invalid backup: metadata not found")
            
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            # Find database file
            db_files = list(backup_path.glob('*.db'))
            if not db_files:
                raise ValueError("No database file found in backup")
            
            shutil.copy2(db_files[0], target_path)
        
        result = {
            "restored_from": str(backup_path),
            "restored_to": target_path,
            "backup_timestamp": metadata.get("timestamp"),
            "restore_timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups.
        
        Returns:
            List of backup information dictionaries
        """
        backups = []
        
        # Find ZIP files
        for zip_file in self.backup_dir.glob('backup_*.zip'):
            try:
                with zipfile.ZipFile(zip_file, 'r') as zipf:
                    with zipf.open('backup_metadata.json') as f:
                        metadata = json.load(f)
                        metadata["backup_file"] = str(zip_file)
                        backups.append(metadata)
            except Exception:
                # Skip invalid backups
                continue
        
        # Find backup directories
        for backup_dir in self.backup_dir.glob('backup_*'):
            if backup_dir.is_dir():
                metadata_file = backup_dir / 'backup_metadata.json'
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            metadata["backup_directory"] = str(backup_dir)
                            backups.append(metadata)
                    except Exception:
                        continue
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return backups
    
    def delete_backup(self, backup_identifier: str) -> bool:
        """Delete a backup.
        
        Args:
            backup_identifier: Name or path of backup to delete
        
        Returns:
            True if deleted successfully
        """
        # Find backup
        backup_path = None
        
        if os.path.exists(backup_identifier):
            backup_path = Path(backup_identifier)
        else:
            possible_zip = self.backup_dir / f"{backup_identifier}.zip"
            possible_dir = self.backup_dir / backup_identifier
            
            if possible_zip.exists():
                backup_path = possible_zip
            elif possible_dir.exists():
                backup_path = possible_dir
        
        if not backup_path:
            return False
        
        # Delete
        if backup_path.is_file():
            os.remove(backup_path)
        else:
            shutil.rmtree(backup_path)
        
        return True
    
    def _cleanup_old_backups(self):
        """Remove old backups exceeding max_backups limit."""
        max_backups = self.config.get("max_backups", 10)
        backups = self.list_backups()
        
        if len(backups) > max_backups:
            # Delete oldest backups
            backups_to_delete = backups[max_backups:]
            for backup in backups_to_delete:
                identifier = backup.get("backup_file") or backup.get("backup_directory")
                if identifier:
                    self.delete_backup(identifier)
    
    def should_auto_backup(self) -> bool:
        """Check if an automatic backup should be performed.
        
        Returns:
            True if auto-backup is due
        """
        if not self.config.get("auto_backup_enabled", False):
            return False
        
        last_backup = self.config.get("last_backup")
        if not last_backup:
            return True
        
        frequency_days = self.config.get("backup_frequency_days", 7)
        last_backup_date = datetime.fromisoformat(last_backup)
        days_since_backup = (datetime.now() - last_backup_date).days
        
        return days_since_backup >= frequency_days
    
    def configure_auto_backup(self, enabled: bool, frequency_days: int = 7, max_backups: int = 10):
        """Configure automatic backup settings.
        
        Args:
            enabled: Enable or disable auto-backup
            frequency_days: Days between automatic backups
            max_backups: Maximum number of backups to keep
        """
        self.config["auto_backup_enabled"] = enabled
        self.config["backup_frequency_days"] = frequency_days
        self.config["max_backups"] = max_backups
        self._save_config()
    
    def get_backup_config(self) -> Dict[str, Any]:
        """Get current backup configuration.
        
        Returns:
            Dictionary with backup configuration
        """
        return self.config.copy()

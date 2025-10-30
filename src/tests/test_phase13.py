"""Tests for Phase 13: Data Management (Export/Import and Backup/Restore)."""
import unittest
import os
import json
import tempfile
import shutil
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from worldbuilder.models import Base, Universe, Location, Species, NotableFigure
from worldbuilder.services.export_import_service import ExportImportService
from worldbuilder.services.backup_service import BackupService


class TestExportImportService(unittest.TestCase):
    """Test export and import functionality."""
    
    def setUp(self):
        """Set up test database and services."""
        # Create in-memory database
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Create test universe with data
        self.universe = Universe(
            name="Test Universe",
            description="A test universe",
            author="Test Author",
            genre="Fantasy",
            is_active=True
        )
        self.session.add(self.universe)
        self.session.flush()
        
        # Add test entities
        self.location = Location(
            universe_id=self.universe.id,
            name="Test City",
            description="A test city",
            location_type="CITY"
        )
        self.session.add(self.location)
        
        self.species = Species(
            universe_id=self.universe.id,
            name="Human",
            description="Test species",
            species_type="SENTIENT"
        )
        self.session.add(self.species)
        
        self.session.flush()
        
        self.figure = NotableFigure(
            universe_id=self.universe.id,
            name="Test Character",
            description="A test character",
            species_id=self.species.id
        )
        self.session.add(self.figure)
        self.session.commit()
        
        # Create service
        self.service = ExportImportService(self.session)
        
        # Create temp directory for exports
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test resources."""
        self.session.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_export_full_universe(self):
        """Test exporting a complete universe."""
        output_path = os.path.join(self.temp_dir, "test_export.json")
        
        stats = self.service.export_universe(
            universe_id=self.universe.id,
            output_path=output_path,
            selective=False
        )
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
        
        # Verify stats
        self.assertGreater(stats["total_entities"], 0)
        self.assertEqual(stats["output_file"], output_path)
        
        # Verify file content
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIn("export_metadata", data)
        self.assertIn("universe", data)
        self.assertIn("data", data)
        
        # Check universe data
        self.assertEqual(data["universe"]["name"], "Test Universe")
        
        # Check entities
        self.assertIn("locations", data["data"])
        self.assertIn("species", data["data"])
        self.assertIn("figures", data["data"])
        
        self.assertEqual(len(data["data"]["locations"]), 1)
        self.assertEqual(len(data["data"]["species"]), 1)
        self.assertEqual(len(data["data"]["figures"]), 1)
    
    def test_export_selective_entities(self):
        """Test selective export of specific entity types."""
        output_path = os.path.join(self.temp_dir, "test_selective_export.json")
        
        stats = self.service.export_universe(
            universe_id=self.universe.id,
            output_path=output_path,
            selective=True,
            entity_types=['locations', 'species']
        )
        
        # Verify file content
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Should have locations and species, but not figures
        self.assertIn("locations", data["data"])
        self.assertIn("species", data["data"])
        self.assertNotIn("figures", data["data"])
    
    def test_import_creates_new_universe(self):
        """Test importing data creates a new universe."""
        # First, export the universe
        export_path = os.path.join(self.temp_dir, "test_export.json")
        self.service.export_universe(
            universe_id=self.universe.id,
            output_path=export_path
        )
        
        # Import into new universe
        stats = self.service.import_universe(
            input_path=export_path,
            create_new=True
        )
        
        # Verify new universe was created
        self.assertIn("new_universe_id", stats)
        self.assertGreater(stats["total_entities"], 0)
        
        # Verify we now have 2 universes
        universes = self.session.query(Universe).all()
        self.assertEqual(len(universes), 2)
    
    def test_export_nonexistent_universe(self):
        """Test exporting a non-existent universe raises error."""
        output_path = os.path.join(self.temp_dir, "test_export.json")
        
        with self.assertRaises(ValueError):
            self.service.export_universe(
                universe_id=99999,
                output_path=output_path
            )
    
    def test_import_invalid_file(self):
        """Test importing an invalid file raises error."""
        invalid_path = os.path.join(self.temp_dir, "invalid.json")
        
        with self.assertRaises(ValueError):
            self.service.import_universe(invalid_path)


class TestBackupService(unittest.TestCase):
    """Test backup and restore functionality."""
    
    def setUp(self):
        """Set up test database and backup service."""
        # Create temp directory for test database and backups
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.backup_dir = os.path.join(self.temp_dir, "backups")
        
        # Create a test database
        engine = create_engine(f"sqlite:///{self.db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Add some data
        universe = Universe(
            name="Test Universe",
            description="Test",
            is_active=True
        )
        session.add(universe)
        session.commit()
        session.close()
        
        # Create backup service
        self.service = BackupService(self.db_path, self.backup_dir)
    
    def tearDown(self):
        """Clean up test resources."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_compressed_backup(self):
        """Test creating a compressed backup."""
        result = self.service.create_backup(
            description="Test backup",
            compress=True
        )
        
        # Verify backup was created
        self.assertIn("backup_file", result)
        self.assertTrue(os.path.exists(result["backup_file"]))
        self.assertTrue(result["backup_file"].endswith(".zip"))
        
        # Verify metadata
        self.assertEqual(result["description"], "Test backup")
        self.assertTrue(result["compressed"])
    
    def test_create_uncompressed_backup(self):
        """Test creating an uncompressed backup."""
        result = self.service.create_backup(
            description="Test backup",
            compress=False
        )
        
        # Verify backup directory was created
        self.assertIn("backup_directory", result)
        self.assertTrue(os.path.exists(result["backup_directory"]))
        self.assertFalse(result["compressed"])
    
    def test_list_backups(self):
        """Test listing available backups."""
        # Create a few backups
        self.service.create_backup(description="Backup 1", compress=True)
        self.service.create_backup(description="Backup 2", compress=False)
        
        # List backups
        backups = self.service.list_backups()
        
        # Verify we have 2 backups
        self.assertEqual(len(backups), 2)
        
        # Verify backups are sorted by timestamp (newest first)
        self.assertGreater(backups[0]["timestamp"], backups[1]["timestamp"])
    
    def test_delete_backup(self):
        """Test deleting a backup."""
        # Create a backup
        result = self.service.create_backup(description="Test", compress=True)
        backup_name = result["backup_name"]
        
        # Delete it
        success = self.service.delete_backup(backup_name)
        self.assertTrue(success)
        
        # Verify it's gone
        backups = self.service.list_backups()
        self.assertEqual(len(backups), 0)
    
    def test_restore_backup(self):
        """Test restoring a backup."""
        # Create a backup
        result = self.service.create_backup(description="Test", compress=True)
        backup_name = result["backup_name"]
        
        # Modify the database
        engine = create_engine(f"sqlite:///{self.db_path}")
        Session = sessionmaker(bind=engine)
        session = Session()
        universe = session.query(Universe).first()
        universe.name = "Modified Universe"
        session.commit()
        session.close()
        
        # Restore the backup
        restore_path = os.path.join(self.temp_dir, "restored.db")
        restore_result = self.service.restore_backup(backup_name, restore_path)
        
        # Verify restoration
        self.assertEqual(restore_result["restored_to"], restore_path)
        self.assertTrue(os.path.exists(restore_path))
        
        # Verify the restored database has original data
        engine = create_engine(f"sqlite:///{restore_path}")
        Session = sessionmaker(bind=engine)
        session = Session()
        universe = session.query(Universe).first()
        self.assertEqual(universe.name, "Test Universe")
        session.close()
    
    def test_configure_auto_backup(self):
        """Test configuring automatic backup settings."""
        self.service.configure_auto_backup(
            enabled=True,
            frequency_days=5,
            max_backups=15
        )
        
        config = self.service.get_backup_config()
        
        self.assertTrue(config["auto_backup_enabled"])
        self.assertEqual(config["backup_frequency_days"], 5)
        self.assertEqual(config["max_backups"], 15)
    
    def test_should_auto_backup(self):
        """Test auto-backup checking logic."""
        # Initially, should not auto-backup (disabled)
        self.assertFalse(self.service.should_auto_backup())
        
        # Enable auto-backup
        self.service.configure_auto_backup(enabled=True, frequency_days=7)
        
        # Should backup (no previous backup)
        self.assertTrue(self.service.should_auto_backup())
        
        # Create a backup
        self.service.create_backup(description="Test")
        
        # Should not backup (just backed up)
        self.assertFalse(self.service.should_auto_backup())
    
    def test_cleanup_old_backups(self):
        """Test automatic cleanup of old backups."""
        # Set max backups to 3
        self.service.configure_auto_backup(enabled=True, frequency_days=1, max_backups=3)
        
        # Create 5 backups
        for i in range(5):
            self.service.create_backup(description=f"Backup {i}")
        
        # Should only have 3 backups (cleanup happens after each creation)
        backups = self.service.list_backups()
        self.assertLessEqual(len(backups), 3)


def run_tests():
    """Run all Phase 13 tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestExportImportService))
    suite.addTests(loader.loadTestsFromTestCase(TestBackupService))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

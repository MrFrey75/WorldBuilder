"""Dialog for backup and restore operations."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QFileDialog,
                             QCheckBox, QGroupBox, QProgressBar, QTextEdit,
                             QTabWidget, QWidget, QListWidget, QMessageBox,
                             QSpinBox, QListWidgetItem)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime
from pathlib import Path


class BackupDialog(QDialog):
    """Dialog for creating and managing backups."""
    
    backup_created = pyqtSignal(dict)  # Emits backup info
    
    def __init__(self, parent=None, backup_service=None):
        """Initialize the backup dialog.
        
        Args:
            parent: Parent widget
            backup_service: BackupService instance
        """
        super().__init__(parent)
        self.backup_service = backup_service
        
        self.setWindowTitle("Backup & Restore")
        self.setModal(True)
        self.setMinimumWidth(700)
        self.setMinimumHeight(600)
        
        self._setup_ui()
        self._load_backups()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Tabs for different operations
        tabs = QTabWidget()
        
        # Create Backup tab
        create_tab = self._create_backup_tab()
        tabs.addTab(create_tab, "Create Backup")
        
        # Manage Backups tab
        manage_tab = self._create_manage_tab()
        tabs.addTab(manage_tab, "Manage Backups")
        
        # Settings tab
        settings_tab = self._create_settings_tab()
        tabs.addTab(settings_tab, "Settings")
        
        layout.addWidget(tabs)
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def _create_backup_tab(self):
        """Create the backup creation tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Description
        desc_label = QLabel("Create a backup of your current database.")
        layout.addWidget(desc_label)
        
        # Backup options
        options_group = QGroupBox("Backup Options")
        options_layout = QFormLayout()
        
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Optional description for this backup")
        options_layout.addRow("Description:", self.description_edit)
        
        self.compress_checkbox = QCheckBox("Compress backup (ZIP)")
        self.compress_checkbox.setChecked(True)
        options_layout.addRow("", self.compress_checkbox)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Backup location info
        if self.backup_service:
            location_label = QLabel(f"Backups are stored in:\n{self.backup_service.backup_dir}")
            location_label.setStyleSheet("color: gray; font-size: 10px;")
            location_label.setWordWrap(True)
            layout.addWidget(location_label)
        
        # Progress and status
        self.create_progress_bar = QProgressBar()
        self.create_progress_bar.setVisible(False)
        layout.addWidget(self.create_progress_bar)
        
        self.create_status_label = QLabel("")
        self.create_status_label.setWordWrap(True)
        layout.addWidget(self.create_status_label)
        
        layout.addStretch()
        
        # Create backup button
        create_btn = QPushButton("Create Backup Now")
        create_btn.clicked.connect(self._create_backup)
        layout.addWidget(create_btn)
        
        return widget
    
    def _create_manage_tab(self):
        """Create the manage backups tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Backups list
        list_label = QLabel("Available Backups:")
        layout.addWidget(list_label)
        
        self.backups_list = QListWidget()
        self.backups_list.itemSelectionChanged.connect(self._on_backup_selected)
        layout.addWidget(self.backups_list)
        
        # Backup details
        self.details_group = QGroupBox("Backup Details")
        details_layout = QFormLayout()
        
        self.detail_name_label = QLabel("")
        details_layout.addRow("Name:", self.detail_name_label)
        
        self.detail_date_label = QLabel("")
        details_layout.addRow("Date:", self.detail_date_label)
        
        self.detail_size_label = QLabel("")
        details_layout.addRow("Size:", self.detail_size_label)
        
        self.detail_desc_label = QLabel("")
        self.detail_desc_label.setWordWrap(True)
        details_layout.addRow("Description:", self.detail_desc_label)
        
        self.details_group.setLayout(details_layout)
        self.details_group.setVisible(False)
        layout.addWidget(self.details_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.restore_btn = QPushButton("Restore Selected")
        self.restore_btn.clicked.connect(self._restore_backup)
        self.restore_btn.setEnabled(False)
        button_layout.addWidget(self.restore_btn)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self._delete_backup)
        self.delete_btn.setEnabled(False)
        button_layout.addWidget(self.delete_btn)
        
        button_layout.addStretch()
        
        refresh_btn = QPushButton("Refresh List")
        refresh_btn.clicked.connect(self._load_backups)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        return widget
    
    def _create_settings_tab(self):
        """Create the settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Auto-backup settings
        auto_backup_group = QGroupBox("Automatic Backup")
        auto_layout = QFormLayout()
        
        self.auto_backup_checkbox = QCheckBox("Enable automatic backups")
        if self.backup_service:
            config = self.backup_service.get_backup_config()
            self.auto_backup_checkbox.setChecked(config.get("auto_backup_enabled", False))
        auto_layout.addRow("", self.auto_backup_checkbox)
        
        self.frequency_spinbox = QSpinBox()
        self.frequency_spinbox.setRange(1, 30)
        self.frequency_spinbox.setValue(7)
        self.frequency_spinbox.setSuffix(" days")
        if self.backup_service:
            config = self.backup_service.get_backup_config()
            self.frequency_spinbox.setValue(config.get("backup_frequency_days", 7))
        auto_layout.addRow("Backup Frequency:", self.frequency_spinbox)
        
        self.max_backups_spinbox = QSpinBox()
        self.max_backups_spinbox.setRange(1, 50)
        self.max_backups_spinbox.setValue(10)
        if self.backup_service:
            config = self.backup_service.get_backup_config()
            self.max_backups_spinbox.setValue(config.get("max_backups", 10))
        auto_layout.addRow("Max Backups to Keep:", self.max_backups_spinbox)
        
        auto_backup_group.setLayout(auto_layout)
        layout.addWidget(auto_backup_group)
        
        # Last backup info
        if self.backup_service:
            config = self.backup_service.get_backup_config()
            last_backup = config.get("last_backup")
            if last_backup:
                try:
                    last_date = datetime.fromisoformat(last_backup)
                    last_backup_text = last_date.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    last_backup_text = "Unknown"
            else:
                last_backup_text = "Never"
            
            info_label = QLabel(f"Last backup: {last_backup_text}")
            info_label.setStyleSheet("color: gray; font-size: 10px;")
            layout.addWidget(info_label)
        
        layout.addStretch()
        
        # Save settings button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self._save_settings)
        layout.addWidget(save_btn)
        
        return widget
    
    def _create_backup(self):
        """Create a new backup."""
        if not self.backup_service:
            QMessageBox.warning(self, "Error", "Backup service not available")
            return
        
        try:
            self.create_progress_bar.setVisible(True)
            self.create_progress_bar.setRange(0, 0)  # Indeterminate
            
            description = self.description_edit.text() or "Manual backup"
            compress = self.compress_checkbox.isChecked()
            
            result = self.backup_service.create_backup(
                description=description,
                compress=compress
            )
            
            self.create_progress_bar.setVisible(False)
            
            size_mb = result.get("backup_size_bytes", 0) / (1024 * 1024)
            self.create_status_label.setText(
                f"✓ Backup created successfully!\n"
                f"Size: {size_mb:.2f} MB\n"
                f"Location: {result.get('backup_file', result.get('backup_directory', 'Unknown'))}"
            )
            self.create_status_label.setStyleSheet("color: green;")
            
            self.description_edit.clear()
            self._load_backups()
            self.backup_created.emit(result)
            
        except Exception as e:
            self.create_progress_bar.setVisible(False)
            self.create_status_label.setText(f"✗ Error creating backup: {str(e)}")
            self.create_status_label.setStyleSheet("color: red;")
    
    def _load_backups(self):
        """Load and display available backups."""
        if not self.backup_service:
            return
        
        self.backups_list.clear()
        self.current_backups = self.backup_service.list_backups()
        
        for backup in self.current_backups:
            name = backup.get("backup_name", "Unknown")
            timestamp = backup.get("timestamp", "")
            
            try:
                date = datetime.fromisoformat(timestamp)
                date_str = date.strftime("%Y-%m-%d %H:%M")
            except:
                date_str = "Unknown date"
            
            size_bytes = backup.get("backup_size_bytes", 0)
            size_mb = size_bytes / (1024 * 1024)
            
            item_text = f"{name} - {date_str} ({size_mb:.1f} MB)"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, backup)
            self.backups_list.addItem(item)
    
    def _on_backup_selected(self):
        """Handle backup selection."""
        selected_items = self.backups_list.selectedItems()
        
        if selected_items:
            backup = selected_items[0].data(Qt.ItemDataRole.UserRole)
            
            self.detail_name_label.setText(backup.get("backup_name", "Unknown"))
            
            timestamp = backup.get("timestamp", "")
            try:
                date = datetime.fromisoformat(timestamp)
                self.detail_date_label.setText(date.strftime("%Y-%m-%d %H:%M:%S"))
            except:
                self.detail_date_label.setText("Unknown")
            
            size_bytes = backup.get("backup_size_bytes", 0)
            size_mb = size_bytes / (1024 * 1024)
            self.detail_size_label.setText(f"{size_mb:.2f} MB")
            
            self.detail_desc_label.setText(backup.get("description", "No description"))
            
            self.details_group.setVisible(True)
            self.restore_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        else:
            self.details_group.setVisible(False)
            self.restore_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
    
    def _restore_backup(self):
        """Restore the selected backup."""
        selected_items = self.backups_list.selectedItems()
        if not selected_items or not self.backup_service:
            return
        
        backup = selected_items[0].data(Qt.ItemDataRole.UserRole)
        backup_name = backup.get("backup_name", "Unknown")
        
        # Confirm
        reply = QMessageBox.question(
            self,
            "Confirm Restore",
            f"Are you sure you want to restore backup '{backup_name}'?\n\n"
            "This will replace your current database. A backup of the current "
            "state will be created automatically.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                backup_file = backup.get("backup_file") or backup.get("backup_directory")
                result = self.backup_service.restore_backup(backup_name)
                
                QMessageBox.information(
                    self,
                    "Restore Complete",
                    f"Backup restored successfully!\n\n"
                    f"The application will need to be restarted to use the restored database."
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Restore Failed",
                    f"Error restoring backup: {str(e)}"
                )
    
    def _delete_backup(self):
        """Delete the selected backup."""
        selected_items = self.backups_list.selectedItems()
        if not selected_items or not self.backup_service:
            return
        
        backup = selected_items[0].data(Qt.ItemDataRole.UserRole)
        backup_name = backup.get("backup_name", "Unknown")
        
        # Confirm
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete backup '{backup_name}'?\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                backup_file = backup.get("backup_file") or backup.get("backup_directory")
                self.backup_service.delete_backup(backup_name)
                self._load_backups()
                
                QMessageBox.information(self, "Deleted", "Backup deleted successfully")
                
            except Exception as e:
                QMessageBox.critical(self, "Delete Failed", f"Error deleting backup: {str(e)}")
    
    def _save_settings(self):
        """Save backup settings."""
        if not self.backup_service:
            return
        
        try:
            self.backup_service.configure_auto_backup(
                enabled=self.auto_backup_checkbox.isChecked(),
                frequency_days=self.frequency_spinbox.value(),
                max_backups=self.max_backups_spinbox.value()
            )
            
            QMessageBox.information(self, "Settings Saved", "Backup settings saved successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", f"Error saving settings: {str(e)}")

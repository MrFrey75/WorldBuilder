"""Dialog for exporting and importing universe data."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel, QFileDialog,
                             QCheckBox, QGroupBox, QProgressBar, QTextEdit,
                             QTabWidget, QWidget, QListWidget, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from pathlib import Path
import json


class ExportDialog(QDialog):
    """Dialog for exporting universe data."""
    
    def __init__(self, parent=None, universe_name: str = "Universe"):
        """Initialize the export dialog.
        
        Args:
            parent: Parent widget
            universe_name: Name of the universe being exported
        """
        super().__init__(parent)
        self.universe_name = universe_name
        self.selected_entity_types = []
        
        self.setWindowTitle(f"Export {universe_name}")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Export type group
        export_type_group = QGroupBox("Export Type")
        export_type_layout = QVBoxLayout()
        
        self.full_export_radio = QCheckBox("Full Export (All Entities)")
        self.full_export_radio.setChecked(True)
        self.full_export_radio.toggled.connect(self._on_export_type_changed)
        export_type_layout.addWidget(self.full_export_radio)
        
        self.selective_export_radio = QCheckBox("Selective Export")
        self.selective_export_radio.toggled.connect(self._on_export_type_changed)
        export_type_layout.addWidget(self.selective_export_radio)
        
        export_type_group.setLayout(export_type_layout)
        layout.addWidget(export_type_group)
        
        # Entity selection group (disabled by default)
        self.entity_selection_group = QGroupBox("Select Entity Types to Export")
        entity_layout = QVBoxLayout()
        
        self.checkboxes = {}
        entity_types = [
            ("locations", "Locations"),
            ("species", "Species"),
            ("figures", "Notable Figures"),
            ("relationships", "Relationships"),
            ("events", "Events"),
            ("organizations", "Organizations"),
            ("artifacts", "Artifacts"),
            ("lore", "Lore & Mythology")
        ]
        
        for key, label in entity_types:
            checkbox = QCheckBox(label)
            checkbox.setChecked(True)
            self.checkboxes[key] = checkbox
            entity_layout.addWidget(checkbox)
        
        self.entity_selection_group.setLayout(entity_layout)
        self.entity_selection_group.setEnabled(False)
        layout.addWidget(self.entity_selection_group)
        
        # Output file selection
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Output File:"))
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Select export file location...")
        file_layout.addWidget(self.file_path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_output_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        # Button box
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.export_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _on_export_type_changed(self):
        """Handle export type radio button change."""
        is_selective = self.selective_export_radio.isChecked()
        self.entity_selection_group.setEnabled(is_selective)
    
    def _browse_output_file(self):
        """Open file browser for output file selection."""
        default_name = f"{self.universe_name.replace(' ', '_')}_export.json"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Universe Data",
            default_name,
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.file_path_edit.setText(file_path)
    
    def get_export_settings(self):
        """Get the export settings from the dialog.
        
        Returns:
            Dictionary with export settings
        """
        is_selective = self.selective_export_radio.isChecked()
        selected_types = []
        
        if is_selective:
            for key, checkbox in self.checkboxes.items():
                if checkbox.isChecked():
                    selected_types.append(key)
        
        return {
            "output_path": self.file_path_edit.text(),
            "selective": is_selective,
            "entity_types": selected_types if is_selective else None
        }


class ImportDialog(QDialog):
    """Dialog for importing universe data."""
    
    def __init__(self, parent=None):
        """Initialize the import dialog."""
        super().__init__(parent)
        
        self.setWindowTitle("Import Universe Data")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # File selection
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Import File:"))
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Select file to import...")
        self.file_path_edit.textChanged.connect(self._on_file_selected)
        file_layout.addWidget(self.file_path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_input_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        # Import preview (shows what will be imported)
        self.preview_group = QGroupBox("Import Preview")
        preview_layout = QVBoxLayout()
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(150)
        preview_layout.addWidget(self.preview_text)
        
        self.preview_group.setLayout(preview_layout)
        self.preview_group.setVisible(False)
        layout.addWidget(self.preview_group)
        
        # Import options
        options_group = QGroupBox("Import Options")
        options_layout = QVBoxLayout()
        
        self.create_new_radio = QCheckBox("Create New Universe")
        self.create_new_radio.setChecked(True)
        self.create_new_radio.toggled.connect(self._on_import_mode_changed)
        options_layout.addWidget(self.create_new_radio)
        
        self.merge_existing_radio = QCheckBox("Merge into Existing Universe (Advanced)")
        self.merge_existing_radio.toggled.connect(self._on_import_mode_changed)
        options_layout.addWidget(self.merge_existing_radio)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Warning label
        warning_label = QLabel("⚠️ Note: Merging into existing universe may create duplicates")
        warning_label.setStyleSheet("color: orange; font-size: 10px;")
        warning_label.setVisible(False)
        self.warning_label = warning_label
        layout.addWidget(warning_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Button box
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.import_btn = QPushButton("Import")
        self.import_btn.clicked.connect(self.accept)
        self.import_btn.setEnabled(False)
        button_layout.addWidget(self.import_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _browse_input_file(self):
        """Open file browser for input file selection."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Import File",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.file_path_edit.setText(file_path)
    
    def _on_file_selected(self, file_path):
        """Handle file selection."""
        if not file_path or not Path(file_path).exists():
            self.import_btn.setEnabled(False)
            self.preview_group.setVisible(False)
            return
        
        # Try to read and preview the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate structure
            if "export_metadata" not in data or "universe" not in data:
                raise ValueError("Invalid import file format")
            
            # Show preview
            metadata = data["export_metadata"]
            universe_data = data["universe"]
            entities_data = data.get("data", {})
            
            preview_text = f"Universe: {universe_data.get('name', 'Unknown')}\n"
            preview_text += f"Export Date: {metadata.get('export_date', 'Unknown')}\n"
            preview_text += f"Export Version: {metadata.get('version', 'Unknown')}\n\n"
            preview_text += "Entities to Import:\n"
            
            for entity_type, entities in entities_data.items():
                preview_text += f"  - {entity_type.title()}: {len(entities)} items\n"
            
            self.preview_text.setPlainText(preview_text)
            self.preview_group.setVisible(True)
            self.import_btn.setEnabled(True)
            
        except Exception as e:
            self.status_label.setText(f"Error reading file: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            self.import_btn.setEnabled(False)
            self.preview_group.setVisible(False)
    
    def _on_import_mode_changed(self):
        """Handle import mode change."""
        is_merge = self.merge_existing_radio.isChecked()
        self.warning_label.setVisible(is_merge)
    
    def get_import_settings(self):
        """Get the import settings from the dialog.
        
        Returns:
            Dictionary with import settings
        """
        return {
            "input_path": self.file_path_edit.text(),
            "create_new": self.create_new_radio.isChecked()
        }

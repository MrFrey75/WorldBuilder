"""Location dialog for creating and editing locations."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QTextEdit, QPushButton, QLabel, QComboBox, QHBoxLayout)
from PyQt6.QtCore import Qt
from worldbuilder.models.location import Location, LocationType
from typing import List, Optional


class LocationDialog(QDialog):
    """Dialog for creating or editing a location."""
    
    def __init__(self, parent=None, location: Location = None, 
                 available_parents: List[Location] = None, universe_id: int = None):
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
            location: Location to edit (None for create new)
            available_parents: List of potential parent locations
            universe_id: Universe ID (required for create)
        """
        super().__init__(parent)
        self.location = location
        self.available_parents = available_parents or []
        self.universe_id = universe_id
        self.is_edit_mode = location is not None
        
        self.setWindowTitle("Edit Location" if self.is_edit_mode else "Create New Location")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self._setup_ui()
        
        if self.is_edit_mode:
            self._load_location_data()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Name field (required)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter location name (required)")
        form_layout.addRow("Name*:", self.name_edit)
        
        # Location type
        self.type_combo = QComboBox()
        for loc_type in LocationType:
            self.type_combo.addItem(loc_type.value, loc_type)
        form_layout.addRow("Type:", self.type_combo)
        
        # Parent location
        self.parent_combo = QComboBox()
        self.parent_combo.addItem("(None - Root Location)", None)
        for parent_loc in self.available_parents:
            # Don't allow selecting self or descendants as parent
            if self.is_edit_mode and (parent_loc.id == self.location.id or 
                                     self.location.is_ancestor_of(parent_loc)):
                continue
            display_name = f"{parent_loc.get_full_path()} ({parent_loc.location_type.value})"
            self.parent_combo.addItem(display_name, parent_loc.id)
        form_layout.addRow("Parent Location:", self.parent_combo)
        
        # Description field
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Enter location description")
        self.description_edit.setMaximumHeight(150)
        form_layout.addRow("Description:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Required field note
        note_label = QLabel("* Required field")
        note_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(note_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Save" if self.is_edit_mode else "Create")
        self.save_button.clicked.connect(self._on_save)
        self.save_button.setDefault(True)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
    
    def _load_location_data(self):
        """Load location data into form fields."""
        if not self.location:
            return
        
        self.name_edit.setText(self.location.name)
        
        # Set type
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == self.location.location_type:
                self.type_combo.setCurrentIndex(i)
                break
        
        # Set parent
        if self.location.parent_id:
            for i in range(self.parent_combo.count()):
                if self.parent_combo.itemData(i) == self.location.parent_id:
                    self.parent_combo.setCurrentIndex(i)
                    break
        
        if self.location.description:
            self.description_edit.setPlainText(self.location.description)
    
    def _on_save(self):
        """Handle save button click."""
        # Validate name
        name = self.name_edit.text().strip()
        if not name:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Validation Error", "Location name is required.")
            self.name_edit.setFocus()
            return
        
        self.accept()
    
    def get_data(self) -> dict:
        """Get form data as dictionary.
        
        Returns:
            Dictionary with location data
        """
        description = self.description_edit.toPlainText().strip()
        if not description:
            description = None
        
        parent_id = self.parent_combo.currentData()
        
        return {
            "name": self.name_edit.text().strip(),
            "location_type": self.type_combo.currentData(),
            "description": description,
            "parent_id": parent_id,
            "universe_id": self.universe_id if not self.is_edit_mode else None
        }

"""Relationship dialog for creating and editing relationships."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QTextEdit, QPushButton, QLabel, QComboBox, 
                             QCheckBox, QHBoxLayout, QGroupBox)
from PyQt6.QtCore import Qt
from worldbuilder.models.relationship import Relationship, RelationshipType, RelationshipStrength


class RelationshipDialog(QDialog):
    """Dialog for creating or editing a relationship."""
    
    def __init__(self, parent=None, relationship: Relationship = None, universe_id: int = None,
                 source_info: tuple = None, target_info: tuple = None):
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
            relationship: Relationship to edit (None for create new)
            universe_id: Universe ID (required for create)
            source_info: Tuple of (entity_type, entity_id, entity_name) for source
            target_info: Tuple of (entity_type, entity_id, entity_name) for target
        """
        super().__init__(parent)
        self.relationship = relationship
        self.universe_id = universe_id
        self.source_info = source_info
        self.target_info = target_info
        self.is_edit_mode = relationship is not None
        
        self.setWindowTitle("Edit Relationship" if self.is_edit_mode else "Create New Relationship")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self._setup_ui()
        
        if self.is_edit_mode:
            self._load_relationship_data()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Entities Group
        entities_group = QGroupBox("Entities")
        entities_layout = QFormLayout()
        
        # Source entity (read-only in create mode if provided)
        self.source_label = QLabel()
        if self.source_info:
            self.source_label.setText(f"{self.source_info[2]} ({self.source_info[0]})")
        entities_layout.addRow("Source Entity:", self.source_label)
        
        # Target entity (read-only in create mode if provided)
        self.target_label = QLabel()
        if self.target_info:
            self.target_label.setText(f"{self.target_info[2]} ({self.target_info[0]})")
        entities_layout.addRow("Target Entity:", self.target_label)
        
        entities_group.setLayout(entities_layout)
        layout.addWidget(entities_group)
        
        # Relationship Properties Group
        props_group = QGroupBox("Relationship Properties")
        props_layout = QFormLayout()
        
        # Relationship type
        self.type_combo = QComboBox()
        for rel_type in RelationshipType:
            self.type_combo.addItem(rel_type.value, rel_type)
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        props_layout.addRow("Type*:", self.type_combo)
        
        # Custom type name (only shown for CUSTOM type)
        self.custom_name_edit = QLineEdit()
        self.custom_name_edit.setPlaceholderText("Enter custom relationship type")
        self.custom_name_label = QLabel("Custom Name*:")
        props_layout.addRow(self.custom_name_label, self.custom_name_edit)
        self.custom_name_label.setVisible(False)
        self.custom_name_edit.setVisible(False)
        
        # Strength
        self.strength_combo = QComboBox()
        for strength in RelationshipStrength:
            self.strength_combo.addItem(strength.value, strength)
        self.strength_combo.setCurrentIndex(1)  # Default to MODERATE
        props_layout.addRow("Strength:", self.strength_combo)
        
        # Active status
        self.active_check = QCheckBox("Relationship is currently active")
        self.active_check.setChecked(True)
        props_layout.addRow("Status:", self.active_check)
        
        props_group.setLayout(props_layout)
        layout.addWidget(props_group)
        
        # Details Group
        details_group = QGroupBox("Details")
        details_layout = QFormLayout()
        
        # Start date
        self.start_date_edit = QLineEdit()
        self.start_date_edit.setPlaceholderText("e.g., 2020, Summer 1995, Ancient Times")
        details_layout.addRow("Start Date:", self.start_date_edit)
        
        # End date
        self.end_date_edit = QLineEdit()
        self.end_date_edit.setPlaceholderText("e.g., 2023, Winter 2000, Present")
        details_layout.addRow("End Date:", self.end_date_edit)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Additional details about this relationship")
        self.description_edit.setMaximumHeight(100)
        details_layout.addRow("Description:", self.description_edit)
        
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        # Note about inverse relationships
        note_label = QLabel("* Note: Inverse relationships (e.g., Parent→Child) are created automatically")
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
    
    def _on_type_changed(self):
        """Handle relationship type change."""
        current_type = self.type_combo.currentData()
        is_custom = current_type == RelationshipType.CUSTOM
        self.custom_name_label.setVisible(is_custom)
        self.custom_name_edit.setVisible(is_custom)
    
    def _load_relationship_data(self):
        """Load relationship data into form fields."""
        if not self.relationship:
            return
        
        # Set entities
        self.source_label.setText(f"{self.relationship.source_entity_type}:{self.relationship.source_entity_id}")
        self.target_label.setText(f"{self.relationship.target_entity_type}:{self.relationship.target_entity_id}")
        
        # Set type
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == self.relationship.relationship_type:
                self.type_combo.setCurrentIndex(i)
                break
        
        # Set custom name if applicable
        if self.relationship.custom_type_name:
            self.custom_name_edit.setText(self.relationship.custom_type_name)
        
        # Set strength
        for i in range(self.strength_combo.count()):
            if self.strength_combo.itemData(i) == self.relationship.strength:
                self.strength_combo.setCurrentIndex(i)
                break
        
        # Set active status
        self.active_check.setChecked(self.relationship.is_active == 1)
        
        # Set dates
        if self.relationship.start_date:
            self.start_date_edit.setText(self.relationship.start_date)
        if self.relationship.end_date:
            self.end_date_edit.setText(self.relationship.end_date)
        
        # Set description
        if self.relationship.description:
            self.description_edit.setPlainText(self.relationship.description)
    
    def _on_save(self):
        """Handle save button click."""
        # Validate
        rel_type = self.type_combo.currentData()
        if rel_type == RelationshipType.CUSTOM and not self.custom_name_edit.text().strip():
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Validation Error", "Custom relationship name is required.")
            self.custom_name_edit.setFocus()
            return
        
        self.accept()
    
    def get_data(self) -> dict:
        """Get form data as dictionary.
        
        Returns:
            Dictionary with relationship data
        """
        description = self.description_edit.toPlainText().strip()
        start_date = self.start_date_edit.text().strip()
        end_date = self.end_date_edit.text().strip()
        custom_name = self.custom_name_edit.text().strip()
        
        data = {
            "relationship_type": self.type_combo.currentData(),
            "custom_type_name": custom_name if custom_name else None,
            "strength": self.strength_combo.currentData(),
            "is_active": self.active_check.isChecked(),
            "description": description if description else None,
            "start_date": start_date if start_date else None,
            "end_date": end_date if end_date else None,
        }
        
        # Add entity info if in create mode
        if not self.is_edit_mode and self.source_info and self.target_info:
            data["universe_id"] = self.universe_id
            data["source_type"] = self.source_info[0]
            data["source_id"] = self.source_info[1]
            data["target_type"] = self.target_info[0]
            data["target_id"] = self.target_info[1]
        
        return data

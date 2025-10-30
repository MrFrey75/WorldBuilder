"""Species dialog for creating and editing species."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QTextEdit, QPushButton, QLabel, QComboBox, 
                             QCheckBox, QHBoxLayout, QGroupBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from worldbuilder.models.species import Species, SpeciesType
import json


class SpeciesDialog(QDialog):
    """Dialog for creating or editing a species."""
    
    def __init__(self, parent=None, species: Species = None, universe_id: int = None):
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
            species: Species to edit (None for create new)
            universe_id: Universe ID (required for create)
        """
        super().__init__(parent)
        self.species = species
        self.universe_id = universe_id
        self.is_edit_mode = species is not None
        
        self.setWindowTitle("Edit Species" if self.is_edit_mode else "Create New Species")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(600)
        
        self._setup_ui()
        
        if self.is_edit_mode:
            self._load_species_data()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Scroll area for all content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        
        # Basic Information Group
        basic_group = QGroupBox("Basic Information")
        basic_layout = QFormLayout()
        
        # Name field (required)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter species name (required)")
        basic_layout.addRow("Name*:", self.name_edit)
        
        # Species type
        self.type_combo = QComboBox()
        for sp_type in SpeciesType:
            self.type_combo.addItem(sp_type.value, sp_type)
        basic_layout.addRow("Type:", self.type_combo)
        
        # Playable checkbox
        self.playable_check = QCheckBox("Can be used for characters/figures")
        self.playable_check.setChecked(True)
        basic_layout.addRow("Playable:", self.playable_check)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Enter species description")
        self.description_edit.setMaximumHeight(100)
        basic_layout.addRow("Description:", self.description_edit)
        
        basic_group.setLayout(basic_layout)
        container_layout.addWidget(basic_group)
        
        # Physical Traits Group
        traits_group = QGroupBox("Physical Traits")
        traits_layout = QFormLayout()
        
        self.height_edit = QLineEdit()
        self.height_edit.setPlaceholderText("e.g., 5-6 feet")
        traits_layout.addRow("Height:", self.height_edit)
        
        self.lifespan_edit = QLineEdit()
        self.lifespan_edit.setPlaceholderText("e.g., 80-100 years")
        traits_layout.addRow("Lifespan:", self.lifespan_edit)
        
        self.build_edit = QLineEdit()
        self.build_edit.setPlaceholderText("e.g., Medium, Slender, Stocky")
        traits_layout.addRow("Build:", self.build_edit)
        
        self.skin_edit = QLineEdit()
        self.skin_edit.setPlaceholderText("e.g., Varied, Green, Scaled")
        traits_layout.addRow("Skin/Covering:", self.skin_edit)
        
        self.special_edit = QLineEdit()
        self.special_edit.setPlaceholderText("e.g., Pointed ears, Wings, Horns")
        traits_layout.addRow("Special Features:", self.special_edit)
        
        traits_group.setLayout(traits_layout)
        container_layout.addWidget(traits_group)
        
        # Abilities Group
        abilities_group = QGroupBox("Abilities & Characteristics")
        abilities_layout = QVBoxLayout()
        
        self.abilities_edit = QTextEdit()
        self.abilities_edit.setPlaceholderText("Describe special abilities, powers, or characteristics")
        self.abilities_edit.setMaximumHeight(80)
        abilities_layout.addWidget(self.abilities_edit)
        
        abilities_group.setLayout(abilities_layout)
        container_layout.addWidget(abilities_group)
        
        # Culture Group
        culture_group = QGroupBox("Culture & Society")
        culture_layout = QVBoxLayout()
        
        self.culture_edit = QTextEdit()
        self.culture_edit.setPlaceholderText("Describe typical culture, society, and customs")
        self.culture_edit.setMaximumHeight(80)
        culture_layout.addWidget(self.culture_edit)
        
        culture_group.setLayout(culture_layout)
        container_layout.addWidget(culture_group)
        
        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
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
    
    def _load_species_data(self):
        """Load species data into form fields."""
        if not self.species:
            return
        
        self.name_edit.setText(self.species.name)
        
        # Set type
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == self.species.species_type:
                self.type_combo.setCurrentIndex(i)
                break
        
        self.playable_check.setChecked(self.species.is_playable)
        
        if self.species.description:
            self.description_edit.setPlainText(self.species.description)
        
        # Load physical traits
        if self.species.physical_traits:
            self.height_edit.setText(self.species.get_trait("height", ""))
            self.lifespan_edit.setText(self.species.get_trait("lifespan", ""))
            self.build_edit.setText(self.species.get_trait("build", ""))
            self.skin_edit.setText(self.species.get_trait("skin_tones", ""))
            self.special_edit.setText(self.species.get_trait("special_features", ""))
        
        if self.species.abilities:
            self.abilities_edit.setPlainText(self.species.abilities)
        
        if self.species.culture:
            self.culture_edit.setPlainText(self.species.culture)
    
    def _on_save(self):
        """Handle save button click."""
        # Validate name
        name = self.name_edit.text().strip()
        if not name:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Validation Error", "Species name is required.")
            self.name_edit.setFocus()
            return
        
        self.accept()
    
    def get_data(self) -> dict:
        """Get form data as dictionary.
        
        Returns:
            Dictionary with species data
        """
        # Build physical traits dict
        physical_traits = {}
        if self.height_edit.text().strip():
            physical_traits["height"] = self.height_edit.text().strip()
        if self.lifespan_edit.text().strip():
            physical_traits["lifespan"] = self.lifespan_edit.text().strip()
        if self.build_edit.text().strip():
            physical_traits["build"] = self.build_edit.text().strip()
        if self.skin_edit.text().strip():
            physical_traits["skin_tones"] = self.skin_edit.text().strip()
        if self.special_edit.text().strip():
            physical_traits["special_features"] = self.special_edit.text().strip()
        
        description = self.description_edit.toPlainText().strip()
        abilities = self.abilities_edit.toPlainText().strip()
        culture = self.culture_edit.toPlainText().strip()
        
        return {
            "name": self.name_edit.text().strip(),
            "species_type": self.type_combo.currentData(),
            "is_playable": self.playable_check.isChecked(),
            "description": description if description else None,
            "physical_traits": physical_traits if physical_traits else None,
            "abilities": abilities if abilities else None,
            "culture": culture if culture else None,
            "universe_id": self.universe_id if not self.is_edit_mode else None
        }

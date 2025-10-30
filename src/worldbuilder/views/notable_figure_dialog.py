"""Notable Figure dialog for creating and editing figures."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QTextEdit, QPushButton, QLabel, QComboBox, 
                             QHBoxLayout, QGroupBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from worldbuilder.models.notable_figure import NotableFigure
from worldbuilder.models.species import Species
from worldbuilder.models.location import Location
from typing import List


class NotableFigureDialog(QDialog):
    """Dialog for creating or editing a notable figure."""
    
    def __init__(self, parent=None, figure: NotableFigure = None, 
                 universe_id: int = None, available_species: List[Species] = None,
                 available_locations: List[Location] = None):
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
            figure: Figure to edit (None for create new)
            universe_id: Universe ID (required for create)
            available_species: List of available species
            available_locations: List of available locations
        """
        super().__init__(parent)
        self.figure = figure
        self.universe_id = universe_id
        self.available_species = available_species or []
        self.available_locations = available_locations or []
        self.is_edit_mode = figure is not None
        
        self.setWindowTitle("Edit Figure" if self.is_edit_mode else "Create New Figure")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        
        self._setup_ui()
        
        if self.is_edit_mode:
            self._load_figure_data()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Scroll area
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
        self.name_edit.setPlaceholderText("Enter figure name (required)")
        basic_layout.addRow("Name*:", self.name_edit)
        
        # Title
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("e.g., King, Lord, Doctor")
        basic_layout.addRow("Title:", self.title_edit)
        
        # Species
        self.species_combo = QComboBox()
        self.species_combo.addItem("(None - Unknown Species)", None)
        for species in self.available_species:
            self.species_combo.addItem(species.name, species.id)
        basic_layout.addRow("Species:", self.species_combo)
        
        # Age
        self.age_edit = QLineEdit()
        self.age_edit.setPlaceholderText("e.g., 25, 30-40, Unknown")
        basic_layout.addRow("Age:", self.age_edit)
        
        # Occupation
        self.occupation_edit = QLineEdit()
        self.occupation_edit.setPlaceholderText("e.g., Warrior, Merchant, Scholar")
        basic_layout.addRow("Occupation:", self.occupation_edit)
        
        # Location
        self.location_combo = QComboBox()
        self.location_combo.addItem("(None - No Fixed Location)", None)
        for location in self.available_locations:
            display = f"{location.get_full_path()} ({location.location_type.value})"
            self.location_combo.addItem(display, location.id)
        basic_layout.addRow("Location:", self.location_combo)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Brief description")
        self.description_edit.setMaximumHeight(80)
        basic_layout.addRow("Description:", self.description_edit)
        
        basic_group.setLayout(basic_layout)
        container_layout.addWidget(basic_group)
        
        # Physical Attributes Group
        attr_group = QGroupBox("Physical Attributes")
        attr_layout = QFormLayout()
        
        self.hair_edit = QLineEdit()
        attr_layout.addRow("Hair Color:", self.hair_edit)
        
        self.eye_edit = QLineEdit()
        attr_layout.addRow("Eye Color:", self.eye_edit)
        
        self.height_edit = QLineEdit()
        attr_layout.addRow("Height:", self.height_edit)
        
        attr_group.setLayout(attr_layout)
        container_layout.addWidget(attr_group)
        
        # Backstory Group
        backstory_group = QGroupBox("Backstory")
        backstory_layout = QVBoxLayout()
        
        self.backstory_edit = QTextEdit()
        self.backstory_edit.setPlaceholderText("Character history and background")
        self.backstory_edit.setMaximumHeight(100)
        backstory_layout.addWidget(self.backstory_edit)
        
        backstory_group.setLayout(backstory_layout)
        container_layout.addWidget(backstory_group)
        
        # Personality Group
        personality_group = QGroupBox("Personality")
        personality_layout = QVBoxLayout()
        
        self.personality_edit = QTextEdit()
        self.personality_edit.setPlaceholderText("Traits, quirks, and characteristics")
        self.personality_edit.setMaximumHeight(80)
        personality_layout.addWidget(self.personality_edit)
        
        personality_group.setLayout(personality_layout)
        container_layout.addWidget(personality_group)
        
        # Goals Group
        goals_group = QGroupBox("Goals & Motivations")
        goals_layout = QVBoxLayout()
        
        self.goals_edit = QTextEdit()
        self.goals_edit.setPlaceholderText("What drives this character?")
        self.goals_edit.setMaximumHeight(80)
        goals_layout.addWidget(self.goals_edit)
        
        goals_group.setLayout(goals_layout)
        container_layout.addWidget(goals_group)
        
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
    
    def _load_figure_data(self):
        """Load figure data into form fields."""
        if not self.figure:
            return
        
        self.name_edit.setText(self.figure.name)
        
        if self.figure.title:
            self.title_edit.setText(self.figure.title)
        
        # Set species
        if self.figure.species_id:
            for i in range(self.species_combo.count()):
                if self.species_combo.itemData(i) == self.figure.species_id:
                    self.species_combo.setCurrentIndex(i)
                    break
        
        if self.figure.age:
            self.age_edit.setText(self.figure.age)
        
        if self.figure.occupation:
            self.occupation_edit.setText(self.figure.occupation)
        
        # Set location
        if self.figure.location_id:
            for i in range(self.location_combo.count()):
                if self.location_combo.itemData(i) == self.figure.location_id:
                    self.location_combo.setCurrentIndex(i)
                    break
        
        if self.figure.description:
            self.description_edit.setPlainText(self.figure.description)
        
        # Load attributes
        if self.figure.attributes:
            self.hair_edit.setText(self.figure.get_attribute("hair_color", ""))
            self.eye_edit.setText(self.figure.get_attribute("eye_color", ""))
            self.height_edit.setText(self.figure.get_attribute("height", ""))
        
        if self.figure.backstory:
            self.backstory_edit.setPlainText(self.figure.backstory)
        
        if self.figure.personality:
            self.personality_edit.setPlainText(self.figure.personality)
        
        if self.figure.goals:
            self.goals_edit.setPlainText(self.figure.goals)
    
    def _on_save(self):
        """Handle save button click."""
        # Validate name
        name = self.name_edit.text().strip()
        if not name:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Validation Error", "Figure name is required.")
            self.name_edit.setFocus()
            return
        
        self.accept()
    
    def get_data(self) -> dict:
        """Get form data as dictionary.
        
        Returns:
            Dictionary with figure data
        """
        # Build attributes dict
        attributes = {}
        if self.hair_edit.text().strip():
            attributes["hair_color"] = self.hair_edit.text().strip()
        if self.eye_edit.text().strip():
            attributes["eye_color"] = self.eye_edit.text().strip()
        if self.height_edit.text().strip():
            attributes["height"] = self.height_edit.text().strip()
        
        title = self.title_edit.text().strip()
        age = self.age_edit.text().strip()
        occupation = self.occupation_edit.text().strip()
        description = self.description_edit.toPlainText().strip()
        backstory = self.backstory_edit.toPlainText().strip()
        personality = self.personality_edit.toPlainText().strip()
        goals = self.goals_edit.toPlainText().strip()
        
        return {
            "name": self.name_edit.text().strip(),
            "title": title if title else None,
            "species_id": self.species_combo.currentData(),
            "age": age if age else None,
            "occupation": occupation if occupation else None,
            "location_id": self.location_combo.currentData(),
            "description": description if description else None,
            "attributes": attributes if attributes else None,
            "backstory": backstory if backstory else None,
            "personality": personality if personality else None,
            "goals": goals if goals else None,
            "universe_id": self.universe_id if not self.is_edit_mode else None
        }

"""Dialog for creating and editing universes."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QTextEdit, QPushButton, QLabel, QComboBox)
from PyQt6.QtCore import Qt
from worldbuilder.models.universe import Universe


class UniverseDialog(QDialog):
    """Dialog for creating or editing a universe."""
    
    GENRES = [
        "",  # Empty for no selection
        "Fantasy",
        "Science Fiction",
        "Horror",
        "Mystery",
        "Historical",
        "Contemporary",
        "Post-Apocalyptic",
        "Cyberpunk",
        "Steampunk",
        "Urban Fantasy",
        "Space Opera",
        "Other"
    ]
    
    def __init__(self, parent=None, universe: Universe = None):
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
            universe: Universe to edit (None for create new)
        """
        super().__init__(parent)
        self.universe = universe
        self.is_edit_mode = universe is not None
        
        self.setWindowTitle("Edit Universe" if self.is_edit_mode else "Create New Universe")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self._setup_ui()
        
        if self.is_edit_mode:
            self._load_universe_data()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Name field (required)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter universe name (required)")
        form_layout.addRow("Name*:", self.name_edit)
        
        # Author field
        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("Enter author name")
        form_layout.addRow("Author:", self.author_edit)
        
        # Genre dropdown
        self.genre_combo = QComboBox()
        self.genre_combo.addItems(self.GENRES)
        form_layout.addRow("Genre:", self.genre_combo)
        
        # Description field
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Enter universe description")
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
    
    def _load_universe_data(self):
        """Load universe data into form fields."""
        if not self.universe:
            return
        
        self.name_edit.setText(self.universe.name)
        
        if self.universe.author:
            self.author_edit.setText(self.universe.author)
        
        if self.universe.genre:
            index = self.genre_combo.findText(self.universe.genre)
            if index >= 0:
                self.genre_combo.setCurrentIndex(index)
        
        if self.universe.description:
            self.description_edit.setPlainText(self.universe.description)
    
    def _on_save(self):
        """Handle save button click."""
        # Validate name
        name = self.name_edit.text().strip()
        if not name:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Validation Error", "Universe name is required.")
            self.name_edit.setFocus()
            return
        
        self.accept()
    
    def get_data(self) -> dict:
        """Get form data as dictionary.
        
        Returns:
            Dictionary with universe data
        """
        genre = self.genre_combo.currentText()
        if not genre or genre == "":
            genre = None
        
        description = self.description_edit.toPlainText().strip()
        if not description:
            description = None
        
        author = self.author_edit.text().strip()
        if not author:
            author = None
        
        return {
            "name": self.name_edit.text().strip(),
            "author": author,
            "genre": genre,
            "description": description
        }

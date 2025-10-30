"""Species list view widget."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel)
from PyQt6.QtCore import pyqtSignal, Qt
from worldbuilder.models.species import Species
from typing import List


class SpeciesListView(QWidget):
    """Widget displaying a list of species."""
    
    # Signals
    species_selected = pyqtSignal(int)  # Emits species ID
    create_requested = pyqtSignal()
    edit_requested = pyqtSignal(int)  # Emits species ID
    delete_requested = pyqtSignal(int)  # Emits species ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Species & Races")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Create button
        self.create_button = QPushButton("New Species")
        self.create_button.clicked.connect(self.create_requested.emit)
        header_layout.addWidget(self.create_button)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Playable", "Description"])
        
        # Configure table
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        # Connect signals
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        layout.addWidget(self.table)
        
        # Button bar
        button_layout = QHBoxLayout()
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self._on_edit_clicked)
        self.edit_button.setEnabled(False)
        button_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self._on_delete_clicked)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def load_species(self, species_list: List[Species]):
        """Load species into the table.
        
        Args:
            species_list: List of Species entities
        """
        self.table.setRowCount(0)
        
        for species in species_list:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # ID (hidden data)
            name_item = QTableWidgetItem(species.name)
            name_item.setData(Qt.ItemDataRole.UserRole, species.id)
            self.table.setItem(row, 0, name_item)
            
            # Type
            type_item = QTableWidgetItem(species.species_type.value)
            self.table.setItem(row, 1, type_item)
            
            # Playable
            playable_item = QTableWidgetItem("Yes" if species.is_playable else "No")
            playable_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, playable_item)
            
            # Description
            desc_text = (species.description or "")[:100]
            desc_item = QTableWidgetItem(desc_text)
            self.table.setItem(row, 3, desc_item)
    
    def get_selected_species_id(self) -> int:
        """Get the ID of the selected species.
        
        Returns:
            Species ID or None if no selection
        """
        selected_items = self.table.selectedItems()
        if not selected_items:
            return None
        
        row = selected_items[0].row()
        id_item = self.table.item(row, 0)
        return id_item.data(Qt.ItemDataRole.UserRole)
    
    def _on_selection_changed(self):
        """Handle selection change."""
        has_selection = len(self.table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        
        if has_selection:
            species_id = self.get_selected_species_id()
            self.species_selected.emit(species_id)
    
    def _on_item_double_clicked(self, item):
        """Handle item double click - edit species."""
        species_id = self.get_selected_species_id()
        if species_id:
            self.edit_requested.emit(species_id)
    
    def _on_edit_clicked(self):
        """Handle edit button click."""
        species_id = self.get_selected_species_id()
        if species_id:
            self.edit_requested.emit(species_id)
    
    def _on_delete_clicked(self):
        """Handle delete button click."""
        species_id = self.get_selected_species_id()
        if species_id:
            self.delete_requested.emit(species_id)

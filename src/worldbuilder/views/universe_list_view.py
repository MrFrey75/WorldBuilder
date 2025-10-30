"""Universe management view showing list of universes."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QLabel)
from PyQt6.QtCore import pyqtSignal, Qt
from worldbuilder.models.universe import Universe
from typing import List


class UniverseListView(QWidget):
    """Widget displaying a list of universes."""
    
    # Signals
    universe_selected = pyqtSignal(int)  # Emits universe ID
    create_requested = pyqtSignal()
    edit_requested = pyqtSignal(int)  # Emits universe ID
    delete_requested = pyqtSignal(int)  # Emits universe ID
    open_requested = pyqtSignal(int)  # Emits universe ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Universes")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Create button
        self.create_button = QPushButton("New Universe")
        self.create_button.clicked.connect(self.create_requested.emit)
        header_layout.addWidget(self.create_button)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Author", "Genre", "Status"])
        
        # Configure table
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 80)
        
        # Connect signals
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        layout.addWidget(self.table)
        
        # Button bar
        button_layout = QHBoxLayout()
        
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self._on_open_clicked)
        self.open_button.setEnabled(False)
        button_layout.addWidget(self.open_button)
        
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
    
    def load_universes(self, universes: List[Universe]):
        """Load universes into the table.
        
        Args:
            universes: List of Universe entities
        """
        self.table.setRowCount(0)
        
        for universe in universes:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(universe.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, id_item)
            
            # Name
            name_item = QTableWidgetItem(universe.name)
            self.table.setItem(row, 1, name_item)
            
            # Author
            author_item = QTableWidgetItem(universe.author or "")
            self.table.setItem(row, 2, author_item)
            
            # Genre
            genre_item = QTableWidgetItem(universe.genre or "")
            self.table.setItem(row, 3, genre_item)
            
            # Status
            status_item = QTableWidgetItem("Active" if universe.is_active else "Inactive")
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if universe.is_active:
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            self.table.setItem(row, 4, status_item)
    
    def get_selected_universe_id(self) -> int:
        """Get the ID of the selected universe.
        
        Returns:
            Universe ID or None if no selection
        """
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        id_item = self.table.item(row, 0)
        return int(id_item.text())
    
    def _on_selection_changed(self):
        """Handle selection change."""
        has_selection = len(self.table.selectedItems()) > 0
        self.open_button.setEnabled(has_selection)
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        
        if has_selection:
            universe_id = self.get_selected_universe_id()
            self.universe_selected.emit(universe_id)
    
    def _on_item_double_clicked(self, item):
        """Handle item double click - open universe."""
        universe_id = self.get_selected_universe_id()
        if universe_id:
            self.open_requested.emit(universe_id)
    
    def _on_open_clicked(self):
        """Handle open button click."""
        universe_id = self.get_selected_universe_id()
        if universe_id:
            self.open_requested.emit(universe_id)
    
    def _on_edit_clicked(self):
        """Handle edit button click."""
        universe_id = self.get_selected_universe_id()
        if universe_id:
            self.edit_requested.emit(universe_id)
    
    def _on_delete_clicked(self):
        """Handle delete button click."""
        universe_id = self.get_selected_universe_id()
        if universe_id:
            self.delete_requested.emit(universe_id)

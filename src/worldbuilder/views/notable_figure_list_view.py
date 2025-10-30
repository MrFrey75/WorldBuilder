"""Notable Figure list view widget."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel)
from PyQt6.QtCore import pyqtSignal, Qt
from worldbuilder.models.notable_figure import NotableFigure
from typing import List


class NotableFigureListView(QWidget):
    """Widget displaying a list of notable figures."""
    
    # Signals
    figure_selected = pyqtSignal(int)  # Emits figure ID
    create_requested = pyqtSignal()
    edit_requested = pyqtSignal(int)  # Emits figure ID
    delete_requested = pyqtSignal(int)  # Emits figure ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Notable Figures")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Create button
        self.create_button = QPushButton("New Figure")
        self.create_button.clicked.connect(self.create_requested.emit)
        header_layout.addWidget(self.create_button)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Species", "Occupation", "Location", "Age"])
        
        # Configure table
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
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
    
    def load_figures(self, figures: List[NotableFigure]):
        """Load figures into the table.
        
        Args:
            figures: List of NotableFigure entities
        """
        self.table.setRowCount(0)
        
        for figure in figures:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Name (with title if present)
            name_item = QTableWidgetItem(figure.get_full_name())
            name_item.setData(Qt.ItemDataRole.UserRole, figure.id)
            self.table.setItem(row, 0, name_item)
            
            # Species
            species_text = figure.species.name if figure.species else "Unknown"
            species_item = QTableWidgetItem(species_text)
            self.table.setItem(row, 1, species_item)
            
            # Occupation
            occupation_item = QTableWidgetItem(figure.occupation or "")
            self.table.setItem(row, 2, occupation_item)
            
            # Location
            location_text = figure.location.name if figure.location else ""
            location_item = QTableWidgetItem(location_text)
            self.table.setItem(row, 3, location_item)
            
            # Age
            age_item = QTableWidgetItem(figure.age or "")
            age_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, age_item)
    
    def get_selected_figure_id(self) -> int:
        """Get the ID of the selected figure.
        
        Returns:
            Figure ID or None if no selection
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
            figure_id = self.get_selected_figure_id()
            self.figure_selected.emit(figure_id)
    
    def _on_item_double_clicked(self, item):
        """Handle item double click - edit figure."""
        figure_id = self.get_selected_figure_id()
        if figure_id:
            self.edit_requested.emit(figure_id)
    
    def _on_edit_clicked(self):
        """Handle edit button click."""
        figure_id = self.get_selected_figure_id()
        if figure_id:
            self.edit_requested.emit(figure_id)
    
    def _on_delete_clicked(self):
        """Handle delete button click."""
        figure_id = self.get_selected_figure_id()
        if figure_id:
            self.delete_requested.emit(figure_id)

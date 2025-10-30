"""Event list view widget."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel)
from PyQt6.QtCore import pyqtSignal, Qt
from worldbuilder.models.event import Event
from typing import List


class EventListView(QWidget):
    """Widget displaying a list of events."""
    
    # Signals
    event_selected = pyqtSignal(int)
    create_requested = pyqtSignal()
    edit_requested = pyqtSignal(int)
    delete_requested = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Events")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.create_button = QPushButton("New Event")
        self.create_button.clicked.connect(self.create_requested.emit)
        header_layout.addWidget(self.create_button)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Date", "Importance", "Duration"])
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
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
    
    def load_events(self, events: List[Event]):
        """Load events into the table."""
        self.table.setRowCount(0)
        
        for event in events:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            name_item = QTableWidgetItem(event.name)
            name_item.setData(Qt.ItemDataRole.UserRole, event.id)
            self.table.setItem(row, 0, name_item)
            
            type_item = QTableWidgetItem(event.event_type.value)
            self.table.setItem(row, 1, type_item)
            
            date_item = QTableWidgetItem(event.date_string or "Unknown")
            self.table.setItem(row, 2, date_item)
            
            importance_item = QTableWidgetItem(event.importance.value)
            importance_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, importance_item)
            
            duration_item = QTableWidgetItem(event.get_duration_display())
            self.table.setItem(row, 4, duration_item)
    
    def get_selected_event_id(self) -> int:
        """Get the ID of the selected event."""
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
            event_id = self.get_selected_event_id()
            self.event_selected.emit(event_id)
    
    def _on_item_double_clicked(self, item):
        """Handle item double click."""
        event_id = self.get_selected_event_id()
        if event_id:
            self.edit_requested.emit(event_id)
    
    def _on_edit_clicked(self):
        """Handle edit button click."""
        event_id = self.get_selected_event_id()
        if event_id:
            self.edit_requested.emit(event_id)
    
    def _on_delete_clicked(self):
        """Handle delete button click."""
        event_id = self.get_selected_event_id()
        if event_id:
            self.delete_requested.emit(event_id)

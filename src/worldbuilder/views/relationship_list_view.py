"""Relationship list view widget."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel)
from PyQt6.QtCore import pyqtSignal, Qt
from worldbuilder.models.relationship import Relationship
from typing import List


class RelationshipListView(QWidget):
    """Widget displaying a list of relationships."""
    
    # Signals
    relationship_selected = pyqtSignal(int)  # Emits relationship ID
    edit_requested = pyqtSignal(int)  # Emits relationship ID
    delete_requested = pyqtSignal(int)  # Emits relationship ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Relationships")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Source", "Relationship", "Target", "Strength", "Status", "Start Date"
        ])
        
        # Configure table
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
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
    
    def load_relationships(self, relationships: List[Relationship], entity_names: dict = None):
        """Load relationships into the table.
        
        Args:
            relationships: List of Relationship entities
            entity_names: Dict mapping (type, id) tuples to entity names
        """
        self.table.setRowCount(0)
        entity_names = entity_names or {}
        
        for rel in relationships:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Source
            source_key = (rel.source_entity_type, rel.source_entity_id)
            source_name = entity_names.get(source_key, f"{rel.source_entity_type}:{rel.source_entity_id}")
            source_item = QTableWidgetItem(source_name)
            source_item.setData(Qt.ItemDataRole.UserRole, rel.id)
            self.table.setItem(row, 0, source_item)
            
            # Relationship type
            type_item = QTableWidgetItem(rel.get_type_display())
            self.table.setItem(row, 1, type_item)
            
            # Target
            target_key = (rel.target_entity_type, rel.target_entity_id)
            target_name = entity_names.get(target_key, f"{rel.target_entity_type}:{rel.target_entity_id}")
            target_item = QTableWidgetItem(target_name)
            self.table.setItem(row, 2, target_item)
            
            # Strength
            strength_text = rel.strength.value if rel.strength else ""
            strength_item = QTableWidgetItem(strength_text)
            strength_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, strength_item)
            
            # Status
            status_text = "Active" if rel.is_active == 1 else "Ended"
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, status_item)
            
            # Start date
            date_item = QTableWidgetItem(rel.start_date or "")
            self.table.setItem(row, 5, date_item)
    
    def get_selected_relationship_id(self) -> int:
        """Get the ID of the selected relationship.
        
        Returns:
            Relationship ID or None if no selection
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
            rel_id = self.get_selected_relationship_id()
            self.relationship_selected.emit(rel_id)
    
    def _on_item_double_clicked(self, item):
        """Handle item double click - edit relationship."""
        rel_id = self.get_selected_relationship_id()
        if rel_id:
            self.edit_requested.emit(rel_id)
    
    def _on_edit_clicked(self):
        """Handle edit button click."""
        rel_id = self.get_selected_relationship_id()
        if rel_id:
            self.edit_requested.emit(rel_id)
    
    def _on_delete_clicked(self):
        """Handle delete button click."""
        rel_id = self.get_selected_relationship_id()
        if rel_id:
            self.delete_requested.emit(rel_id)

"""Location tree view widget with hierarchical display."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTreeWidget, QTreeWidgetItem, QLabel, QMessageBox, QMenu)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction
from worldbuilder.models.location import Location, LocationType
from typing import List, Dict, Optional


class LocationTreeView(QWidget):
    """Widget displaying locations in a hierarchical tree structure."""
    
    # Signals
    location_selected = pyqtSignal(int)  # Emits location ID
    create_requested = pyqtSignal(int)  # Emits parent ID (or 0 for root)
    edit_requested = pyqtSignal(int)  # Emits location ID
    delete_requested = pyqtSignal(int)  # Emits location ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._location_items = {}  # Maps location ID to QTreeWidgetItem
        self._current_universe_id = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Locations")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Create root button
        self.create_button = QPushButton("New Root Location")
        self.create_button.clicked.connect(lambda: self.create_requested.emit(0))
        header_layout.addWidget(self.create_button)
        
        layout.addLayout(header_layout)
        
        # Tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Name", "Type", "Description"])
        self.tree.setColumnWidth(0, 250)
        self.tree.setColumnWidth(1, 120)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        self.tree.itemSelectionChanged.connect(self._on_selection_changed)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.tree)
        
        # Button bar
        button_layout = QHBoxLayout()
        
        self.add_child_button = QPushButton("Add Child")
        self.add_child_button.clicked.connect(self._on_add_child_clicked)
        self.add_child_button.setEnabled(False)
        button_layout.addWidget(self.add_child_button)
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self._on_edit_clicked)
        self.edit_button.setEnabled(False)
        button_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self._on_delete_clicked)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button)
        
        button_layout.addStretch()
        
        # Expand/Collapse buttons
        self.expand_all_button = QPushButton("Expand All")
        self.expand_all_button.clicked.connect(self.tree.expandAll)
        button_layout.addWidget(self.expand_all_button)
        
        self.collapse_all_button = QPushButton("Collapse All")
        self.collapse_all_button.clicked.connect(self.tree.collapseAll)
        button_layout.addWidget(self.collapse_all_button)
        
        layout.addLayout(button_layout)
    
    def set_universe(self, universe_id: int):
        """Set the current universe context.
        
        Args:
            universe_id: Universe ID to display locations for
        """
        self._current_universe_id = universe_id
    
    def load_locations(self, locations: List[Location]):
        """Load locations into the tree.
        
        Args:
            locations: List of all locations (flat list)
        """
        self.tree.clear()
        self._location_items.clear()
        
        if not locations:
            return
        
        # Separate root and non-root locations
        root_locations = [loc for loc in locations if loc.parent_id is None]
        child_locations = [loc for loc in locations if loc.parent_id is not None]
        
        # Add root locations first
        for location in root_locations:
            self._add_location_item(location, None)
        
        # Add children recursively
        self._add_children_recursive(child_locations)
        
        # Expand first level
        self.tree.expandToDepth(0)
    
    def _add_location_item(self, location: Location, parent_item: Optional[QTreeWidgetItem]) -> QTreeWidgetItem:
        """Add a location to the tree.
        
        Args:
            location: Location to add
            parent_item: Parent tree item (None for root)
            
        Returns:
            Created tree item
        """
        item = QTreeWidgetItem()
        item.setText(0, location.name)
        item.setText(1, location.location_type.value)
        item.setText(2, (location.description or "")[:100])  # Truncate long descriptions
        item.setData(0, Qt.ItemDataRole.UserRole, location.id)
        
        if parent_item:
            parent_item.addChild(item)
        else:
            self.tree.addTopLevelItem(item)
        
        self._location_items[location.id] = item
        return item
    
    def _add_children_recursive(self, locations: List[Location]):
        """Recursively add child locations to tree.
        
        Args:
            locations: List of locations to add
        """
        added_any = True
        remaining = locations.copy()
        
        while added_any and remaining:
            added_any = False
            still_remaining = []
            
            for location in remaining:
                parent_item = self._location_items.get(location.parent_id)
                if parent_item:
                    self._add_location_item(location, parent_item)
                    added_any = True
                else:
                    still_remaining.append(location)
            
            remaining = still_remaining
    
    def get_selected_location_id(self) -> Optional[int]:
        """Get the ID of the selected location.
        
        Returns:
            Location ID or None if no selection
        """
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return None
        
        return selected_items[0].data(0, Qt.ItemDataRole.UserRole)
    
    def _on_selection_changed(self):
        """Handle selection change."""
        has_selection = len(self.tree.selectedItems()) > 0
        self.add_child_button.setEnabled(has_selection)
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        
        if has_selection:
            location_id = self.get_selected_location_id()
            self.location_selected.emit(location_id)
    
    def _on_item_double_clicked(self, item, column):
        """Handle item double click - edit location."""
        location_id = self.get_selected_location_id()
        if location_id:
            self.edit_requested.emit(location_id)
    
    def _on_add_child_clicked(self):
        """Handle add child button click."""
        parent_id = self.get_selected_location_id()
        if parent_id:
            self.create_requested.emit(parent_id)
    
    def _on_edit_clicked(self):
        """Handle edit button click."""
        location_id = self.get_selected_location_id()
        if location_id:
            self.edit_requested.emit(location_id)
    
    def _on_delete_clicked(self):
        """Handle delete button click."""
        location_id = self.get_selected_location_id()
        if location_id:
            self.delete_requested.emit(location_id)
    
    def _show_context_menu(self, position):
        """Show context menu for tree items."""
        item = self.tree.itemAt(position)
        if not item:
            return
        
        menu = QMenu()
        
        edit_action = QAction("Edit", self)
        edit_action.triggered.connect(self._on_edit_clicked)
        menu.addAction(edit_action)
        
        add_child_action = QAction("Add Child Location", self)
        add_child_action.triggered.connect(self._on_add_child_clicked)
        menu.addAction(add_child_action)
        
        menu.addSeparator()
        
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self._on_delete_clicked)
        menu.addAction(delete_action)
        
        menu.exec(self.tree.viewport().mapToGlobal(position))

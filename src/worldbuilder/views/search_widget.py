"""Search widget for global entity search."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QLabel, QComboBox, QCheckBox, QGroupBox)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QFont
from typing import List
from worldbuilder.services.search_service import SearchResult


class SearchWidget(QWidget):
    """Widget for searching across all entities."""
    
    # Signals
    result_selected = pyqtSignal(str, int)  # entity_type, entity_id
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._perform_search)
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Global Search")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Search input
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search across all entities...")
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.search_input.returnPressed.connect(self._perform_search)
        search_layout.addWidget(self.search_input, stretch=3)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self._perform_search)
        search_layout.addWidget(self.search_button)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self._clear_search)
        search_layout.addWidget(self.clear_button)
        
        layout.addLayout(search_layout)
        
        # Filter options
        filter_group = QGroupBox("Filter by Entity Type")
        filter_layout = QHBoxLayout()
        
        self.filter_checks = {}
        entity_types = [
            ('Universe', 'universe'),
            ('Location', 'location'),
            ('Species', 'species'),
            ('Figure', 'notable_figure'),
            ('Relationship', 'relationship'),
            ('Event', 'event'),
            ('Timeline', 'timeline')
        ]
        
        for display_name, internal_name in entity_types:
            check = QCheckBox(display_name)
            check.setChecked(True)
            check.stateChanged.connect(self._on_filter_changed)
            self.filter_checks[internal_name] = check
            filter_layout.addWidget(check)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # Results count label
        self.results_label = QLabel("Enter search query...")
        self.results_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.results_label)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels([
            "Type", "Name/Title", "Matched Field", "Match Snippet"
        ])
        
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        self.results_table.itemDoubleClicked.connect(self._on_result_double_clicked)
        
        layout.addWidget(self.results_table)
        
        # View button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.view_button = QPushButton("View Selected")
        self.view_button.clicked.connect(self._on_view_clicked)
        self.view_button.setEnabled(False)
        button_layout.addWidget(self.view_button)
        
        layout.addLayout(button_layout)
        
        self.results_table.itemSelectionChanged.connect(self._on_selection_changed)
    
    def _on_search_text_changed(self):
        """Handle search text change with debouncing."""
        # Reset timer on each keystroke (debounce)
        self._search_timer.stop()
        if self.search_input.text().strip():
            self._search_timer.start(500)  # Wait 500ms after typing stops
    
    def _on_filter_changed(self):
        """Handle filter checkbox change."""
        # Re-run search if we have results
        if self.results_table.rowCount() > 0:
            self._perform_search()
    
    def _perform_search(self):
        """Perform the actual search (to be connected to service)."""
        query = self.search_input.text().strip()
        if not query:
            self.results_label.setText("Enter search query...")
            self.results_table.setRowCount(0)
            return
        
        # This is a placeholder - will be connected to actual service
        self.results_label.setText(f"Searching for '{query}'...")
        # Emit signal for parent to handle actual search
    
    def load_results(self, results: List[SearchResult]):
        """Load search results into the table.
        
        Args:
            results: List of SearchResult objects
        """
        self.results_table.setRowCount(0)
        
        if not results:
            self.results_label.setText("No results found.")
            return
        
        self.results_label.setText(f"Found {len(results)} result(s)")
        
        for result in results:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            
            # Entity type
            type_item = QTableWidgetItem(result.entity_type.replace('_', ' ').title())
            type_item.setData(Qt.ItemDataRole.UserRole, result)
            self.results_table.setItem(row, 0, type_item)
            
            # Entity name/title
            name = self._get_entity_display_name(result.entity)
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("", weight=QFont.Weight.Bold))
            self.results_table.setItem(row, 1, name_item)
            
            # Matched field
            field_item = QTableWidgetItem(result.matched_field)
            self.results_table.setItem(row, 2, field_item)
            
            # Match snippet
            snippet_item = QTableWidgetItem(result.match_snippet)
            self.results_table.setItem(row, 3, snippet_item)
    
    def _get_entity_display_name(self, entity) -> str:
        """Get display name for an entity."""
        if hasattr(entity, 'name'):
            return entity.name
        return str(entity)
    
    def get_selected_entity_types(self) -> List[str]:
        """Get list of selected entity types from filters.
        
        Returns:
            List of entity type names
        """
        return [name for name, check in self.filter_checks.items() if check.isChecked()]
    
    def _get_selected_result(self) -> SearchResult:
        """Get the selected search result.
        
        Returns:
            SearchResult or None
        """
        selected_items = self.results_table.selectedItems()
        if not selected_items:
            return None
        
        row = selected_items[0].row()
        type_item = self.results_table.item(row, 0)
        return type_item.data(Qt.ItemDataRole.UserRole)
    
    def _on_selection_changed(self):
        """Handle selection change in results table."""
        has_selection = len(self.results_table.selectedItems()) > 0
        self.view_button.setEnabled(has_selection)
    
    def _on_result_double_clicked(self, item):
        """Handle double-click on result."""
        result = self._get_selected_result()
        if result:
            self.result_selected.emit(result.entity_type, result.entity_id)
    
    def _on_view_clicked(self):
        """Handle view button click."""
        result = self._get_selected_result()
        if result:
            self.result_selected.emit(result.entity_type, result.entity_id)
    
    def _clear_search(self):
        """Clear search input and results."""
        self.search_input.clear()
        self.results_table.setRowCount(0)
        self.results_label.setText("Enter search query...")
        self.view_button.setEnabled(False)
    
    def get_search_query(self) -> str:
        """Get the current search query.
        
        Returns:
            Search query string
        """
        return self.search_input.text().strip()

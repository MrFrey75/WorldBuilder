"""Advanced filter widget for entity filtering."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QComboBox, QGroupBox, QFormLayout,
                             QLineEdit, QCheckBox, QScrollArea)
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any, Optional


class FilterPreset:
    """Represents a saved filter configuration."""
    
    def __init__(self, name: str, filters: Dict[str, Any]):
        self.name = name
        self.filters = filters
    
    def __repr__(self):
        return f"<FilterPreset(name='{self.name}')>"


class AdvancedFilterWidget(QWidget):
    """Widget for advanced entity filtering."""
    
    # Signals
    filters_changed = pyqtSignal(dict)  # Emits filter configuration
    filter_applied = pyqtSignal(dict)   # Emits when Apply clicked
    filter_cleared = pyqtSignal()       # Emits when Clear clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        main_layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Advanced Filters")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        # Scroll area for filters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        
        # Entity Type Filter
        type_group = QGroupBox("Entity Type")
        type_layout = QVBoxLayout()
        
        self.type_combo = QComboBox()
        self.type_combo.addItem("All Types", None)
        self.type_combo.addItem("Universe", "universe")
        self.type_combo.addItem("Location", "location")
        self.type_combo.addItem("Species", "species")
        self.type_combo.addItem("Notable Figure", "notable_figure")
        self.type_combo.addItem("Relationship", "relationship")
        self.type_combo.addItem("Event", "event")
        self.type_combo.addItem("Timeline", "timeline")
        self.type_combo.currentIndexChanged.connect(self._on_filter_changed)
        type_layout.addWidget(self.type_combo)
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # Location Filter
        location_group = QGroupBox("Filter by Location")
        location_layout = QFormLayout()
        
        self.location_enabled = QCheckBox("Enable")
        self.location_enabled.stateChanged.connect(self._on_filter_changed)
        location_layout.addRow("", self.location_enabled)
        
        self.location_combo = QComboBox()
        self.location_combo.addItem("Select Location...", None)
        self.location_combo.setEnabled(False)
        self.location_combo.currentIndexChanged.connect(self._on_filter_changed)
        self.location_enabled.stateChanged.connect(
            lambda: self.location_combo.setEnabled(self.location_enabled.isChecked())
        )
        location_layout.addRow("Location:", self.location_combo)
        
        self.include_sublocation = QCheckBox("Include sub-locations")
        self.include_sublocation.setChecked(True)
        self.include_sublocation.setEnabled(False)
        self.include_sublocation.stateChanged.connect(self._on_filter_changed)
        self.location_enabled.stateChanged.connect(
            lambda: self.include_sublocation.setEnabled(self.location_enabled.isChecked())
        )
        location_layout.addRow("", self.include_sublocation)
        
        location_group.setLayout(location_layout)
        layout.addWidget(location_group)
        
        # Species Filter
        species_group = QGroupBox("Filter by Species")
        species_layout = QFormLayout()
        
        self.species_enabled = QCheckBox("Enable")
        self.species_enabled.stateChanged.connect(self._on_filter_changed)
        species_layout.addRow("", self.species_enabled)
        
        self.species_combo = QComboBox()
        self.species_combo.addItem("Select Species...", None)
        self.species_combo.setEnabled(False)
        self.species_combo.currentIndexChanged.connect(self._on_filter_changed)
        self.species_enabled.stateChanged.connect(
            lambda: self.species_combo.setEnabled(self.species_enabled.isChecked())
        )
        species_layout.addRow("Species:", self.species_combo)
        
        species_group.setLayout(species_layout)
        layout.addWidget(species_group)
        
        # Date/Timeline Filter
        date_group = QGroupBox("Filter by Date/Timeline")
        date_layout = QFormLayout()
        
        self.date_enabled = QCheckBox("Enable")
        self.date_enabled.stateChanged.connect(self._on_filter_changed)
        date_layout.addRow("", self.date_enabled)
        
        self.timeline_combo = QComboBox()
        self.timeline_combo.addItem("Select Timeline...", None)
        self.timeline_combo.setEnabled(False)
        self.timeline_combo.currentIndexChanged.connect(self._on_filter_changed)
        self.date_enabled.stateChanged.connect(
            lambda: self.timeline_combo.setEnabled(self.date_enabled.isChecked())
        )
        date_layout.addRow("Timeline:", self.timeline_combo)
        
        self.date_from = QLineEdit()
        self.date_from.setPlaceholderText("From date...")
        self.date_from.setEnabled(False)
        self.date_from.textChanged.connect(self._on_filter_changed)
        self.date_enabled.stateChanged.connect(
            lambda: self.date_from.setEnabled(self.date_enabled.isChecked())
        )
        date_layout.addRow("Date From:", self.date_from)
        
        self.date_to = QLineEdit()
        self.date_to.setPlaceholderText("To date...")
        self.date_to.setEnabled(False)
        self.date_to.textChanged.connect(self._on_filter_changed)
        self.date_enabled.stateChanged.connect(
            lambda: self.date_to.setEnabled(self.date_enabled.isChecked())
        )
        date_layout.addRow("Date To:", self.date_to)
        
        date_group.setLayout(date_layout)
        layout.addWidget(date_group)
        
        # Tags Filter (placeholder for future)
        tags_group = QGroupBox("Filter by Tags")
        tags_layout = QFormLayout()
        
        self.tags_enabled = QCheckBox("Enable")
        self.tags_enabled.setEnabled(False)  # Not implemented yet
        tags_layout.addRow("", self.tags_enabled)
        
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Enter tags (comma separated)...")
        self.tags_input.setEnabled(False)
        tags_layout.addRow("Tags:", self.tags_input)
        
        tags_group.setLayout(tags_layout)
        layout.addWidget(tags_group)
        
        layout.addStretch()
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.apply_button = QPushButton("Apply Filters")
        self.apply_button.clicked.connect(self._on_apply_clicked)
        button_layout.addWidget(self.apply_button)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self._on_clear_clicked)
        button_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(button_layout)
        
        # Preset management (for future)
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Presets:"))
        
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("No presets saved", None)
        self.preset_combo.setEnabled(False)  # Not implemented yet
        preset_layout.addWidget(self.preset_combo, stretch=1)
        
        self.save_preset_button = QPushButton("Save")
        self.save_preset_button.setEnabled(False)
        preset_layout.addWidget(self.save_preset_button)
        
        main_layout.addLayout(preset_layout)
    
    def _on_filter_changed(self):
        """Handle filter change."""
        filters = self.get_filters()
        self.filters_changed.emit(filters)
    
    def _on_apply_clicked(self):
        """Handle Apply button click."""
        filters = self.get_filters()
        self.filter_applied.emit(filters)
    
    def _on_clear_clicked(self):
        """Handle Clear button click."""
        self.clear_filters()
        self.filter_cleared.emit()
    
    def get_filters(self) -> Dict[str, Any]:
        """Get current filter configuration.
        
        Returns:
            Dictionary of filter settings
        """
        filters = {}
        
        # Entity type
        entity_type = self.type_combo.currentData()
        if entity_type:
            filters['entity_type'] = entity_type
        
        # Location
        if self.location_enabled.isChecked():
            location_id = self.location_combo.currentData()
            if location_id:
                filters['location_id'] = location_id
                filters['include_sublocations'] = self.include_sublocation.isChecked()
        
        # Species
        if self.species_enabled.isChecked():
            species_id = self.species_combo.currentData()
            if species_id:
                filters['species_id'] = species_id
        
        # Date/Timeline
        if self.date_enabled.isChecked():
            timeline_id = self.timeline_combo.currentData()
            if timeline_id:
                filters['timeline_id'] = timeline_id
            
            date_from = self.date_from.text().strip()
            if date_from:
                filters['date_from'] = date_from
            
            date_to = self.date_to.text().strip()
            if date_to:
                filters['date_to'] = date_to
        
        return filters
    
    def clear_filters(self):
        """Clear all filter settings."""
        self.type_combo.setCurrentIndex(0)
        self.location_enabled.setChecked(False)
        self.location_combo.setCurrentIndex(0)
        self.include_sublocation.setChecked(True)
        self.species_enabled.setChecked(False)
        self.species_combo.setCurrentIndex(0)
        self.date_enabled.setChecked(False)
        self.timeline_combo.setCurrentIndex(0)
        self.date_from.clear()
        self.date_to.clear()
    
    def load_locations(self, locations: list):
        """Load locations into combo box.
        
        Args:
            locations: List of Location entities
        """
        self.location_combo.clear()
        self.location_combo.addItem("Select Location...", None)
        for location in locations:
            self.location_combo.addItem(location.name, location.id)
    
    def load_species(self, species_list: list):
        """Load species into combo box.
        
        Args:
            species_list: List of Species entities
        """
        self.species_combo.clear()
        self.species_combo.addItem("Select Species...", None)
        for species in species_list:
            self.species_combo.addItem(species.name, species.id)
    
    def load_timelines(self, timelines: list):
        """Load timelines into combo box.
        
        Args:
            timelines: List of Timeline entities
        """
        self.timeline_combo.clear()
        self.timeline_combo.addItem("Select Timeline...", None)
        for timeline in timelines:
            self.timeline_combo.addItem(timeline.name, timeline.id)

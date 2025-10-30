"""Recent universes widget."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, 
                             QListWidgetItem, QPushButton)
from PyQt6.QtCore import pyqtSignal, Qt
from worldbuilder.models.universe import Universe
from typing import List
import json
from pathlib import Path


class RecentUniversesWidget(QWidget):
    """Widget displaying recently opened universes."""
    
    universe_selected = pyqtSignal(int)  # Emits universe ID
    
    MAX_RECENT = 10
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._recent_ids = []
        self._load_recent_from_settings()
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Recent Universes")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px 0;")
        layout.addWidget(title_label)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(200)
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        # Clear button
        button_layout = QVBoxLayout()
        self.clear_button = QPushButton("Clear History")
        self.clear_button.clicked.connect(self._on_clear_clicked)
        self.clear_button.setMaximumWidth(120)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)
    
    def update_recent(self, universes: List[Universe]):
        """Update the recent universes list.
        
        Args:
            universes: All universes to filter against recent IDs
        """
        self.list_widget.clear()
        
        # Create a map of universe ID to universe object
        universe_map = {u.id: u for u in universes}
        
        # Add recent universes that still exist
        valid_recent = []
        for universe_id in self._recent_ids:
            if universe_id in universe_map:
                universe = universe_map[universe_id]
                valid_recent.append(universe_id)
                
                item = QListWidgetItem(universe.name)
                item.setData(Qt.ItemDataRole.UserRole, universe.id)
                
                # Add metadata as tooltip
                tooltip = f"Author: {universe.author or 'Not specified'}\n"
                tooltip += f"Genre: {universe.genre or 'Not specified'}"
                item.setToolTip(tooltip)
                
                self.list_widget.addItem(item)
        
        # Update recent IDs to only include valid ones
        if len(valid_recent) != len(self._recent_ids):
            self._recent_ids = valid_recent
            self._save_recent_to_settings()
        
        # Show/hide clear button
        self.clear_button.setEnabled(len(valid_recent) > 0)
        
        # Show empty message if no recent universes
        if len(valid_recent) == 0:
            item = QListWidgetItem("No recent universes")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            item.setForeground(Qt.GlobalColor.gray)
            self.list_widget.addItem(item)
    
    def add_recent(self, universe_id: int):
        """Add a universe to recent list.
        
        Args:
            universe_id: ID of universe to add
        """
        # Remove if already in list
        if universe_id in self._recent_ids:
            self._recent_ids.remove(universe_id)
        
        # Add to front
        self._recent_ids.insert(0, universe_id)
        
        # Trim to max size
        if len(self._recent_ids) > self.MAX_RECENT:
            self._recent_ids = self._recent_ids[:self.MAX_RECENT]
        
        self._save_recent_to_settings()
    
    def _on_item_double_clicked(self, item: QListWidgetItem):
        """Handle item double click."""
        universe_id = item.data(Qt.ItemDataRole.UserRole)
        if universe_id:
            self.universe_selected.emit(universe_id)
    
    def _on_clear_clicked(self):
        """Handle clear button click."""
        self._recent_ids = []
        self.list_widget.clear()
        self._save_recent_to_settings()
        
        # Show empty message
        item = QListWidgetItem("No recent universes")
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        item.setForeground(Qt.GlobalColor.gray)
        self.list_widget.addItem(item)
        
        self.clear_button.setEnabled(False)
    
    def _get_settings_file(self) -> Path:
        """Get path to settings file."""
        app_data_dir = Path.home() / ".worldbuilder"
        app_data_dir.mkdir(exist_ok=True)
        return app_data_dir / "recent.json"
    
    def _load_recent_from_settings(self):
        """Load recent universes from settings file."""
        settings_file = self._get_settings_file()
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    data = json.load(f)
                    self._recent_ids = data.get('recent_universe_ids', [])
            except (json.JSONDecodeError, IOError):
                self._recent_ids = []
    
    def _save_recent_to_settings(self):
        """Save recent universes to settings file."""
        settings_file = self._get_settings_file()
        try:
            with open(settings_file, 'w') as f:
                json.dump({'recent_universe_ids': self._recent_ids}, f)
        except IOError:
            pass

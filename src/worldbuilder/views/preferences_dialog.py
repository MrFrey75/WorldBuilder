"""
User Preferences Dialog
Allows configuration of application settings, theme, and keyboard shortcuts
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QWidget, QLabel, QComboBox, QPushButton,
                             QCheckBox, QSpinBox, QGroupBox, QFormLayout,
                             QKeySequenceEdit, QListWidget, QListWidgetItem,
                             QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence
import json
from pathlib import Path


class PreferencesDialog(QDialog):
    """Dialog for managing application preferences"""
    
    preferences_changed = pyqtSignal(dict)
    
    def __init__(self, current_preferences=None, parent=None):
        super().__init__(parent)
        self.preferences = current_preferences or self._default_preferences()
        self.setup_ui()
        self.load_preferences()
        
    def _default_preferences(self):
        """Get default preferences"""
        return {
            'theme': 'light',
            'auto_save': True,
            'auto_save_interval': 5,
            'show_tooltips': True,
            'confirm_delete': True,
            'recent_files_limit': 10,
            'font_size': 11,
            'enable_spell_check': True,
            'shortcuts': {
                'new_universe': 'Ctrl+N',
                'open_universe': 'Ctrl+O',
                'save': 'Ctrl+S',
                'search': 'Ctrl+F',
                'new_location': 'Ctrl+Shift+L',
                'new_figure': 'Ctrl+Shift+F',
                'new_species': 'Ctrl+Shift+S',
                'new_event': 'Ctrl+Shift+E',
            }
        }
        
    def setup_ui(self):
        """Set up the dialog UI"""
        self.setWindowTitle("Preferences")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Tab widget for different preference categories
        self.tab_widget = QTabWidget()
        
        # General tab
        general_tab = self.create_general_tab()
        self.tab_widget.addTab(general_tab, "General")
        
        # Appearance tab
        appearance_tab = self.create_appearance_tab()
        self.tab_widget.addTab(appearance_tab, "Appearance")
        
        # Editor tab
        editor_tab = self.create_editor_tab()
        self.tab_widget.addTab(editor_tab, "Editor")
        
        # Shortcuts tab
        shortcuts_tab = self.create_shortcuts_tab()
        self.tab_widget.addTab(shortcuts_tab, "Keyboard Shortcuts")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.restore_defaults_btn = QPushButton("Restore Defaults")
        self.restore_defaults_btn.clicked.connect(self.restore_defaults)
        button_layout.addWidget(self.restore_defaults_btn)
        
        button_layout.addStretch()
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept_preferences)
        button_layout.addWidget(self.ok_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.apply_preferences)
        button_layout.addWidget(self.apply_btn)
        
        layout.addLayout(button_layout)
        
    def create_general_tab(self):
        """Create the general preferences tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Auto-save group
        auto_save_group = QGroupBox("Auto-Save")
        auto_save_layout = QFormLayout()
        
        self.auto_save_check = QCheckBox("Enable auto-save")
        auto_save_layout.addRow("", self.auto_save_check)
        
        self.auto_save_interval_spin = QSpinBox()
        self.auto_save_interval_spin.setRange(1, 60)
        self.auto_save_interval_spin.setSuffix(" minutes")
        auto_save_layout.addRow("Save interval:", self.auto_save_interval_spin)
        
        auto_save_group.setLayout(auto_save_layout)
        layout.addWidget(auto_save_group)
        
        # Confirmation group
        confirm_group = QGroupBox("Confirmations")
        confirm_layout = QVBoxLayout()
        
        self.confirm_delete_check = QCheckBox("Confirm before deleting entities")
        confirm_layout.addWidget(self.confirm_delete_check)
        
        confirm_group.setLayout(confirm_layout)
        layout.addWidget(confirm_group)
        
        # Recent files group
        recent_group = QGroupBox("Recent Files")
        recent_layout = QFormLayout()
        
        self.recent_files_spin = QSpinBox()
        self.recent_files_spin.setRange(5, 50)
        recent_layout.addRow("Maximum recent files:", self.recent_files_spin)
        
        recent_group.setLayout(recent_layout)
        layout.addWidget(recent_group)
        
        layout.addStretch()
        return widget
        
    def create_appearance_tab(self):
        """Create the appearance preferences tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Theme group
        theme_group = QGroupBox("Theme")
        theme_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        theme_layout.addRow("Application theme:", self.theme_combo)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Font group
        font_group = QGroupBox("Font")
        font_layout = QFormLayout()
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setSuffix(" pt")
        font_layout.addRow("Font size:", self.font_size_spin)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # UI group
        ui_group = QGroupBox("User Interface")
        ui_layout = QVBoxLayout()
        
        self.tooltips_check = QCheckBox("Show tooltips")
        ui_layout.addWidget(self.tooltips_check)
        
        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)
        
        layout.addStretch()
        return widget
        
    def create_editor_tab(self):
        """Create the editor preferences tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Editor features group
        features_group = QGroupBox("Editor Features")
        features_layout = QVBoxLayout()
        
        self.spell_check_check = QCheckBox("Enable spell checking")
        features_layout.addWidget(self.spell_check_check)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        layout.addStretch()
        return widget
        
    def create_shortcuts_tab(self):
        """Create the keyboard shortcuts tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Double-click a shortcut to edit it")
        info_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(info_label)
        
        # Shortcuts list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        shortcuts_widget = QWidget()
        shortcuts_layout = QFormLayout(shortcuts_widget)
        
        self.shortcut_edits = {}
        
        shortcut_labels = {
            'new_universe': 'New Universe',
            'open_universe': 'Open Universe',
            'save': 'Save',
            'search': 'Search',
            'new_location': 'New Location',
            'new_figure': 'New Figure',
            'new_species': 'New Species',
            'new_event': 'New Event',
        }
        
        for key, label in shortcut_labels.items():
            edit = QKeySequenceEdit()
            self.shortcut_edits[key] = edit
            shortcuts_layout.addRow(f"{label}:", edit)
            
        scroll.setWidget(shortcuts_widget)
        layout.addWidget(scroll)
        
        return widget
        
    def load_preferences(self):
        """Load current preferences into UI"""
        # General tab
        self.auto_save_check.setChecked(self.preferences.get('auto_save', True))
        self.auto_save_interval_spin.setValue(self.preferences.get('auto_save_interval', 5))
        self.confirm_delete_check.setChecked(self.preferences.get('confirm_delete', True))
        self.recent_files_spin.setValue(self.preferences.get('recent_files_limit', 10))
        
        # Appearance tab
        theme = self.preferences.get('theme', 'light')
        self.theme_combo.setCurrentText(theme.capitalize())
        self.font_size_spin.setValue(self.preferences.get('font_size', 11))
        self.tooltips_check.setChecked(self.preferences.get('show_tooltips', True))
        
        # Editor tab
        self.spell_check_check.setChecked(self.preferences.get('enable_spell_check', True))
        
        # Shortcuts tab
        shortcuts = self.preferences.get('shortcuts', {})
        for key, edit in self.shortcut_edits.items():
            shortcut = shortcuts.get(key, '')
            if shortcut:
                edit.setKeySequence(QKeySequence(shortcut))
                
    def get_preferences(self):
        """Get current preferences from UI"""
        preferences = {
            'theme': self.theme_combo.currentText().lower(),
            'auto_save': self.auto_save_check.isChecked(),
            'auto_save_interval': self.auto_save_interval_spin.value(),
            'show_tooltips': self.tooltips_check.isChecked(),
            'confirm_delete': self.confirm_delete_check.isChecked(),
            'recent_files_limit': self.recent_files_spin.value(),
            'font_size': self.font_size_spin.value(),
            'enable_spell_check': self.spell_check_check.isChecked(),
            'shortcuts': {}
        }
        
        # Get shortcuts
        for key, edit in self.shortcut_edits.items():
            sequence = edit.keySequence()
            if not sequence.isEmpty():
                preferences['shortcuts'][key] = sequence.toString()
                
        return preferences
        
    def apply_preferences(self):
        """Apply preferences without closing"""
        self.preferences = self.get_preferences()
        self.preferences_changed.emit(self.preferences)
        
    def accept_preferences(self):
        """Apply preferences and close"""
        self.apply_preferences()
        self.accept()
        
    def restore_defaults(self):
        """Restore default preferences"""
        reply = QMessageBox.question(
            self,
            "Restore Defaults",
            "Are you sure you want to restore default preferences?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.preferences = self._default_preferences()
            self.load_preferences()


class PreferencesManager:
    """Manages loading and saving of user preferences"""
    
    def __init__(self, config_path=None):
        """
        Initialize preferences manager
        
        Args:
            config_path: Path to config file (default: ~/.worldbuilder/preferences.json)
        """
        if config_path is None:
            config_dir = Path.home() / ".worldbuilder"
            config_dir.mkdir(exist_ok=True)
            config_path = config_dir / "preferences.json"
            
        self.config_path = Path(config_path)
        self.preferences = self.load_preferences()
        
    def load_preferences(self):
        """Load preferences from file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading preferences: {e}")
                
        # Return defaults if file doesn't exist or error occurred
        return PreferencesDialog()._default_preferences()
        
    def save_preferences(self, preferences):
        """Save preferences to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(preferences, f, indent=2)
            self.preferences = preferences
            return True
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False
            
    def get_preference(self, key, default=None):
        """Get a specific preference value"""
        return self.preferences.get(key, default)
        
    def set_preference(self, key, value):
        """Set a specific preference value"""
        self.preferences[key] = value
        self.save_preferences(self.preferences)

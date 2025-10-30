"""Universe settings dialog."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QTextEdit, QPushButton, QLabel, 
                             QComboBox, QCheckBox, QGroupBox, QSpinBox)
from PyQt6.QtCore import Qt
from worldbuilder.models.universe import Universe


class UniverseSettingsDialog(QDialog):
    """Dialog for configuring universe-specific settings."""
    
    def __init__(self, parent=None, universe: Universe = None):
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
            universe: Universe to configure settings for
        """
        super().__init__(parent)
        self.universe = universe
        
        self.setWindowTitle(f"Settings - {universe.name if universe else 'Universe'}")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self._setup_ui()
        
        if self.universe:
            self._load_settings()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Calendar System Group
        calendar_group = QGroupBox("Calendar System")
        calendar_layout = QFormLayout()
        
        self.calendar_type_combo = QComboBox()
        self.calendar_type_combo.addItems([
            "Gregorian (Earth Standard)",
            "Custom Calendar",
            "No Calendar System"
        ])
        calendar_layout.addRow("Calendar Type:", self.calendar_type_combo)
        
        self.days_per_week_spin = QSpinBox()
        self.days_per_week_spin.setRange(1, 20)
        self.days_per_week_spin.setValue(7)
        calendar_layout.addRow("Days per Week:", self.days_per_week_spin)
        
        self.months_per_year_spin = QSpinBox()
        self.months_per_year_spin.setRange(1, 30)
        self.months_per_year_spin.setValue(12)
        calendar_layout.addRow("Months per Year:", self.months_per_year_spin)
        
        self.days_per_year_spin = QSpinBox()
        self.days_per_year_spin.setRange(1, 1000)
        self.days_per_year_spin.setValue(365)
        calendar_layout.addRow("Days per Year:", self.days_per_year_spin)
        
        calendar_group.setLayout(calendar_layout)
        layout.addWidget(calendar_group)
        
        # Timeline Settings Group
        timeline_group = QGroupBox("Timeline Settings")
        timeline_layout = QFormLayout()
        
        self.timeline_unit_combo = QComboBox()
        self.timeline_unit_combo.addItems([
            "Standard Years",
            "Custom Era System",
            "Before/After Event"
        ])
        timeline_layout.addRow("Timeline Unit:", self.timeline_unit_combo)
        
        self.enable_negative_dates = QCheckBox("Allow dates before year 0")
        self.enable_negative_dates.setChecked(True)
        timeline_layout.addRow("", self.enable_negative_dates)
        
        timeline_group.setLayout(timeline_layout)
        layout.addWidget(timeline_group)
        
        # Display Settings Group
        display_group = QGroupBox("Display Settings")
        display_layout = QFormLayout()
        
        self.show_entity_count = QCheckBox("Show entity counts")
        self.show_entity_count.setChecked(True)
        display_layout.addRow("", self.show_entity_count)
        
        self.default_sort_combo = QComboBox()
        self.default_sort_combo.addItems([
            "Name (A-Z)",
            "Name (Z-A)",
            "Date Created (Newest)",
            "Date Created (Oldest)",
            "Last Modified"
        ])
        display_layout.addRow("Default Sort:", self.default_sort_combo)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # Data Management Group
        data_group = QGroupBox("Data Management")
        data_layout = QFormLayout()
        
        self.auto_backup = QCheckBox("Enable automatic backups")
        self.auto_backup.setChecked(False)
        data_layout.addRow("", self.auto_backup)
        
        self.backup_frequency_spin = QSpinBox()
        self.backup_frequency_spin.setRange(1, 30)
        self.backup_frequency_spin.setValue(7)
        self.backup_frequency_spin.setSuffix(" days")
        self.backup_frequency_spin.setEnabled(False)
        data_layout.addRow("Backup Every:", self.backup_frequency_spin)
        
        self.auto_backup.stateChanged.connect(
            lambda: self.backup_frequency_spin.setEnabled(self.auto_backup.isChecked())
        )
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        # Notes section
        notes_group = QGroupBox("Notes")
        notes_layout = QVBoxLayout()
        
        note_label = QLabel("Note: These settings are currently for demonstration purposes.\n"
                           "Full functionality will be implemented in future phases.")
        note_label.setStyleSheet("color: gray; font-style: italic;")
        note_label.setWordWrap(True)
        notes_layout.addWidget(note_label)
        
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)
        
        layout.addStretch()
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.save_button.setDefault(True)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
    
    def _load_settings(self):
        """Load settings for the current universe."""
        # For now, just use defaults
        # In future phases, settings will be stored in database
        pass
    
    def get_settings(self) -> dict:
        """Get the current settings as a dictionary.
        
        Returns:
            Dictionary with settings
        """
        return {
            'calendar_type': self.calendar_type_combo.currentText(),
            'days_per_week': self.days_per_week_spin.value(),
            'months_per_year': self.months_per_year_spin.value(),
            'days_per_year': self.days_per_year_spin.value(),
            'timeline_unit': self.timeline_unit_combo.currentText(),
            'enable_negative_dates': self.enable_negative_dates.isChecked(),
            'show_entity_count': self.show_entity_count.isChecked(),
            'default_sort': self.default_sort_combo.currentText(),
            'auto_backup': self.auto_backup.isChecked(),
            'backup_frequency_days': self.backup_frequency_spin.value()
        }

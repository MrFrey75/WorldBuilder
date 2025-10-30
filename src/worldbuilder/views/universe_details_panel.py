"""Universe details panel widget."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QScrollArea, QFrame, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from worldbuilder.models.universe import Universe
from datetime import datetime


class UniverseDetailsPanel(QWidget):
    """Widget displaying detailed information about a selected universe."""
    
    edit_requested = pyqtSignal(int)  # Emits universe ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_universe = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Scroll area for details
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Container widget
        container = QWidget()
        container_layout = QVBoxLayout(container)
        
        # Title
        title_label = QLabel("Universe Details")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px 0;")
        container_layout.addWidget(title_label)
        
        # Empty state
        self.empty_label = QLabel("No universe selected")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("color: gray; padding: 20px;")
        container_layout.addWidget(self.empty_label)
        
        # Details container (hidden initially)
        self.details_widget = QWidget()
        details_layout = QVBoxLayout(self.details_widget)
        details_layout.setSpacing(15)
        
        # Basic Information Group
        basic_group = QGroupBox("Basic Information")
        basic_layout = QVBoxLayout()
        
        self.name_label = self._create_info_row("Name:", "")
        self.author_label = self._create_info_row("Author:", "")
        self.genre_label = self._create_info_row("Genre:", "")
        self.status_label = self._create_info_row("Status:", "")
        
        basic_layout.addWidget(self.name_label[0])
        basic_layout.addWidget(self.author_label[0])
        basic_layout.addWidget(self.genre_label[0])
        basic_layout.addWidget(self.status_label[0])
        basic_group.setLayout(basic_layout)
        details_layout.addWidget(basic_group)
        
        # Description Group
        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout()
        
        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.description_label.setStyleSheet("padding: 5px;")
        desc_layout.addWidget(self.description_label)
        desc_group.setLayout(desc_layout)
        details_layout.addWidget(desc_group)
        
        # Metadata Group
        meta_group = QGroupBox("Metadata")
        meta_layout = QVBoxLayout()
        
        self.id_label = self._create_info_row("ID:", "")
        self.created_label = self._create_info_row("Created:", "")
        self.updated_label = self._create_info_row("Updated:", "")
        
        meta_layout.addWidget(self.id_label[0])
        meta_layout.addWidget(self.created_label[0])
        meta_layout.addWidget(self.updated_label[0])
        meta_group.setLayout(meta_layout)
        details_layout.addWidget(meta_group)
        
        details_layout.addStretch()
        self.details_widget.setVisible(False)
        container_layout.addWidget(self.details_widget)
        
        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)
    
    def _create_info_row(self, label_text: str, value_text: str):
        """Create an information row with label and value."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 2, 0, 2)
        
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; min-width: 80px;")
        
        value = QLabel(value_text)
        value.setWordWrap(True)
        value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        layout.addWidget(label)
        layout.addWidget(value, 1)
        
        return (container, label, value)
    
    def set_universe(self, universe: Universe):
        """Display details for the given universe."""
        self._current_universe = universe
        
        if universe is None:
            self.empty_label.setVisible(True)
            self.details_widget.setVisible(False)
            return
        
        self.empty_label.setVisible(False)
        self.details_widget.setVisible(True)
        
        # Update basic info
        self.name_label[2].setText(universe.name)
        self.author_label[2].setText(universe.author or "Not specified")
        self.genre_label[2].setText(universe.genre or "Not specified")
        self.status_label[2].setText("Active" if universe.is_active else "Inactive")
        
        # Update description
        if universe.description:
            self.description_label.setText(universe.description)
        else:
            self.description_label.setText("<i>No description provided</i>")
        
        # Update metadata
        self.id_label[2].setText(str(universe.id))
        self.created_label[2].setText(self._format_datetime(universe.created_at))
        self.updated_label[2].setText(self._format_datetime(universe.updated_at))
    
    def clear(self):
        """Clear the details panel."""
        self.set_universe(None)
    
    def _format_datetime(self, dt: datetime) -> str:
        """Format datetime for display."""
        if dt is None:
            return "Unknown"
        return dt.strftime("%Y-%m-%d %H:%M:%S")

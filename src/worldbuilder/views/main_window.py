"""Main application window."""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMenuBar, QMenu, QStatusBar, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction
from worldbuilder.utils import ThemeManager, Theme


class MainWindow(QMainWindow):
    """Main application window."""
    
    # Signals
    theme_changed = pyqtSignal(Theme)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WorldBuilder")
        self.setGeometry(100, 100, 1200, 800)
        
        self._setup_ui()
        self._create_menu_bar()
        self._create_status_bar()
    
    def _setup_ui(self):
        """Set up the main UI components."""
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Placeholder label
        placeholder = QLabel("Welcome to WorldBuilder")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 24px; color: gray;")
        self.main_layout.addWidget(placeholder)
    
    def _create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Universe", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open Universe", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        preferences_action = QAction("&Preferences", self)
        preferences_action.setShortcut("Ctrl+,")
        edit_menu.addAction(preferences_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        # Theme submenu
        theme_menu = view_menu.addMenu("&Theme")
        
        light_theme_action = QAction("&Light", self)
        light_theme_action.triggered.connect(lambda: self.theme_changed.emit(Theme.LIGHT))
        theme_menu.addAction(light_theme_action)
        
        dark_theme_action = QAction("&Dark", self)
        dark_theme_action.triggered.connect(lambda: self.theme_changed.emit(Theme.DARK))
        theme_menu.addAction(dark_theme_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        help_menu.addAction(about_action)
    
    def _create_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def set_status_message(self, message: str):
        """Set status bar message.
        
        Args:
            message: Message to display
        """
        self.status_bar.showMessage(message)

"""Main entry point for WorldBuilder application."""
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from worldbuilder.views import MainWindow
from worldbuilder.utils import ThemeManager, Theme
from worldbuilder.database import DatabaseManager


class WorldBuilderApp:
    """WorldBuilder application class."""
    
    def __init__(self):
        """Initialize the application."""
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("WorldBuilder")
        self.app.setOrganizationName("WorldBuilder")
        
        # Initialize database
        self.db_manager = None
        self._setup_database()
        
        # Create main window
        self.main_window = MainWindow()
        
        # Connect signals
        self.main_window.theme_changed.connect(self._on_theme_changed)
        
        # Apply default theme
        ThemeManager.apply_theme(self.app, Theme.LIGHT)
    
    def _setup_database(self):
        """Set up database connection."""
        # Use application data directory for database
        app_data_dir = Path.home() / ".worldbuilder"
        app_data_dir.mkdir(exist_ok=True)
        
        db_path = app_data_dir / "worldbuilder.db"
        self.db_manager = DatabaseManager(str(db_path))
        self.db_manager.create_tables()
    
    def _on_theme_changed(self, theme: Theme):
        """Handle theme change event.
        
        Args:
            theme: New theme to apply
        """
        ThemeManager.apply_theme(self.app, theme)
        self.main_window.set_status_message(f"Theme changed to {theme.value}")
    
    def run(self):
        """Run the application."""
        self.main_window.show()
        return self.app.exec()


def main():
    """Main entry point."""
    app = WorldBuilderApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()

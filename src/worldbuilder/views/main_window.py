"""Main application window."""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QMenuBar, QMenu, QStatusBar, QLabel, 
                             QMessageBox, QDialog)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction
from worldbuilder.utils import ThemeManager, Theme
from worldbuilder.views.universe_list_view import UniverseListView
from worldbuilder.views.universe_dialog import UniverseDialog
from worldbuilder.views.universe_details_panel import UniverseDetailsPanel
from worldbuilder.views.recent_universes_widget import RecentUniversesWidget
from worldbuilder.views.universe_settings_dialog import UniverseSettingsDialog
from worldbuilder.views.export_import_dialog import ExportDialog, ImportDialog
from worldbuilder.views.backup_dialog import BackupDialog
from worldbuilder.services import UniverseService
from worldbuilder.services.export_import_service import ExportImportService
from worldbuilder.services.backup_service import BackupService
from worldbuilder.database import DatabaseManager


class MainWindow(QMainWindow):
    """Main application window."""
    
    # Signals
    theme_changed = pyqtSignal(Theme)
    universe_opened = pyqtSignal(int)  # Emits universe ID
    
    def __init__(self, universe_service: UniverseService = None, db_manager: DatabaseManager = None):
        super().__init__()
        self.universe_service = universe_service
        self.db_manager = db_manager
        self.setWindowTitle("WorldBuilder")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize services
        self.export_import_service = None
        self.backup_service = None
        if db_manager:
            self.export_import_service = ExportImportService(db_manager.session)
            self.backup_service = BackupService(db_manager.db_path)
        
        self._setup_ui()
        self._create_menu_bar()
        self._create_status_bar()
        
        # Load universes if service is available
        if self.universe_service:
            self._load_universes()
    
    def _setup_ui(self):
        """Set up the main UI components."""
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Recent universes widget
        self.recent_widget = RecentUniversesWidget()
        self.recent_widget.universe_selected.connect(self._on_open_universe)
        self.main_layout.addWidget(self.recent_widget)
        
        # Splitter for list and details
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Universe list view
        self.universe_list_view = UniverseListView()
        self.universe_list_view.create_requested.connect(self._on_create_universe)
        self.universe_list_view.edit_requested.connect(self._on_edit_universe)
        self.universe_list_view.delete_requested.connect(self._on_delete_universe)
        self.universe_list_view.open_requested.connect(self._on_open_universe)
        self.universe_list_view.universe_selected.connect(self._on_universe_selected)
        splitter.addWidget(self.universe_list_view)
        
        # Universe details panel
        self.details_panel = UniverseDetailsPanel()
        self.details_panel.edit_requested.connect(self._on_edit_universe)
        splitter.addWidget(self.details_panel)
        
        # Set splitter proportions (2:1 ratio)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        self.main_layout.addWidget(splitter)
    
    def _create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Universe", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._on_create_universe)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open Universe", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._on_open_selected_universe)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # Export/Import submenu
        export_import_menu = file_menu.addMenu("Export/Import")
        
        export_action = QAction("&Export Universe...", self)
        export_action.setShortcut("Ctrl+Shift+E")
        export_action.triggered.connect(self._on_export_universe)
        export_import_menu.addAction(export_action)
        
        import_action = QAction("&Import Universe...", self)
        import_action.setShortcut("Ctrl+Shift+I")
        import_action.triggered.connect(self._on_import_universe)
        export_import_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        # Backup submenu
        backup_menu = file_menu.addMenu("Backup")
        
        create_backup_action = QAction("&Create Backup...", self)
        create_backup_action.setShortcut("Ctrl+B")
        create_backup_action.triggered.connect(self._on_create_backup)
        backup_menu.addAction(create_backup_action)
        
        manage_backups_action = QAction("&Manage Backups...", self)
        manage_backups_action.triggered.connect(self._on_manage_backups)
        backup_menu.addAction(manage_backups_action)
        
        file_menu.addSeparator()
        
        refresh_action = QAction("&Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._load_universes)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        edit_universe_action = QAction("&Edit Universe", self)
        edit_universe_action.setShortcut("Ctrl+E")
        edit_universe_action.triggered.connect(self._on_edit_selected_universe)
        edit_menu.addAction(edit_universe_action)
        
        delete_universe_action = QAction("&Delete Universe", self)
        delete_universe_action.setShortcut("Delete")
        delete_universe_action.triggered.connect(self._on_delete_selected_universe)
        edit_menu.addAction(delete_universe_action)
        
        edit_menu.addSeparator()
        
        settings_action = QAction("Universe &Settings", self)
        settings_action.setShortcut("Ctrl+Shift+S")
        settings_action.triggered.connect(self._on_universe_settings)
        edit_menu.addAction(settings_action)
        
        edit_menu.addSeparator()
        
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
        about_action.triggered.connect(self._show_about)
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
    
    def _load_universes(self):
        """Load universes from database."""
        if not self.universe_service:
            return
        
        try:
            universes = self.universe_service.get_all_universes()
            self.universe_list_view.load_universes(universes)
            self.recent_widget.update_recent(universes)
            self.set_status_message(f"Loaded {len(universes)} universe(s)")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load universes: {str(e)}")
    
    def _on_create_universe(self):
        """Handle create universe request."""
        if not self.universe_service:
            return
        
        dialog = UniverseDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                universe = self.universe_service.create_universe(**data)
                self._load_universes()
                self.set_status_message(f"Created universe: {universe.name}")
            except ValueError as e:
                QMessageBox.warning(self, "Validation Error", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create universe: {str(e)}")
    
    def _on_edit_universe(self, universe_id: int):
        """Handle edit universe request."""
        if not self.universe_service:
            return
        
        universe = self.universe_service.get_universe(universe_id)
        if not universe:
            QMessageBox.warning(self, "Error", "Universe not found")
            return
        
        dialog = UniverseDialog(self, universe)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                self.universe_service.update_universe(universe_id, **data)
                self._load_universes()
                self.set_status_message(f"Updated universe: {data['name']}")
            except ValueError as e:
                QMessageBox.warning(self, "Validation Error", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update universe: {str(e)}")
    
    def _on_edit_selected_universe(self):
        """Handle edit selected universe from menu."""
        universe_id = self.universe_list_view.get_selected_universe_id()
        if universe_id:
            self._on_edit_universe(universe_id)
    
    def _on_delete_universe(self, universe_id: int):
        """Handle delete universe request."""
        if not self.universe_service:
            return
        
        universe = self.universe_service.get_universe(universe_id)
        if not universe:
            return
        
        reply = QMessageBox.question(
            self, 
            "Confirm Delete",
            f"Are you sure you want to delete universe '{universe.name}'?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.universe_service.delete_universe(universe_id)
                self._load_universes()
                self.set_status_message(f"Deleted universe: {universe.name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete universe: {str(e)}")
    
    def _on_delete_selected_universe(self):
        """Handle delete selected universe from menu."""
        universe_id = self.universe_list_view.get_selected_universe_id()
        if universe_id:
            self._on_delete_universe(universe_id)
    
    def _on_open_universe(self, universe_id: int):
        """Handle open universe request."""
        if not self.universe_service:
            return
        
        try:
            self.universe_service.set_active_universe(universe_id)
            universe = self.universe_service.get_universe(universe_id)
            self._load_universes()
            self.recent_widget.add_recent(universe_id)
            self.set_status_message(f"Opened universe: {universe.name}")
            self.universe_opened.emit(universe_id)
            
            # TODO: Switch to universe workspace view
            QMessageBox.information(
                self,
                "Universe Opened",
                f"Universe '{universe.name}' is now active.\n\nFull workspace functionality will be available in Phase 3+."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open universe: {str(e)}")
    
    def _on_open_selected_universe(self):
        """Handle open selected universe from menu."""
        universe_id = self.universe_list_view.get_selected_universe_id()
        if universe_id:
            self._on_open_universe(universe_id)
        else:
            QMessageBox.information(self, "No Selection", "Please select a universe to open.")
    
    def _on_universe_selected(self, universe_id: int):
        """Handle universe selection in list.
        
        Args:
            universe_id: ID of selected universe
        """
        if not self.universe_service:
            return
        
        universe = self.universe_service.get_universe(universe_id)
        self.details_panel.set_universe(universe)
    
    def _on_universe_settings(self):
        """Handle universe settings menu action."""
        universe_id = self.universe_list_view.get_selected_universe_id()
        if not universe_id:
            QMessageBox.information(self, "No Selection", "Please select a universe to configure settings.")
            return
        
        if not self.universe_service:
            return
        
        universe = self.universe_service.get_universe(universe_id)
        if not universe:
            return
        
        dialog = UniverseSettingsDialog(self, universe)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            # TODO: Save settings to database in future phases
            self.set_status_message(f"Settings saved for: {universe.name}")
            QMessageBox.information(
                self,
                "Settings Saved",
                "Universe settings have been configured.\n\nNote: Full settings persistence will be implemented in future phases."
            )
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About WorldBuilder",
            "<h3>WorldBuilder v0.1.0</h3>"
            "<p>A comprehensive worldbuilding and universe creation tool.</p>"
            "<p>Phase 13 Complete - Data Management (Export/Import & Backup/Restore)</p>"
            "<p>© 2025 WorldBuilder Team</p>"
        )
    
    def _on_export_universe(self):
        """Handle export universe menu action."""
        universe_id = self.universe_list_view.get_selected_universe_id()
        if not universe_id:
            QMessageBox.information(self, "No Selection", "Please select a universe to export.")
            return
        
        if not self.export_import_service or not self.universe_service:
            QMessageBox.warning(self, "Service Unavailable", "Export service is not available.")
            return
        
        universe = self.universe_service.get_universe(universe_id)
        if not universe:
            return
        
        dialog = ExportDialog(self, universe.name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_export_settings()
            
            if not settings["output_path"]:
                QMessageBox.warning(self, "No Output File", "Please specify an output file.")
                return
            
            try:
                stats = self.export_import_service.export_universe(
                    universe_id=universe_id,
                    output_path=settings["output_path"],
                    selective=settings["selective"],
                    entity_types=settings.get("entity_types")
                )
                
                QMessageBox.information(
                    self,
                    "Export Complete",
                    f"Universe exported successfully!\n\n"
                    f"Total entities: {stats['total_entities']}\n"
                    f"File size: {stats['file_size'] / 1024:.1f} KB\n"
                    f"Output: {stats['output_file']}"
                )
                self.set_status_message(f"Exported {universe.name}")
                
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Error exporting universe: {str(e)}")
    
    def _on_import_universe(self):
        """Handle import universe menu action."""
        if not self.export_import_service:
            QMessageBox.warning(self, "Service Unavailable", "Import service is not available.")
            return
        
        dialog = ImportDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_import_settings()
            
            if not settings["input_path"]:
                QMessageBox.warning(self, "No Input File", "Please specify an input file.")
                return
            
            try:
                stats = self.export_import_service.import_universe(
                    input_path=settings["input_path"],
                    create_new=settings["create_new"]
                )
                
                QMessageBox.information(
                    self,
                    "Import Complete",
                    f"Universe imported successfully!\n\n"
                    f"Total entities: {stats['total_entities']}\n"
                    f"Skipped: {stats.get('skipped', 0)}\n"
                    f"Errors: {len(stats.get('errors', []))}"
                )
                self.set_status_message("Universe imported")
                self._load_universes()  # Refresh the list
                
            except Exception as e:
                QMessageBox.critical(self, "Import Failed", f"Error importing universe: {str(e)}")
    
    def _on_create_backup(self):
        """Handle create backup menu action."""
        if not self.backup_service:
            QMessageBox.warning(self, "Service Unavailable", "Backup service is not available.")
            return
        
        dialog = BackupDialog(self, self.backup_service)
        dialog.exec()
    
    def _on_manage_backups(self):
        """Handle manage backups menu action."""
        if not self.backup_service:
            QMessageBox.warning(self, "Service Unavailable", "Backup service is not available.")
            return
        
        dialog = BackupDialog(self, self.backup_service)
        dialog.exec()

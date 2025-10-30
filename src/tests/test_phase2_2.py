"""Test Phase 2.2 UI components."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from worldbuilder.database import DatabaseManager, UniverseRepository
from worldbuilder.services import UniverseService
from worldbuilder.models import Universe


def test_recent_universes_persistence():
    """Test recent universes persistence."""
    from worldbuilder.views import RecentUniversesWidget
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\nTesting Recent Universes Widget...")
    
    # Create widget
    widget = RecentUniversesWidget()
    
    # Add some recent IDs
    widget.add_recent(1)
    widget.add_recent(2)
    widget.add_recent(3)
    
    assert len(widget._recent_ids) == 3
    assert widget._recent_ids[0] == 3  # Most recent first
    print("✓ Recent universes tracking works")
    
    # Test max limit
    for i in range(4, 15):
        widget.add_recent(i)
    
    assert len(widget._recent_ids) <= widget.MAX_RECENT
    print(f"✓ Recent universes limited to {widget.MAX_RECENT}")
    
    # Test clearing
    widget._on_clear_clicked()
    assert len(widget._recent_ids) == 0
    print("✓ Recent universes clearing works")


def test_universe_details_panel():
    """Test universe details panel."""
    from worldbuilder.views import UniverseDetailsPanel
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\nTesting Universe Details Panel...")
    
    # Create panel
    panel = UniverseDetailsPanel()
    
    # Test with None
    panel.set_universe(None)
    assert panel._current_universe is None
    print("✓ Empty state works")
    
    # Create test universe
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    repository = UniverseRepository(session)
    service = UniverseService(repository)
    
    universe = service.create_universe(
        name="Test Universe",
        author="Test Author",
        genre="Fantasy",
        description="Test description"
    )
    
    # Test with universe
    panel.set_universe(universe)
    assert panel._current_universe is not None
    assert panel.name_label[2].text() == "Test Universe"
    assert panel.author_label[2].text() == "Test Author"
    print("✓ Universe details display works")
    
    session.close()


def test_universe_settings_dialog():
    """Test universe settings dialog."""
    from worldbuilder.views import UniverseSettingsDialog
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\nTesting Universe Settings Dialog...")
    
    # Create test universe
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    repository = UniverseRepository(session)
    service = UniverseService(repository)
    
    universe = service.create_universe(
        name="Settings Test Universe",
        author="Test Author"
    )
    
    # Create dialog
    dialog = UniverseSettingsDialog(None, universe)
    
    # Test settings retrieval
    settings = dialog.get_settings()
    
    assert 'calendar_type' in settings
    assert 'days_per_week' in settings
    assert 'timeline_unit' in settings
    assert 'auto_backup' in settings
    
    print("✓ Settings dialog created successfully")
    print(f"✓ Default calendar: {settings['calendar_type']}")
    print(f"✓ Days per week: {settings['days_per_week']}")
    
    session.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Running WorldBuilder Phase 2.2 Tests")
    print("=" * 60)
    
    test_recent_universes_persistence()
    test_universe_details_panel()
    test_universe_settings_dialog()
    
    print("\n" + "=" * 60)
    print("✓ ALL PHASE 2.2 TESTS PASSED!")
    print("=" * 60)

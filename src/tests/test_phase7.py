"""Test Phase 7: Events & Timeline System."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from worldbuilder.database import (DatabaseManager, UniverseRepository, 
                                   EventRepository, TimelineRepository)
from worldbuilder.services import UniverseService, EventService, TimelineService
from worldbuilder.models import Event, Timeline, EventType, EventImportance, DatePrecision


def test_event_model():
    """Test Event model methods."""
    print("\nTesting Event Model...")
    
    event = Event()
    event.date_string = "Year 1000"
    event.is_instantaneous = 1
    
    assert event.get_duration_display() == "Instantaneous"
    print("   ✓ Instantaneous duration display")
    
    event.is_instantaneous = 0
    event.end_date_string = "Year 1010"
    assert "1000" in event.get_duration_display() and "1010" in event.get_duration_display()
    print("   ✓ Duration range display")
    
    # Test related entities
    event.add_related_entity("notable_figures", 1)
    event.add_related_entity("notable_figures", 2)
    event.add_related_entity("locations", 5)
    
    figures = event.get_related_entities("notable_figures")
    assert len(figures) == 2
    print("   ✓ Related entities work")
    
    event.remove_related_entity("notable_figures", 1)
    figures = event.get_related_entities("notable_figures")
    assert len(figures) == 1
    print("   ✓ Remove related entity works")


def test_timeline_model():
    """Test Timeline model methods."""
    print("\nTesting Timeline Model...")
    
    timeline = Timeline()
    timeline.event_ids = []
    
    timeline.add_event(1)
    timeline.add_event(2)
    timeline.add_event(3)
    
    event_ids = timeline.get_event_ids()
    assert len(event_ids) == 3
    print("   ✓ Add events to timeline")
    
    timeline.remove_event(2)
    event_ids = timeline.get_event_ids()
    assert len(event_ids) == 2
    assert 2 not in event_ids
    print("   ✓ Remove event from timeline")


def test_event_crud():
    """Test Event CRUD operations."""
    print("\nTesting Event CRUD...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    event_repo = EventRepository(session)
    event_service = EventService(event_repo)
    
    universe = universe_service.create_universe(name="Middle Earth")
    
    # CREATE
    print("\n1. Testing CREATE...")
    
    battle = event_service.create_event(
        name="Battle of Helm's Deep",
        universe_id=universe.id,
        event_type=EventType.BATTLE,
        importance=EventImportance.MAJOR,
        description="Decisive battle against Saruman's forces",
        date_string="March 3-4, 3019",
        date_precision=DatePrecision.DAY,
        date_sort_value=3019034,
        is_instantaneous=False,
        end_date_string="March 4, 3019",
        end_date_sort_value=3019044
    )
    assert battle.id is not None
    print(f"   ✓ Created event: {battle}")
    
    coronation = event_service.create_event(
        name="Aragorn's Coronation",
        universe_id=universe.id,
        event_type=EventType.CORONATION,
        importance=EventImportance.CRITICAL,
        date_string="May 1, 3019",
        date_sort_value=3019051
    )
    print(f"   ✓ Created event: {coronation}")
    
    # Test validation
    try:
        event_service.create_event(name="", universe_id=universe.id)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Empty name validation: {e}")
    
    # READ
    print("\n2. Testing READ...")
    retrieved = event_service.get_event(battle.id)
    assert retrieved.name == "Battle of Helm's Deep"
    print(f"   ✓ Retrieved by ID: {retrieved}")
    
    all_events = event_service.get_all_events(universe.id)
    assert len(all_events) == 2
    print(f"   ✓ Retrieved all: {len(all_events)} events")
    
    battles = event_service.get_by_type(universe.id, EventType.BATTLE)
    assert len(battles) == 1
    print(f"   ✓ Battles: {len(battles)}")
    
    critical_events = event_service.get_by_importance(universe.id, EventImportance.CRITICAL)
    assert len(critical_events) == 1
    print(f"   ✓ Critical events: {len(critical_events)}")
    
    sorted_events = event_service.get_sorted_by_date(universe.id)
    assert sorted_events[0].date_sort_value < sorted_events[1].date_sort_value
    print(f"   ✓ Events sorted by date")
    
    # UPDATE
    print("\n3. Testing UPDATE...")
    updated = event_service.update_event(
        battle.id,
        importance=EventImportance.LEGENDARY,
        description="Epic victory against overwhelming odds"
    )
    assert updated.importance == EventImportance.LEGENDARY
    print(f"   ✓ Updated event importance and description")
    
    # DELETE
    print("\n4. Testing DELETE...")
    deleted = event_service.delete_event(coronation.id)
    assert deleted is True
    remaining = event_service.get_all_events(universe.id)
    assert len(remaining) == 1
    print(f"   ✓ Deleted event")
    
    # SEARCH
    print("\n5. Testing SEARCH...")
    results = event_service.search_events(universe.id, "helm")
    assert len(results) == 1
    print(f"   ✓ Search 'helm': {results[0].name}")
    
    session.close()


def test_timeline_crud():
    """Test Timeline CRUD operations."""
    print("\nTesting Timeline CRUD...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    event_repo = EventRepository(session)
    event_service = EventService(event_repo)
    timeline_repo = TimelineRepository(session)
    timeline_service = TimelineService(timeline_repo)
    
    universe = universe_service.create_universe(name="Star Wars")
    
    # Create events
    event1 = event_service.create_event(
        name="Order 66",
        universe_id=universe.id,
        event_type=EventType.POLITICAL,
        date_sort_value=-19
    )
    
    event2 = event_service.create_event(
        name="Battle of Yavin",
        universe_id=universe.id,
        event_type=EventType.BATTLE,
        date_sort_value=0
    )
    
    # CREATE TIMELINE
    print("\n1. Testing CREATE TIMELINE...")
    
    main_timeline = timeline_service.create_timeline(
        name="Galactic History",
        universe_id=universe.id,
        description="Main timeline of galactic events",
        is_main_timeline=True
    )
    assert main_timeline.id is not None
    assert main_timeline.is_main_timeline == 1
    print(f"   ✓ Created main timeline: {main_timeline}")
    
    alt_timeline = timeline_service.create_timeline(
        name="What If: Order 66 Failed",
        universe_id=universe.id,
        is_main_timeline=False
    )
    print(f"   ✓ Created alternate timeline: {alt_timeline}")
    
    # Test only one main timeline
    main_check = timeline_service.get_main_timeline(universe.id)
    assert main_check.id == main_timeline.id
    print(f"   ✓ Only one main timeline enforced")
    
    # ADD EVENTS TO TIMELINE
    print("\n2. Testing ADD EVENTS...")
    timeline_service.add_event_to_timeline(main_timeline.id, event1.id)
    timeline_service.add_event_to_timeline(main_timeline.id, event2.id)
    
    updated_timeline = timeline_service.get_timeline(main_timeline.id)
    assert len(updated_timeline.get_event_ids()) == 2
    print(f"   ✓ Added {len(updated_timeline.get_event_ids())} events to timeline")
    
    # READ
    print("\n3. Testing READ...")
    all_timelines = timeline_service.get_all_timelines(universe.id)
    assert len(all_timelines) == 2
    print(f"   ✓ Retrieved all: {len(all_timelines)} timelines")
    
    # UPDATE
    print("\n4. Testing UPDATE...")
    updated = timeline_service.update_timeline(
        alt_timeline.id,
        description="Alternate history where the Jedi survived"
    )
    assert "Jedi survived" in updated.description
    print(f"   ✓ Updated timeline description")
    
    # REMOVE EVENT
    print("\n5. Testing REMOVE EVENT...")
    timeline_service.remove_event_from_timeline(main_timeline.id, event1.id)
    updated_timeline = timeline_service.get_timeline(main_timeline.id)
    assert len(updated_timeline.get_event_ids()) == 1
    print(f"   ✓ Removed event from timeline")
    
    # DELETE
    print("\n6. Testing DELETE...")
    deleted = timeline_service.delete_timeline(alt_timeline.id)
    assert deleted is True
    remaining = timeline_service.get_all_timelines(universe.id)
    assert len(remaining) == 1
    print(f"   ✓ Deleted timeline")
    
    session.close()


def test_event_ui_components():
    """Test Event UI components."""
    from worldbuilder.views.event_list_view import EventListView
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\nTesting Event UI Components...")
    
    list_view = EventListView()
    print("   ✓ EventListView created")
    
    # Test with actual events
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    event_repo = EventRepository(session)
    event_service = EventService(event_repo)
    
    universe = universe_service.create_universe(name="UI Test")
    
    ev1 = event_service.create_event(
        name="The Beginning",
        universe_id=universe.id,
        event_type=EventType.OTHER
    )
    
    ev2 = event_service.create_event(
        name="The End",
        universe_id=universe.id,
        event_type=EventType.OTHER
    )
    
    events = event_service.get_all_events(universe.id)
    list_view.load_events(events)
    
    assert list_view.table.rowCount() == 2
    print(f"   ✓ List view loaded {len(events)} events")
    
    session.close()


if __name__ == "__main__":
    print("=" * 70)
    print("Running WorldBuilder Phase 7 Tests")
    print("=" * 70)
    
    test_event_model()
    test_timeline_model()
    test_event_crud()
    test_timeline_crud()
    test_event_ui_components()
    
    print("\n" + "=" * 70)
    print("✓ ALL PHASE 7 TESTS PASSED!")
    print("=" * 70)

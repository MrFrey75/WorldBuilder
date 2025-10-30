"""Test Phase 3: Location System."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from worldbuilder.database import DatabaseManager, UniverseRepository, LocationRepository
from worldbuilder.services import UniverseService, LocationService
from worldbuilder.models import Location, LocationType


def test_location_model():
    """Test Location model methods."""
    print("\nTesting Location Model...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    
    location_repo = LocationRepository(session)
    location_service = LocationService(location_repo)
    
    # Create test universe
    universe = universe_service.create_universe(name="Test World")
    
    # Create location hierarchy
    continent = location_service.create_location(
        name="Westeros",
        universe_id=universe.id,
        location_type=LocationType.CONTINENT
    )
    
    region = location_service.create_location(
        name="The North",
        universe_id=universe.id,
        location_type=LocationType.REGION,
        parent_id=continent.id
    )
    
    city = location_service.create_location(
        name="Winterfell",
        universe_id=universe.id,
        location_type=LocationType.CITY,
        parent_id=region.id
    )
    
    building = location_service.create_location(
        name="Great Hall",
        universe_id=universe.id,
        location_type=LocationType.BUILDING,
        parent_id=city.id
    )
    
    # Test get_full_path
    path = building.get_full_path()
    assert path == "Westeros > The North > Winterfell > Great Hall"
    print(f"   ✓ Full path: {path}")
    
    # Test get_depth
    assert continent.get_depth() == 0
    assert region.get_depth() == 1
    assert city.get_depth() == 2
    assert building.get_depth() == 3
    print(f"   ✓ Depth calculation works")
    
    # Test is_ancestor_of
    assert continent.is_ancestor_of(building)
    assert region.is_ancestor_of(city)
    assert not city.is_ancestor_of(region)
    print(f"   ✓ Ancestor checking works")
    
    # Test get_all_descendants
    descendants = continent.get_all_descendants()
    assert len(descendants) == 3
    print(f"   ✓ Descendants: {len(descendants)} found")
    
    session.close()


def test_location_crud():
    """Test Location CRUD operations."""
    print("\nTesting Location CRUD...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    
    location_repo = LocationRepository(session)
    location_service = LocationService(location_repo)
    
    # Create universe
    universe = universe_service.create_universe(name="Fantasy World")
    
    # CREATE
    print("\n1. Testing CREATE...")
    location1 = location_service.create_location(
        name="Middle Earth",
        universe_id=universe.id,
        location_type=LocationType.CONTINENT,
        description="A vast continent"
    )
    assert location1.id is not None
    assert location1.name == "Middle Earth"
    print(f"   ✓ Created root location: {location1}")
    
    # Create child
    location2 = location_service.create_location(
        name="The Shire",
        universe_id=universe.id,
        location_type=LocationType.REGION,
        parent_id=location1.id
    )
    assert location2.parent_id == location1.id
    print(f"   ✓ Created child location: {location2}")
    
    # Test validation
    try:
        location_service.create_location(name="", universe_id=universe.id)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Empty name validation: {e}")
    
    # READ
    print("\n2. Testing READ...")
    retrieved = location_service.get_location(location1.id)
    assert retrieved.name == "Middle Earth"
    print(f"   ✓ Retrieved by ID: {retrieved}")
    
    all_locations = location_service.get_all_locations(universe.id)
    assert len(all_locations) == 2
    print(f"   ✓ Retrieved all: {len(all_locations)} locations")
    
    root_locations = location_service.get_root_locations(universe.id)
    assert len(root_locations) == 1
    assert root_locations[0].id == location1.id
    print(f"   ✓ Root locations: {len(root_locations)}")
    
    children = location_service.get_children(location1.id)
    assert len(children) == 1
    assert children[0].id == location2.id
    print(f"   ✓ Children: {len(children)}")
    
    # UPDATE
    print("\n3. Testing UPDATE...")
    updated = location_service.update_location(
        location1.id,
        description="The central continent of Middle Earth"
    )
    assert updated.description == "The central continent of Middle Earth"
    print(f"   ✓ Updated description")
    
    # Test circular reference prevention
    try:
        location_service.update_location(location1.id, parent_id=location2.id)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Circular reference prevention: {e}")
    
    # DELETE
    print("\n4. Testing DELETE...")
    
    # Create a location with children
    location3 = location_service.create_location(
        name="Mordor",
        universe_id=universe.id,
        location_type=LocationType.REGION,
        parent_id=location1.id
    )
    
    location4 = location_service.create_location(
        name="Mount Doom",
        universe_id=universe.id,
        location_type=LocationType.OTHER,
        parent_id=location3.id
    )
    
    # Try to delete without cascade
    try:
        location_service.delete_location(location3.id, cascade=False)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Delete with children blocked: {e}")
    
    # Delete with cascade
    deleted = location_service.delete_location(location3.id, cascade=True)
    assert deleted is True
    remaining = location_service.get_all_locations(universe.id)
    assert len(remaining) == 2  # location1 and location2
    print(f"   ✓ Cascade delete: removed location and descendants")
    
    # SEARCH
    print("\n5. Testing SEARCH...")
    results = location_service.search_locations(universe.id, "shire")
    assert len(results) == 1
    assert results[0].name == "The Shire"
    print(f"   ✓ Search 'shire': {results[0].name}")
    
    # GET BY TYPE
    print("\n6. Testing GET BY TYPE...")
    continents = location_service.get_by_type(universe.id, LocationType.CONTINENT)
    assert len(continents) == 1
    assert continents[0].name == "Middle Earth"
    print(f"   ✓ Found {len(continents)} continent(s)")
    
    session.close()


def test_location_repository():
    """Test LocationRepository methods."""
    print("\nTesting LocationRepository...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    location_repo = LocationRepository(session)
    
    # Create universe
    universe = universe_service.create_universe(name="Repo Test World")
    
    # Create locations
    loc1 = Location(
        name="Galaxy",
        universe_id=universe.id,
        location_type=LocationType.GALAXY
    )
    location_repo.add(loc1)
    location_repo.commit()
    
    loc2 = Location(
        name="Solar System",
        universe_id=universe.id,
        location_type=LocationType.STAR_SYSTEM,
        parent_id=loc1.id
    )
    location_repo.add(loc2)
    location_repo.commit()
    
    # Test has_children
    assert location_repo.has_children(loc1.id) is True
    assert location_repo.has_children(loc2.id) is False
    print(f"   ✓ has_children works")
    
    # Test get_by_universe
    all_locs = location_repo.get_by_universe(universe.id)
    assert len(all_locs) == 2
    print(f"   ✓ get_by_universe: {len(all_locs)} locations")
    
    session.close()


def test_location_ui_components():
    """Test Location UI components."""
    from worldbuilder.views.location_dialog import LocationDialog
    from worldbuilder.views.location_tree_view import LocationTreeView
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\nTesting Location UI Components...")
    
    # Test LocationDialog
    dialog = LocationDialog(universe_id=1)
    assert dialog.universe_id == 1
    assert not dialog.is_edit_mode
    print("   ✓ LocationDialog created")
    
    # Test LocationTreeView
    tree_view = LocationTreeView()
    tree_view.set_universe(1)
    assert tree_view._current_universe_id == 1
    print("   ✓ LocationTreeView created")
    
    # Test with actual locations
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    location_repo = LocationRepository(session)
    location_service = LocationService(location_repo)
    
    universe = universe_service.create_universe(name="UI Test")
    
    loc1 = location_service.create_location(
        name="Root",
        universe_id=universe.id,
        location_type=LocationType.CONTINENT
    )
    
    loc2 = location_service.create_location(
        name="Child",
        universe_id=universe.id,
        location_type=LocationType.REGION,
        parent_id=loc1.id
    )
    
    locations = location_service.get_all_locations(universe.id)
    tree_view.load_locations(locations)
    
    assert len(tree_view._location_items) == 2
    print(f"   ✓ Tree view loaded {len(locations)} locations")
    
    session.close()


if __name__ == "__main__":
    print("=" * 70)
    print("Running WorldBuilder Phase 3 Tests")
    print("=" * 70)
    
    test_location_model()
    test_location_crud()
    test_location_repository()
    test_location_ui_components()
    
    print("\n" + "=" * 70)
    print("✓ ALL PHASE 3 TESTS PASSED!")
    print("=" * 70)

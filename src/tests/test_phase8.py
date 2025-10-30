"""Test Phase 8: Search & Filter System."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from worldbuilder.database import (DatabaseManager, UniverseRepository, LocationRepository,
                                   SpeciesRepository, NotableFigureRepository, EventRepository)
from worldbuilder.services import (UniverseService, LocationService, SpeciesService,
                                   NotableFigureService, EventService, SearchService)
from worldbuilder.models import LocationType, EventType


def test_basic_search():
    """Test basic search functionality."""
    print("\nTesting Basic Search...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    # Create test data
    universe_service = UniverseService(UniverseRepository(session))
    location_service = LocationService(LocationRepository(session))
    species_service = SpeciesService(SpeciesRepository(session))
    figure_service = NotableFigureService(NotableFigureRepository(session))
    event_service = EventService(EventRepository(session))
    search_service = SearchService(session)
    
    universe = universe_service.create_universe(name="Middle Earth")
    shire = location_service.create_location("The Shire", universe.id, LocationType.REGION)
    mordor = location_service.create_location("Mordor", universe.id, LocationType.REGION)
    human = species_service.create_default_human(universe.id)
    hobbit = species_service.create_species("Hobbit", universe.id, description="Small folk of the Shire")
    
    frodo = figure_service.create_figure(
        "Frodo Baggins", universe.id, species_id=hobbit.id,
        backstory="Bearer of the One Ring"
    )
    aragorn = figure_service.create_figure(
        "Aragorn", universe.id, species_id=human.id,
        title="King of Gondor"
    )
    
    quest = event_service.create_event(
        "Quest to Mount Doom", universe.id, EventType.QUEST,
        description="Journey to destroy the Ring"
    )
    
    # Test search by name
    print("\n1. Testing name search...")
    results = search_service.global_search("frodo", universe.id)
    assert len(results) == 1
    assert results[0].entity_type == 'notable_figure'
    assert 'Frodo' in results[0].entity.name
    print(f"   ✓ Found: {results[0].entity.name}")
    
    # Test search across multiple entities
    print("\n2. Testing multi-entity search...")
    results = search_service.global_search("shire", universe.id)
    assert len(results) >= 2  # Location and species description
    types_found = set(r.entity_type for r in results)
    assert 'location' in types_found
    print(f"   ✓ Found {len(results)} results across types: {types_found}")
    
    # Test description search
    print("\n3. Testing description search...")
    results = search_service.global_search("ring", universe.id)
    assert len(results) >= 2  # Figure backstory and event description
    print(f"   ✓ Found {len(results)} matches in descriptions")
    
    # Test case-insensitive search
    print("\n4. Testing case-insensitive search...")
    results_lower = search_service.global_search("aragorn", universe.id)
    results_upper = search_service.global_search("ARAGORN", universe.id)
    assert len(results_lower) == len(results_upper)
    print(f"   ✓ Case-insensitive search works")
    
    # Test empty query
    print("\n5. Testing empty query...")
    results = search_service.global_search("", universe.id)
    assert len(results) == 0
    print(f"   ✓ Empty query returns no results")
    
    # Test no matches
    print("\n6. Testing no matches...")
    results = search_service.global_search("nonexistent123", universe.id)
    assert len(results) == 0
    print(f"   ✓ No false matches")
    
    session.close()


def test_filtered_search():
    """Test search with entity type filtering."""
    print("\nTesting Filtered Search...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_service = UniverseService(UniverseRepository(session))
    location_service = LocationService(LocationRepository(session))
    species_service = SpeciesService(SpeciesRepository(session))
    search_service = SearchService(session)
    
    universe = universe_service.create_universe(name="Test Universe")
    location_service.create_location("Test Location", universe.id, LocationType.CITY)
    species_service.create_species("Test Species", universe.id)
    
    # Search only locations
    print("\n1. Testing location-only filter...")
    results = search_service.global_search("test", universe.id, entity_types=['location'])
    assert len(results) == 1
    assert results[0].entity_type == 'location'
    print(f"   ✓ Location filter works: {results[0].entity.name}")
    
    # Search only species
    print("\n2. Testing species-only filter...")
    results = search_service.global_search("test", universe.id, entity_types=['species'])
    assert len(results) == 1
    assert results[0].entity_type == 'species'
    print(f"   ✓ Species filter works: {results[0].entity.name}")
    
    # Search multiple types
    print("\n3. Testing multi-type filter...")
    results = search_service.global_search("test", universe.id, 
                                          entity_types=['location', 'species'])
    assert len(results) == 2
    types = {r.entity_type for r in results}
    assert types == {'location', 'species'}
    print(f"   ✓ Multi-type filter works: {types}")
    
    session.close()


def test_universe_scoped_search():
    """Test search scoped to specific universe."""
    print("\nTesting Universe-Scoped Search...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_service = UniverseService(UniverseRepository(session))
    location_service = LocationService(LocationRepository(session))
    search_service = SearchService(session)
    
    universe1 = universe_service.create_universe(name="Universe One")
    universe2 = universe_service.create_universe(name="Universe Two")
    
    location_service.create_location("Shared Name", universe1.id, LocationType.CITY)
    location_service.create_location("Shared Name", universe2.id, LocationType.CITY)
    location_service.create_location("Unique to One", universe1.id, LocationType.CITY)
    
    # Search in universe 1
    print("\n1. Testing universe 1 scope...")
    results = search_service.global_search("shared", universe1.id, entity_types=['location'])
    assert len(results) == 1
    assert results[0].entity.universe_id == universe1.id
    print(f"   ✓ Found in universe 1: {results[0].entity.name}")
    
    # Search in universe 2
    print("\n2. Testing universe 2 scope...")
    results = search_service.global_search("shared", universe2.id, entity_types=['location'])
    assert len(results) == 1
    assert results[0].entity.universe_id == universe2.id
    print(f"   ✓ Found in universe 2: {results[0].entity.name}")
    
    # Global search (no universe specified)
    print("\n3. Testing global search...")
    results = search_service.global_search("shared", entity_types=['location'])
    assert len(results) == 2
    print(f"   ✓ Global search found {len(results)} matches")
    
    session.close()


def test_search_snippet():
    """Test search result snippet extraction."""
    print("\nTesting Search Snippets...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_service = UniverseService(UniverseRepository(session))
    location_service = LocationService(LocationRepository(session))
    search_service = SearchService(session)
    
    universe = universe_service.create_universe(name="Test")
    
    long_description = (
        "This is a long description that contains many words. "
        "The search term appears somewhere in the middle of this text. "
        "We want to extract a snippet around the search term."
    )
    
    location_service.create_location(
        "Test Location", universe.id, LocationType.CITY,
        description=long_description
    )
    
    print("\n1. Testing snippet extraction...")
    results = search_service.global_search("search term", universe.id)
    assert len(results) == 1
    snippet = results[0].match_snippet
    assert "search term" in snippet.lower()
    assert len(snippet) < len(long_description)  # Should be shorter
    print(f"   ✓ Snippet: {snippet[:50]}...")
    
    session.close()


def test_search_ui_components():
    """Test Search UI components."""
    from worldbuilder.views.search_widget import SearchWidget
    from worldbuilder.views.filter_widget import AdvancedFilterWidget
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\nTesting Search UI Components...")
    
    # Test SearchWidget
    search_widget = SearchWidget()
    assert search_widget.search_input is not None
    assert search_widget.results_table is not None
    print("   ✓ SearchWidget created")
    
    # Test filter checkboxes
    entity_types = search_widget.get_selected_entity_types()
    assert len(entity_types) == 7  # All should be checked by default
    print(f"   ✓ Default filters: {len(entity_types)} types")
    
    # Test AdvancedFilterWidget
    filter_widget = AdvancedFilterWidget()
    assert filter_widget.type_combo is not None
    assert filter_widget.location_combo is not None
    print("   ✓ AdvancedFilterWidget created")
    
    # Test filter getting
    filters = filter_widget.get_filters()
    assert isinstance(filters, dict)
    print(f"   ✓ Filter dict: {filters}")
    
    # Test filter clearing
    filter_widget.location_enabled.setChecked(True)
    filter_widget.clear_filters()
    assert not filter_widget.location_enabled.isChecked()
    print(f"   ✓ Filter clearing works")


def test_search_result_object():
    """Test SearchResult object."""
    from worldbuilder.services.search_service import SearchResult
    
    print("\nTesting SearchResult Object...")
    
    class MockEntity:
        def __init__(self):
            self.name = "Test Entity"
    
    result = SearchResult(
        entity_type="location",
        entity_id=1,
        entity=MockEntity(),
        matched_field="name",
        match_snippet="Test Entity"
    )
    
    assert result.entity_type == "location"
    assert result.entity_id == 1
    assert result.matched_field == "name"
    print(f"   ✓ SearchResult created: {result}")


if __name__ == "__main__":
    print("=" * 70)
    print("Running WorldBuilder Phase 8 Tests")
    print("=" * 70)
    
    test_search_result_object()
    test_basic_search()
    test_filtered_search()
    test_universe_scoped_search()
    test_search_snippet()
    test_search_ui_components()
    
    print("\n" + "=" * 70)
    print("✓ ALL PHASE 8 TESTS PASSED!")
    print("=" * 70)

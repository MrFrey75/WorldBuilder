"""Test Phase 5: Notable Figures System."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from worldbuilder.database import (DatabaseManager, UniverseRepository, 
                                   SpeciesRepository, LocationRepository, 
                                   NotableFigureRepository)
from worldbuilder.services import (UniverseService, SpeciesService, 
                                   LocationService, NotableFigureService)
from worldbuilder.models import NotableFigure, SpeciesType, LocationType


def test_notable_figure_model():
    """Test NotableFigure model methods."""
    print("\nTesting NotableFigure Model...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    species_repo = SpeciesRepository(session)
    species_service = SpeciesService(species_repo)
    figure_repo = NotableFigureRepository(session)
    
    # Create test data
    universe = universe_service.create_universe(name="Test World")
    human = species_service.create_default_human(universe.id)
    
    # Create figure
    figure = NotableFigure(
        name="Aragorn",
        title="King",
        universe_id=universe.id,
        species_id=human.id,
        age="87",
        occupation="Ranger"
    )
    figure_repo.add(figure)
    figure_repo.commit()
    
    # Test get_full_name
    full_name = figure.get_full_name()
    assert full_name == "King Aragorn"
    print(f"   ✓ Full name: {full_name}")
    
    # Test attribute methods
    figure.set_attribute("hair_color", "Dark")
    hair = figure.get_attribute("hair_color")
    assert hair == "Dark"
    print(f"   ✓ Attribute get/set works")
    
    # Test get_summary
    summary = figure.get_summary()
    assert "Aragorn" in summary
    assert "Ranger" in summary
    print(f"   ✓ Summary: {summary}")
    
    session.close()


def test_notable_figure_crud():
    """Test NotableFigure CRUD operations."""
    print("\nTesting NotableFigure CRUD...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    species_repo = SpeciesRepository(session)
    species_service = SpeciesService(species_repo)
    location_repo = LocationRepository(session)
    location_service = LocationService(location_repo)
    figure_repo = NotableFigureRepository(session)
    figure_service = NotableFigureService(figure_repo)
    
    # Create test universe
    universe = universe_service.create_universe(name="Middle Earth")
    
    # Create species
    human = species_service.create_default_human(universe.id)
    elf = species_service.create_species(
        name="Elf",
        universe_id=universe.id,
        species_type=SpeciesType.SENTIENT
    )
    
    # Create location
    shire = location_service.create_location(
        name="The Shire",
        universe_id=universe.id,
        location_type=LocationType.REGION
    )
    
    # CREATE
    print("\n1. Testing CREATE...")
    frodo = figure_service.create_figure(
        name="Frodo Baggins",
        universe_id=universe.id,
        species_id=human.id,
        location_id=shire.id,
        age="50",
        occupation="Ring Bearer",
        description="A brave hobbit",
        attributes={"hair_color": "Brown", "height": "3.5 feet"},
        personality="Brave, kind, determined",
        goals="Destroy the One Ring"
    )
    assert frodo.id is not None
    assert frodo.name == "Frodo Baggins"
    print(f"   ✓ Created figure: {frodo}")
    
    # Test validation
    try:
        figure_service.create_figure(name="", universe_id=universe.id)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Empty name validation: {e}")
    
    # READ
    print("\n2. Testing READ...")
    retrieved = figure_service.get_figure(frodo.id)
    assert retrieved.name == "Frodo Baggins"
    assert retrieved.get_attribute("hair_color") == "Brown"
    print(f"   ✓ Retrieved by ID: {retrieved}")
    
    all_figures = figure_service.get_all_figures(universe.id)
    assert len(all_figures) == 1
    print(f"   ✓ Retrieved all: {len(all_figures)} figures")
    
    # Create more figures
    legolas = figure_service.create_figure(
        name="Legolas",
        universe_id=universe.id,
        species_id=elf.id,
        occupation="Archer"
    )
    
    gandalf = figure_service.create_figure(
        name="Gandalf",
        title="The Grey",
        universe_id=universe.id,
        occupation="Wizard"
    )
    
    # Test get_by_species
    humans = figure_service.get_by_species(human.id)
    assert len(humans) == 1
    print(f"   ✓ Humans: {len(humans)}")
    
    elves = figure_service.get_by_species(elf.id)
    assert len(elves) == 1
    print(f"   ✓ Elves: {len(elves)}")
    
    # Test get_by_location
    shire_folks = figure_service.get_by_location(shire.id)
    assert len(shire_folks) == 1
    print(f"   ✓ Figures in Shire: {len(shire_folks)}")
    
    # Test get_by_occupation
    wizards = figure_service.get_by_occupation(universe.id, "Wizard")
    assert len(wizards) == 1
    print(f"   ✓ Wizards: {len(wizards)}")
    
    # UPDATE
    print("\n3. Testing UPDATE...")
    updated = figure_service.update_figure(
        frodo.id,
        title="Mr.",
        backstory="Born in the Shire, inherited the Ring from Bilbo"
    )
    assert updated.title == "Mr."
    assert "Bilbo" in updated.backstory
    print(f"   ✓ Updated figure: {updated.get_full_name()}")
    
    # DELETE
    print("\n4. Testing DELETE...")
    deleted = figure_service.delete_figure(gandalf.id)
    assert deleted is True
    remaining = figure_service.get_all_figures(universe.id)
    assert len(remaining) == 2
    print(f"   ✓ Deleted figure")
    
    # SEARCH
    print("\n5. Testing SEARCH...")
    results = figure_service.search_figures(universe.id, "frodo")
    assert len(results) == 1
    assert results[0].name == "Frodo Baggins"
    print(f"   ✓ Search 'frodo': {results[0].name}")
    
    session.close()


def test_notable_figure_repository():
    """Test NotableFigureRepository methods."""
    print("\nTesting NotableFigureRepository...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    species_repo = SpeciesRepository(session)
    species_service = SpeciesService(species_repo)
    figure_repo = NotableFigureRepository(session)
    
    # Create test data
    universe = universe_service.create_universe(name="Repo Test")
    human = species_service.create_default_human(universe.id)
    
    # Create figures
    fig1 = NotableFigure(
        name="Arthur",
        title="King",
        universe_id=universe.id,
        species_id=human.id,
        occupation="King"
    )
    figure_repo.add(fig1)
    figure_repo.commit()
    
    fig2 = NotableFigure(
        name="Merlin",
        universe_id=universe.id,
        species_id=human.id,
        occupation="Wizard"
    )
    figure_repo.add(fig2)
    figure_repo.commit()
    
    # Test get_by_universe
    all_figs = figure_repo.get_by_universe(universe.id)
    assert len(all_figs) == 2
    print(f"   ✓ get_by_universe: {len(all_figs)} figures")
    
    # Test get_by_species
    human_figs = figure_repo.get_by_species(human.id)
    assert len(human_figs) == 2
    print(f"   ✓ get_by_species: {len(human_figs)} humans")
    
    # Test get_by_occupation
    kings = figure_repo.get_by_occupation(universe.id, "King")
    assert len(kings) == 1
    assert kings[0].name == "Arthur"
    print(f"   ✓ get_by_occupation: {len(kings)} kings")
    
    session.close()


def test_notable_figure_ui_components():
    """Test NotableFigure UI components."""
    from worldbuilder.views.notable_figure_dialog import NotableFigureDialog
    from worldbuilder.views.notable_figure_list_view import NotableFigureListView
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\nTesting NotableFigure UI Components...")
    
    # Test NotableFigureDialog
    dialog = NotableFigureDialog(universe_id=1)
    assert dialog.universe_id == 1
    assert not dialog.is_edit_mode
    print("   ✓ NotableFigureDialog created")
    
    # Test NotableFigureListView
    list_view = NotableFigureListView()
    print("   ✓ NotableFigureListView created")
    
    # Test with actual figures
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    species_repo = SpeciesRepository(session)
    species_service = SpeciesService(species_repo)
    figure_repo = NotableFigureRepository(session)
    figure_service = NotableFigureService(figure_repo)
    
    universe = universe_service.create_universe(name="UI Test")
    human = species_service.create_default_human(universe.id)
    
    fig1 = figure_service.create_figure(
        name="Alice",
        universe_id=universe.id,
        species_id=human.id
    )
    
    fig2 = figure_service.create_figure(
        name="Bob",
        title="Sir",
        universe_id=universe.id,
        species_id=human.id
    )
    
    figures = figure_service.get_all_figures(universe.id)
    list_view.load_figures(figures)
    
    assert list_view.table.rowCount() == 2
    print(f"   ✓ List view loaded {len(figures)} figures")
    
    session.close()


if __name__ == "__main__":
    print("=" * 70)
    print("Running WorldBuilder Phase 5 Tests")
    print("=" * 70)
    
    test_notable_figure_model()
    test_notable_figure_crud()
    test_notable_figure_repository()
    test_notable_figure_ui_components()
    
    print("\n" + "=" * 70)
    print("✓ ALL PHASE 5 TESTS PASSED!")
    print("=" * 70)

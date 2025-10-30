"""Test Phase 4: Species & Races System."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from worldbuilder.database import DatabaseManager, UniverseRepository, SpeciesRepository
from worldbuilder.services import UniverseService, SpeciesService
from worldbuilder.models import Species, SpeciesType


def test_species_model():
    """Test Species model methods."""
    print("\nTesting Species Model...")
    
    # Test create_default_human
    human = Species.create_default_human(universe_id=1)
    assert human.name == "Human"
    assert human.species_type == SpeciesType.SENTIENT
    assert human.is_playable is True
    print("   ✓ Default human creation works")
    
    # Test trait methods
    human.set_trait("height", "5-6 feet")
    height = human.get_trait("height")
    assert height == "5-6 feet"
    print("   ✓ Trait get/set works")
    
    unknown = human.get_trait("unknown", "default")
    assert unknown == "default"
    print("   ✓ Trait default value works")


def test_species_crud():
    """Test Species CRUD operations."""
    print("\nTesting Species CRUD...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    
    species_repo = SpeciesRepository(session)
    species_service = SpeciesService(species_repo)
    
    # Create universe
    universe = universe_service.create_universe(name="Fantasy Realm")
    
    # CREATE
    print("\n1. Testing CREATE...")
    
    # Create default human
    human = species_service.create_default_human(universe.id)
    assert human.name == "Human"
    print(f"   ✓ Created default human: {human}")
    
    # Create custom species
    elf = species_service.create_species(
        name="Elf",
        universe_id=universe.id,
        species_type=SpeciesType.SENTIENT,
        description="Graceful and long-lived",
        physical_traits={
            "height": "5-6 feet",
            "lifespan": "500-800 years",
            "build": "Slender",
            "special_features": "Pointed ears"
        },
        abilities="Enhanced senses, natural magic affinity",
        culture="Close to nature, artistic"
    )
    assert elf.id is not None
    assert elf.name == "Elf"
    print(f"   ✓ Created custom species: {elf}")
    
    # Test validation
    try:
        species_service.create_species(name="", universe_id=universe.id)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Empty name validation: {e}")
    
    # Test duplicate name
    try:
        species_service.create_species(name="Human", universe_id=universe.id)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Duplicate name validation: {e}")
    
    # READ
    print("\n2. Testing READ...")
    retrieved = species_service.get_species(elf.id)
    assert retrieved.name == "Elf"
    assert retrieved.get_trait("special_features") == "Pointed ears"
    print(f"   ✓ Retrieved by ID: {retrieved}")
    
    all_species = species_service.get_all_species(universe.id)
    assert len(all_species) == 2
    print(f"   ✓ Retrieved all: {len(all_species)} species")
    
    playable = species_service.get_playable_species(universe.id)
    assert len(playable) == 2
    print(f"   ✓ Playable species: {len(playable)}")
    
    sentient = species_service.get_by_type(universe.id, SpeciesType.SENTIENT)
    assert len(sentient) == 2
    print(f"   ✓ Sentient species: {len(sentient)}")
    
    # UPDATE
    print("\n3. Testing UPDATE...")
    updated = species_service.update_species(
        elf.id,
        description="Ancient and wise beings of the forest"
    )
    assert updated.description == "Ancient and wise beings of the forest"
    print(f"   ✓ Updated description")
    
    # Test duplicate name update
    try:
        species_service.update_species(elf.id, name="Human")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Duplicate name update blocked: {e}")
    
    # DELETE
    print("\n4. Testing DELETE...")
    
    # Create a temporary species
    orc = species_service.create_species(
        name="Orc",
        universe_id=universe.id,
        species_type=SpeciesType.SENTIENT
    )
    
    deleted = species_service.delete_species(orc.id)
    assert deleted is True
    remaining = species_service.get_all_species(universe.id)
    assert len(remaining) == 2
    print(f"   ✓ Deleted species")
    
    # SEARCH
    print("\n5. Testing SEARCH...")
    results = species_service.search_species(universe.id, "elf")
    assert len(results) == 1
    assert results[0].name == "Elf"
    print(f"   ✓ Search 'elf': {results[0].name}")
    
    session.close()


def test_species_repository():
    """Test SpeciesRepository methods."""
    print("\nTesting SpeciesRepository...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    species_repo = SpeciesRepository(session)
    
    # Create universe
    universe = universe_service.create_universe(name="Repo Test")
    
    # Create species
    sp1 = Species(
        name="Dragon",
        universe_id=universe.id,
        species_type=SpeciesType.MAGICAL,
        is_playable=False
    )
    species_repo.add(sp1)
    species_repo.commit()
    
    sp2 = Species(
        name="Dwarf",
        universe_id=universe.id,
        species_type=SpeciesType.SENTIENT,
        is_playable=True
    )
    species_repo.add(sp2)
    species_repo.commit()
    
    # Test get_by_universe
    all_sp = species_repo.get_by_universe(universe.id)
    assert len(all_sp) == 2
    print(f"   ✓ get_by_universe: {len(all_sp)} species")
    
    # Test get_playable_species
    playable = species_repo.get_playable_species(universe.id)
    assert len(playable) == 1
    assert playable[0].name == "Dwarf"
    print(f"   ✓ get_playable_species: {len(playable)}")
    
    # Test get_by_type
    magical = species_repo.get_by_type(universe.id, SpeciesType.MAGICAL)
    assert len(magical) == 1
    assert magical[0].name == "Dragon"
    print(f"   ✓ get_by_type: {len(magical)} magical")
    
    session.close()


def test_species_ui_components():
    """Test Species UI components."""
    from worldbuilder.views.species_dialog import SpeciesDialog
    from worldbuilder.views.species_list_view import SpeciesListView
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\nTesting Species UI Components...")
    
    # Test SpeciesDialog
    dialog = SpeciesDialog(universe_id=1)
    assert dialog.universe_id == 1
    assert not dialog.is_edit_mode
    print("   ✓ SpeciesDialog created")
    
    # Test SpeciesListView
    list_view = SpeciesListView()
    print("   ✓ SpeciesListView created")
    
    # Test with actual species
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    species_repo = SpeciesRepository(session)
    species_service = SpeciesService(species_repo)
    
    universe = universe_service.create_universe(name="UI Test")
    
    human = species_service.create_default_human(universe.id)
    elf = species_service.create_species(
        name="Elf",
        universe_id=universe.id,
        species_type=SpeciesType.SENTIENT
    )
    
    species_list = species_service.get_all_species(universe.id)
    list_view.load_species(species_list)
    
    assert list_view.table.rowCount() == 2
    print(f"   ✓ List view loaded {len(species_list)} species")
    
    session.close()


if __name__ == "__main__":
    print("=" * 70)
    print("Running WorldBuilder Phase 4 Tests")
    print("=" * 70)
    
    test_species_model()
    test_species_crud()
    test_species_repository()
    test_species_ui_components()
    
    print("\n" + "=" * 70)
    print("✓ ALL PHASE 4 TESTS PASSED!")
    print("=" * 70)

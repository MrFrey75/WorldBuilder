"""Test Universe service and CRUD operations."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from worldbuilder.database import DatabaseManager, UniverseRepository
from worldbuilder.services import UniverseService


def test_universe_crud():
    """Test Universe CRUD operations."""
    # Setup
    db_manager = DatabaseManager()  # In-memory
    db_manager.create_tables()
    session = db_manager.get_session()
    repository = UniverseRepository(session)
    service = UniverseService(repository)
    
    print("Testing Universe CRUD operations...\n")
    
    # CREATE
    print("1. Testing CREATE...")
    universe1 = service.create_universe(
        name="Middle Earth",
        description="The world of The Lord of the Rings",
        author="J.R.R. Tolkien",
        genre="Fantasy"
    )
    assert universe1.id is not None
    assert universe1.name == "Middle Earth"
    assert universe1.author == "J.R.R. Tolkien"
    print(f"   ✓ Created: {universe1}")
    
    # Test duplicate name validation
    try:
        service.create_universe(name="Middle Earth")
        assert False, "Should have raised ValueError for duplicate name"
    except ValueError as e:
        print(f"   ✓ Duplicate validation works: {e}")
    
    # CREATE more universes
    universe2 = service.create_universe(
        name="Westeros",
        author="George R.R. Martin",
        genre="Fantasy"
    )
    universe3 = service.create_universe(
        name="Foundation Galaxy",
        author="Isaac Asimov",
        genre="Science Fiction"
    )
    print(f"   ✓ Created: {universe2}")
    print(f"   ✓ Created: {universe3}")
    
    # READ
    print("\n2. Testing READ...")
    retrieved = service.get_universe(universe1.id)
    assert retrieved.name == "Middle Earth"
    print(f"   ✓ Retrieved by ID: {retrieved}")
    
    all_universes = service.get_all_universes()
    assert len(all_universes) == 3
    print(f"   ✓ Retrieved all: {len(all_universes)} universes")
    
    # UPDATE
    print("\n3. Testing UPDATE...")
    updated = service.update_universe(
        universe1.id,
        description="The legendary world of hobbits, elves, and wizards"
    )
    assert updated.description == "The legendary world of hobbits, elves, and wizards"
    print(f"   ✓ Updated description: {updated.description[:50]}...")
    
    # Test name conflict during update
    try:
        service.update_universe(universe2.id, name="Middle Earth")
        assert False, "Should have raised ValueError for name conflict"
    except ValueError as e:
        print(f"   ✓ Update name conflict validation works: {e}")
    
    # DELETE
    print("\n4. Testing DELETE...")
    deleted = service.delete_universe(universe3.id)
    assert deleted is True
    remaining = service.get_all_universes()
    assert len(remaining) == 2
    print(f"   ✓ Deleted universe: Foundation Galaxy")
    print(f"   ✓ Remaining universes: {len(remaining)}")
    
    # ACTIVE UNIVERSE
    print("\n5. Testing SET ACTIVE...")
    service.set_active_universe(universe1.id)
    active_universes = service.get_active_universes()
    assert len(active_universes) == 1
    assert active_universes[0].id == universe1.id
    print(f"   ✓ Set active universe: {active_universes[0].name}")
    
    # SEARCH
    print("\n6. Testing SEARCH...")
    results = service.search_universes("middle")
    assert len(results) == 1
    assert results[0].name == "Middle Earth"
    print(f"   ✓ Search 'middle': {results[0].name}")
    
    session.close()
    print("\n✓ All Universe CRUD tests passed!")


def test_validation():
    """Test service validation."""
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    repository = UniverseRepository(session)
    service = UniverseService(repository)
    
    print("\nTesting validation...\n")
    
    # Empty name
    try:
        service.create_universe(name="")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Empty name validation: {e}")
    
    # Whitespace name
    try:
        service.create_universe(name="   ")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Whitespace name validation: {e}")
    
    session.close()
    print("\n✓ All validation tests passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("Running WorldBuilder Phase 2.1 Tests")
    print("=" * 60 + "\n")
    
    test_universe_crud()
    test_validation()
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)

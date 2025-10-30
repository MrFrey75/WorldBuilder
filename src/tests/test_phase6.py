"""Test Phase 6: Relationships & Connections."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from worldbuilder.database import (DatabaseManager, UniverseRepository, 
                                   SpeciesRepository, NotableFigureRepository,
                                   RelationshipRepository)
from worldbuilder.services import (UniverseService, SpeciesService, 
                                   NotableFigureService, RelationshipService)
from worldbuilder.models import Relationship, RelationshipType, RelationshipStrength


def test_relationship_model():
    """Test Relationship model methods."""
    print("\nTesting Relationship Model...")
    
    # Test inverse types
    rel = Relationship()
    rel.relationship_type = RelationshipType.PARENT
    assert rel.get_inverse_type() == RelationshipType.CHILD
    print("   ✓ Parent-Child inverse works")
    
    rel.relationship_type = RelationshipType.MENTOR
    assert rel.get_inverse_type() == RelationshipType.STUDENT
    print("   ✓ Mentor-Student inverse works")
    
    # Test bidirectional check
    rel.relationship_type = RelationshipType.FRIEND
    assert rel.is_bidirectional() is True
    print("   ✓ Friend is bidirectional")
    
    rel.relationship_type = RelationshipType.PARENT
    assert rel.is_bidirectional() is False
    print("   ✓ Parent is not bidirectional")
    
    # Test custom type display
    rel.relationship_type = RelationshipType.CUSTOM
    rel.custom_type_name = "Blood Brothers"
    assert rel.get_type_display() == "Blood Brothers"
    print("   ✓ Custom type display works")


def test_relationship_crud():
    """Test Relationship CRUD operations."""
    print("\nTesting Relationship CRUD...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    species_repo = SpeciesRepository(session)
    species_service = SpeciesService(species_repo)
    figure_repo = NotableFigureRepository(session)
    figure_service = NotableFigureService(figure_repo)
    rel_repo = RelationshipRepository(session)
    rel_service = RelationshipService(rel_repo)
    
    # Create test data
    universe = universe_service.create_universe(name="Test Realm")
    human = species_service.create_default_human(universe.id)
    
    # Create figures
    aragorn = figure_service.create_figure(
        name="Aragorn",
        universe_id=universe.id,
        species_id=human.id
    )
    
    arwen = figure_service.create_figure(
        name="Arwen",
        universe_id=universe.id,
        species_id=human.id
    )
    
    elrond = figure_service.create_figure(
        name="Elrond",
        universe_id=universe.id,
        species_id=human.id
    )
    
    # CREATE
    print("\n1. Testing CREATE...")
    
    # Create spouse relationship
    spouse_rel = rel_service.create_relationship(
        universe_id=universe.id,
        source_type="notable_figure",
        source_id=aragorn.id,
        target_type="notable_figure",
        target_id=arwen.id,
        relationship_type=RelationshipType.SPOUSE,
        strength=RelationshipStrength.VERY_STRONG,
        description="Married after the War of the Ring"
    )
    assert spouse_rel.id is not None
    print(f"   ✓ Created relationship: {spouse_rel}")
    
    # Create parent-child relationship (should auto-create inverse)
    parent_rel = rel_service.create_relationship(
        universe_id=universe.id,
        source_type="notable_figure",
        source_id=elrond.id,
        target_type="notable_figure",
        target_id=arwen.id,
        relationship_type=RelationshipType.PARENT,
        create_inverse=True
    )
    print(f"   ✓ Created parent relationship with auto-inverse")
    
    # Test validation
    try:
        rel_service.create_relationship(
            universe_id=universe.id,
            source_type="notable_figure",
            source_id=aragorn.id,
            target_type="notable_figure",
            target_id=aragorn.id,
            relationship_type=RelationshipType.FRIEND
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Self-relationship validation: {e}")
    
    # READ
    print("\n2. Testing READ...")
    retrieved = rel_service.get_relationship(spouse_rel.id)
    assert retrieved.source_entity_id == aragorn.id
    print(f"   ✓ Retrieved by ID: {retrieved}")
    
    all_rels = rel_service.get_all_relationships(universe.id)
    assert len(all_rels) == 3  # spouse + parent + child (inverse)
    print(f"   ✓ Retrieved all: {len(all_rels)} relationships")
    
    # Get relationships for specific entity
    aragorn_rels = rel_service.get_relationships_for_entity("notable_figure", aragorn.id)
    assert len(aragorn_rels) == 1  # spouse relationship
    print(f"   ✓ Aragorn's relationships: {len(aragorn_rels)}")
    
    arwen_rels = rel_service.get_relationships_for_entity("notable_figure", arwen.id)
    assert len(arwen_rels) == 3  # spouse + parent + child
    print(f"   ✓ Arwen's relationships: {len(arwen_rels)}")
    
    # Get by type
    spouses = rel_service.get_by_type(universe.id, RelationshipType.SPOUSE)
    assert len(spouses) == 1
    print(f"   ✓ Spouse relationships: {len(spouses)}")
    
    # UPDATE
    print("\n3. Testing UPDATE...")
    updated = rel_service.update_relationship(
        spouse_rel.id,
        start_date="Year 3019",
        description="United the kingdoms of Men and Elves"
    )
    assert "3019" in updated.start_date
    print(f"   ✓ Updated relationship dates and description")
    
    # End a relationship
    ended = rel_service.end_relationship(spouse_rel.id, end_date="Year 3021")
    assert ended.is_active == 0
    assert ended.end_date == "Year 3021"
    print(f"   ✓ Ended relationship")
    
    # DELETE
    print("\n4. Testing DELETE...")
    deleted = rel_service.delete_relationship(parent_rel.id)
    assert deleted is True
    remaining = rel_service.get_all_relationships(universe.id)
    assert len(remaining) == 2  # spouse + child (inverse wasn't auto-deleted)
    print(f"   ✓ Deleted relationship")
    
    session.close()


def test_relationship_repository():
    """Test RelationshipRepository methods."""
    print("\nTesting RelationshipRepository...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    rel_repo = RelationshipRepository(session)
    
    universe = universe_service.create_universe(name="Repo Test")
    
    # Create relationships directly
    rel1 = Relationship(
        universe_id=universe.id,
        source_entity_type="notable_figure",
        source_entity_id=1,
        target_entity_type="notable_figure",
        target_entity_id=2,
        relationship_type=RelationshipType.FRIEND,
        is_active=1
    )
    rel_repo.add(rel1)
    rel_repo.commit()
    
    rel2 = Relationship(
        universe_id=universe.id,
        source_entity_type="notable_figure",
        source_entity_id=2,
        target_entity_type="notable_figure",
        target_entity_id=3,
        relationship_type=RelationshipType.ENEMY,
        is_active=0
    )
    rel_repo.add(rel2)
    rel_repo.commit()
    
    # Test get_by_source
    source_rels = rel_repo.get_by_source("notable_figure", 1)
    assert len(source_rels) == 1
    print(f"   ✓ get_by_source: {len(source_rels)}")
    
    # Test get_by_target
    target_rels = rel_repo.get_by_target("notable_figure", 2)
    assert len(target_rels) == 1
    print(f"   ✓ get_by_target: {len(target_rels)}")
    
    # Test get_all_for_entity
    all_for_2 = rel_repo.get_all_for_entity("notable_figure", 2)
    assert len(all_for_2) == 2  # As source and target
    print(f"   ✓ get_all_for_entity: {len(all_for_2)}")
    
    # Test get_active_relationships
    active = rel_repo.get_active_relationships(universe.id)
    assert len(active) == 1
    print(f"   ✓ get_active_relationships: {len(active)}")
    
    # Test find_relationship
    found = rel_repo.find_relationship("notable_figure", 1, "notable_figure", 2)
    assert found is not None
    assert found.relationship_type == RelationshipType.FRIEND
    print(f"   ✓ find_relationship works")
    
    session.close()


def test_relationship_ui_components():
    """Test Relationship UI components."""
    from worldbuilder.views.relationship_dialog import RelationshipDialog
    from worldbuilder.views.relationship_list_view import RelationshipListView
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("\nTesting Relationship UI Components...")
    
    # Test RelationshipDialog
    dialog = RelationshipDialog(
        universe_id=1,
        source_info=("notable_figure", 1, "Aragorn"),
        target_info=("notable_figure", 2, "Arwen")
    )
    assert dialog.universe_id == 1
    assert not dialog.is_edit_mode
    print("   ✓ RelationshipDialog created")
    
    # Test RelationshipListView
    list_view = RelationshipListView()
    print("   ✓ RelationshipListView created")
    
    # Test with actual relationships
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_repo = UniverseRepository(session)
    universe_service = UniverseService(universe_repo)
    rel_repo = RelationshipRepository(session)
    rel_service = RelationshipService(rel_repo)
    
    universe = universe_service.create_universe(name="UI Test")
    
    rel = rel_service.create_relationship(
        universe_id=universe.id,
        source_type="notable_figure",
        source_id=1,
        target_type="notable_figure",
        target_id=2,
        relationship_type=RelationshipType.FRIEND
    )
    
    rels = rel_service.get_all_relationships(universe.id)
    list_view.load_relationships(rels)
    
    assert list_view.table.rowCount() == 1
    print(f"   ✓ List view loaded {len(rels)} relationship(s)")
    
    session.close()


if __name__ == "__main__":
    print("=" * 70)
    print("Running WorldBuilder Phase 6 Tests")
    print("=" * 70)
    
    test_relationship_model()
    test_relationship_crud()
    test_relationship_repository()
    test_relationship_ui_components()
    
    print("\n" + "=" * 70)
    print("✓ ALL PHASE 6 TESTS PASSED!")
    print("=" * 70)

"""Test Phase 9: Additional Entity Types (Organizations, Artifacts, Lore)."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from worldbuilder.database import (DatabaseManager, UniverseRepository, LocationRepository,
                                   OrganizationRepository, ArtifactRepository, LoreRepository)
from worldbuilder.services import (UniverseService, LocationService,
                                   OrganizationService, ArtifactService, LoreService)
from worldbuilder.models import (OrganizationType, ArtifactType, LoreType, LocationType)


def test_organizations():
    """Test Organization model and repository."""
    print("\nTesting Organizations...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_service = UniverseService(UniverseRepository(session))
    org_service = OrganizationService(OrganizationRepository(session))
    
    universe = universe_service.create_universe(name="Fantasy Realm")
    
    # Create various organizations
    print("\n1. Creating organizations...")
    kingdom = org_service.create_organization(
        "Kingdom of Avalon", universe.id, OrganizationType.KINGDOM,
        description="A prosperous kingdom", motto="Unity and Honor"
    )
    assert kingdom.id is not None
    assert kingdom.organization_type == OrganizationType.KINGDOM
    print(f"   ✓ Created kingdom: {kingdom.name}")
    
    guild = org_service.create_organization(
        "Mages Guild", universe.id, OrganizationType.GUILD,
        description="Guild of magical practitioners"
    )
    assert guild.id is not None
    print(f"   ✓ Created guild: {guild.name}")
    
    # Test retrieval
    print("\n2. Testing retrieval...")
    retrieved = org_service.get_organization(kingdom.id)
    assert retrieved.name == "Kingdom of Avalon"
    print(f"   ✓ Retrieved: {retrieved.name}")
    
    all_orgs = org_service.get_all_organizations(universe.id)
    assert len(all_orgs) == 2
    print(f"   ✓ Found {len(all_orgs)} organizations")
    
    kingdoms = org_service.get_by_type(universe.id, OrganizationType.KINGDOM)
    assert len(kingdoms) == 1
    print(f"   ✓ Filtered by type: {len(kingdoms)} kingdoms")
    
    # Test update
    print("\n3. Testing update...")
    kingdom.colors = "Blue and Gold"
    updated = org_service.update_organization(kingdom)
    assert updated.colors == "Blue and Gold"
    print(f"   ✓ Updated organization colors")
    
    # Test hierarchy
    print("\n4. Testing organization hierarchy...")
    regional_chapter = org_service.create_organization(
        "Avalon Chapter", universe.id, OrganizationType.GUILD,
        parent_organization_id=guild.id
    )
    assert regional_chapter.parent_organization_id == guild.id
    print(f"   ✓ Created child organization")
    
    session.close()


def test_artifacts():
    """Test Artifact model and repository."""
    print("\nTesting Artifacts...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_service = UniverseService(UniverseRepository(session))
    artifact_service = ArtifactService(ArtifactRepository(session))
    
    universe = universe_service.create_universe(name="Magic World")
    
    # Create artifacts
    print("\n1. Creating artifacts...")
    sword = artifact_service.create_artifact(
        "Excalibur", universe.id, ArtifactType.WEAPON,
        description="Legendary sword",
        material="Enchanted Steel",
        rarity="legendary"
    )
    sword.magical = True
    artifact_service.update_artifact(sword)
    assert sword.id is not None
    assert sword.magical is True
    print(f"   ✓ Created magical weapon: {sword.name}")
    
    book = artifact_service.create_artifact(
        "Book of Shadows", universe.id, ArtifactType.BOOK,
        description="Ancient spellbook"
    )
    book.magical = True
    book.cursed = True
    artifact_service.update_artifact(book)
    assert book.cursed is True
    print(f"   ✓ Created cursed book: {book.name}")
    
    # Test retrieval
    print("\n2. Testing retrieval...")
    retrieved = artifact_service.get_artifact(sword.id)
    assert retrieved.name == "Excalibur"
    print(f"   ✓ Retrieved: {retrieved.name}")
    
    all_artifacts = artifact_service.get_all_artifacts(universe.id)
    assert len(all_artifacts) == 2
    print(f"   ✓ Found {len(all_artifacts)} artifacts")
    
    magical = artifact_service.get_magical_artifacts(universe.id)
    assert len(magical) == 2
    print(f"   ✓ Found {len(magical)} magical artifacts")
    
    # Test properties
    print("\n3. Testing boolean properties...")
    assert sword.magical is True
    assert sword.sentient is False
    assert book.cursed is True
    print(f"   ✓ Boolean properties work correctly")
    
    session.close()


def test_lore():
    """Test Lore model and repository."""
    print("\nTesting Lore...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_service = UniverseService(UniverseRepository(session))
    lore_service = LoreService(LoreRepository(session))
    
    universe = universe_service.create_universe(name="Mythic Lands")
    
    # Create lore entries
    print("\n1. Creating lore entries...")
    myth = lore_service.create_lore(
        "The Great Flood", universe.id, LoreType.MYTH,
        description="Ancient tale of world-ending flood",
        summary="Gods punished mortals with a great flood"
    )
    myth.true = False  # It's just a myth
    lore_service.update_lore(myth)
    assert myth.id is not None
    assert myth.true is False
    print(f"   ✓ Created myth: {myth.name}")
    
    prophecy = lore_service.create_lore(
        "The Chosen One", universe.id, LoreType.PROPHECY,
        description="Prophecy of a hero",
        full_text="When darkness rises, a hero shall appear"
    )
    prophecy.true = None  # Unknown if true
    lore_service.update_lore(prophecy)
    assert prophecy.true is None
    print(f"   ✓ Created prophecy: {prophecy.name}")
    
    # Test retrieval
    print("\n2. Testing retrieval...")
    retrieved = lore_service.get_lore(myth.id)
    assert retrieved.name == "The Great Flood"
    print(f"   ✓ Retrieved: {retrieved.name}")
    
    all_lore = lore_service.get_all_lore(universe.id)
    assert len(all_lore) == 2
    print(f"   ✓ Found {len(all_lore)} lore entries")
    
    myths = lore_service.get_by_type(universe.id, LoreType.MYTH)
    assert len(myths) == 1
    print(f"   ✓ Filtered by type: {len(myths)} myths")
    
    # Test truth status
    print("\n3. Testing truth status...")
    assert myth.true is False
    assert prophecy.true is None
    print(f"   ✓ Truth status works correctly")
    
    session.close()


def test_integration():
    """Test integration between new entities."""
    print("\nTesting Integration...")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    session = db_manager.get_session()
    
    universe_service = UniverseService(UniverseRepository(session))
    location_service = LocationService(LocationRepository(session))
    org_service = OrganizationService(OrganizationRepository(session))
    artifact_service = ArtifactService(ArtifactRepository(session))
    lore_service = LoreService(LoreRepository(session))
    
    universe = universe_service.create_universe(name="Test World")
    capital = location_service.create_location("Capital City", universe.id, LocationType.CITY)
    
    # Create organization with headquarters
    print("\n1. Testing organization with location...")
    kingdom = org_service.create_organization(
        "Test Kingdom", universe.id, OrganizationType.KINGDOM,
        headquarters_location_id=capital.id
    )
    assert kingdom.headquarters_location_id == capital.id
    print(f"   ✓ Organization linked to location")
    
    # Create artifact at location
    print("\n2. Testing artifact at location...")
    crown = artifact_service.create_artifact(
        "Royal Crown", universe.id, ArtifactType.JEWELRY,
        current_location_id=capital.id
    )
    assert crown.current_location_id == capital.id
    print(f"   ✓ Artifact linked to location")
    
    # Create lore about location
    print("\n3. Testing lore about location...")
    legend = lore_service.create_lore(
        "Founding of the Capital", universe.id, LoreType.LEGEND,
        origin_location_id=capital.id
    )
    assert legend.origin_location_id == capital.id
    print(f"   ✓ Lore linked to location")
    
    # Test complex relationships
    print("\n4. Testing complex relationships...")
    lore_about_org = lore_service.create_lore(
        "Kingdom's Origin", universe.id, LoreType.HISTORICAL_ACCOUNT,
        origin_organization_id=kingdom.id
    )
    assert lore_about_org.origin_organization_id == kingdom.id
    print(f"   ✓ Lore linked to organization")
    
    session.close()


if __name__ == "__main__":
    print("=" * 70)
    print("Running WorldBuilder Phase 9 Tests")
    print("=" * 70)
    
    test_organizations()
    test_artifacts()
    test_lore()
    test_integration()
    
    print("\n" + "=" * 70)
    print("✓ ALL PHASE 9 TESTS PASSED!")
    print("=" * 70)

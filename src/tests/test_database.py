"""Test basic database functionality."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from worldbuilder.database import DatabaseManager
from worldbuilder.models import Universe


def test_database_creation():
    """Test database and table creation."""
    db_manager = DatabaseManager()  # In-memory database
    db_manager.create_tables()
    print("✓ Database tables created successfully")


def test_universe_creation():
    """Test creating and retrieving a universe."""
    db_manager = DatabaseManager()
    db_manager.create_tables()
    
    session = db_manager.get_session()
    
    # Create a universe
    universe = Universe(
        name="Test Universe",
        description="A test fictional universe",
        author="Test Author",
        genre="Fantasy"
    )
    
    session.add(universe)
    session.commit()
    
    # Retrieve it
    retrieved = session.query(Universe).filter_by(name="Test Universe").first()
    
    assert retrieved is not None
    assert retrieved.name == "Test Universe"
    assert retrieved.author == "Test Author"
    assert retrieved.genre == "Fantasy"
    
    print(f"✓ Universe created and retrieved: {retrieved}")
    
    session.close()


if __name__ == "__main__":
    print("Running WorldBuilder tests...\n")
    test_database_creation()
    test_universe_creation()
    print("\n✓ All tests passed!")

"""Database manager for SQLAlchemy connections and sessions."""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from worldbuilder.models import Base


class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self, db_path: str = None):
        """Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file. If None, uses in-memory database.
        """
        if db_path:
            db_url = f"sqlite:///{db_path}"
        else:
            db_url = "sqlite:///:memory:"
        
        self.engine = create_engine(db_url, echo=False)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
    
    def create_tables(self):
        """Create all tables defined in models."""
        Base.metadata.create_all(self.engine)
    
    def drop_tables(self):
        """Drop all tables."""
        Base.metadata.drop_all(self.engine)
    
    def get_session(self):
        """Get a new database session."""
        return self.Session()
    
    def close_session(self):
        """Close current session."""
        self.Session.remove()

"""Universe repository for data access operations."""
from typing import List, Optional
from worldbuilder.database.repository import BaseRepository
from worldbuilder.models.universe import Universe


class UniverseRepository(BaseRepository[Universe]):
    """Repository for Universe entity operations."""
    
    def __init__(self, session):
        super().__init__(session, Universe)
    
    def get_active_universes(self) -> List[Universe]:
        """Get all active universes."""
        return self.session.query(Universe).filter_by(is_active=True).all()
    
    def get_by_name(self, name: str) -> Optional[Universe]:
        """Get universe by name."""
        return self.session.query(Universe).filter_by(name=name).first()
    
    def search_by_name(self, search_term: str) -> List[Universe]:
        """Search universes by name (case-insensitive)."""
        return self.session.query(Universe).filter(
            Universe.name.ilike(f"%{search_term}%")
        ).all()

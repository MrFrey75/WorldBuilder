"""Notable Figure repository for data access operations."""
from typing import List, Optional
from sqlalchemy import and_
from worldbuilder.database.repository import BaseRepository
from worldbuilder.models.notable_figure import NotableFigure


class NotableFigureRepository(BaseRepository[NotableFigure]):
    """Repository for NotableFigure entity operations."""
    
    def __init__(self, session):
        super().__init__(session, NotableFigure)
    
    def get_by_universe(self, universe_id: int) -> List[NotableFigure]:
        """Get all notable figures in a universe.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            List of notable figures
        """
        return self.session.query(NotableFigure).filter_by(universe_id=universe_id).all()
    
    def get_by_species(self, species_id: int) -> List[NotableFigure]:
        """Get figures of a specific species.
        
        Args:
            species_id: Species ID
            
        Returns:
            List of figures
        """
        return self.session.query(NotableFigure).filter_by(species_id=species_id).all()
    
    def get_by_location(self, location_id: int) -> List[NotableFigure]:
        """Get figures at a specific location.
        
        Args:
            location_id: Location ID
            
        Returns:
            List of figures
        """
        return self.session.query(NotableFigure).filter_by(location_id=location_id).all()
    
    def get_by_occupation(self, universe_id: int, occupation: str) -> List[NotableFigure]:
        """Get figures by occupation.
        
        Args:
            universe_id: Universe ID
            occupation: Occupation to filter by
            
        Returns:
            List of figures
        """
        return self.session.query(NotableFigure).filter(
            and_(
                NotableFigure.universe_id == universe_id,
                NotableFigure.occupation.ilike(f"%{occupation}%")
            )
        ).all()
    
    def search_by_name(self, universe_id: int, search_term: str) -> List[NotableFigure]:
        """Search figures by name in a universe.
        
        Args:
            universe_id: Universe ID
            search_term: Search term
            
        Returns:
            List of matching figures
        """
        return self.session.query(NotableFigure).filter(
            and_(
                NotableFigure.universe_id == universe_id,
                NotableFigure.name.ilike(f"%{search_term}%")
            )
        ).all()

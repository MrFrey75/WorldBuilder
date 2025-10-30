"""Species repository for data access operations."""
from typing import List, Optional
from sqlalchemy import and_
from worldbuilder.database.repository import BaseRepository
from worldbuilder.models.species import Species, SpeciesType


class SpeciesRepository(BaseRepository[Species]):
    """Repository for Species entity operations."""
    
    def __init__(self, session):
        super().__init__(session, Species)
    
    def get_by_universe(self, universe_id: int) -> List[Species]:
        """Get all species in a universe.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            List of species
        """
        return self.session.query(Species).filter_by(universe_id=universe_id).all()
    
    def get_by_type(self, universe_id: int, species_type: SpeciesType) -> List[Species]:
        """Get species by type.
        
        Args:
            universe_id: Universe ID
            species_type: Type of species
            
        Returns:
            List of species of given type
        """
        return self.session.query(Species).filter(
            and_(
                Species.universe_id == universe_id,
                Species.species_type == species_type
            )
        ).all()
    
    def get_playable_species(self, universe_id: int) -> List[Species]:
        """Get all playable species in a universe.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            List of playable species
        """
        return self.session.query(Species).filter(
            and_(
                Species.universe_id == universe_id,
                Species.is_playable == True
            )
        ).all()
    
    def search_by_name(self, universe_id: int, search_term: str) -> List[Species]:
        """Search species by name in a universe.
        
        Args:
            universe_id: Universe ID
            search_term: Search term
            
        Returns:
            List of matching species
        """
        return self.session.query(Species).filter(
            and_(
                Species.universe_id == universe_id,
                Species.name.ilike(f"%{search_term}%")
            )
        ).all()
    
    def get_by_name(self, universe_id: int, name: str) -> Optional[Species]:
        """Get species by exact name.
        
        Args:
            universe_id: Universe ID
            name: Species name
            
        Returns:
            Species or None
        """
        return self.session.query(Species).filter(
            and_(
                Species.universe_id == universe_id,
                Species.name == name
            )
        ).first()

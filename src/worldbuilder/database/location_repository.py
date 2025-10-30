"""Location repository for data access operations."""
from typing import List, Optional
from sqlalchemy import and_
from worldbuilder.database.repository import BaseRepository
from worldbuilder.models.location import Location, LocationType


class LocationRepository(BaseRepository[Location]):
    """Repository for Location entity operations."""
    
    def __init__(self, session):
        super().__init__(session, Location)
    
    def get_by_universe(self, universe_id: int) -> List[Location]:
        """Get all locations in a universe.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            List of locations
        """
        return self.session.query(Location).filter_by(universe_id=universe_id).all()
    
    def get_root_locations(self, universe_id: int) -> List[Location]:
        """Get all root (top-level) locations in a universe.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            List of root locations (those without parents)
        """
        return self.session.query(Location).filter(
            and_(
                Location.universe_id == universe_id,
                Location.parent_id == None
            )
        ).all()
    
    def get_children(self, parent_id: int) -> List[Location]:
        """Get direct children of a location.
        
        Args:
            parent_id: Parent location ID
            
        Returns:
            List of child locations
        """
        return self.session.query(Location).filter_by(parent_id=parent_id).all()
    
    def get_by_type(self, universe_id: int, location_type: LocationType) -> List[Location]:
        """Get locations by type.
        
        Args:
            universe_id: Universe ID
            location_type: Type of location
            
        Returns:
            List of locations of given type
        """
        return self.session.query(Location).filter(
            and_(
                Location.universe_id == universe_id,
                Location.location_type == location_type
            )
        ).all()
    
    def search_by_name(self, universe_id: int, search_term: str) -> List[Location]:
        """Search locations by name in a universe.
        
        Args:
            universe_id: Universe ID
            search_term: Search term
            
        Returns:
            List of matching locations
        """
        return self.session.query(Location).filter(
            and_(
                Location.universe_id == universe_id,
                Location.name.ilike(f"%{search_term}%")
            )
        ).all()
    
    def has_children(self, location_id: int) -> bool:
        """Check if location has children.
        
        Args:
            location_id: Location ID
            
        Returns:
            True if location has children
        """
        count = self.session.query(Location).filter_by(parent_id=location_id).count()
        return count > 0
    
    def delete_with_children(self, location_id: int) -> int:
        """Delete location and all its descendants.
        
        Args:
            location_id: Location ID
            
        Returns:
            Number of locations deleted
        """
        location = self.get_by_id(location_id)
        if not location:
            return 0
        
        # Get all descendants
        descendants = location.get_all_descendants()
        count = len(descendants) + 1
        
        # Delete all descendants
        for descendant in descendants:
            self.session.delete(descendant)
        
        # Delete the location itself
        self.session.delete(location)
        
        return count

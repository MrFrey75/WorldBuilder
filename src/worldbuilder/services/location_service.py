"""Location service for business logic operations."""
from typing import List, Optional
from worldbuilder.models.location import Location, LocationType
from worldbuilder.database.location_repository import LocationRepository


class LocationService:
    """Service layer for Location business logic."""
    
    def __init__(self, repository: LocationRepository):
        self.repository = repository
    
    def create_location(self, name: str, universe_id: int, 
                       location_type: LocationType = LocationType.OTHER,
                       description: str = None, parent_id: int = None) -> Location:
        """Create a new location.
        
        Args:
            name: Location name (required)
            universe_id: Universe ID (required)
            location_type: Type of location
            description: Location description
            parent_id: Parent location ID (None for root)
            
        Returns:
            Created Location entity
            
        Raises:
            ValueError: If validation fails
        """
        if not name or not name.strip():
            raise ValueError("Location name cannot be empty")
        
        if not universe_id:
            raise ValueError("Universe ID is required")
        
        # Validate parent exists if provided
        if parent_id:
            parent = self.repository.get_by_id(parent_id)
            if not parent:
                raise ValueError(f"Parent location with ID {parent_id} not found")
            
            # Validate parent is in same universe
            if parent.universe_id != universe_id:
                raise ValueError("Parent location must be in the same universe")
        
        location = Location(
            name=name.strip(),
            universe_id=universe_id,
            location_type=location_type,
            description=description,
            parent_id=parent_id
        )
        
        self.repository.add(location)
        self.repository.commit()
        
        return location
    
    def get_location(self, location_id: int) -> Optional[Location]:
        """Get location by ID."""
        return self.repository.get_by_id(location_id)
    
    def get_all_locations(self, universe_id: int) -> List[Location]:
        """Get all locations in a universe."""
        return self.repository.get_by_universe(universe_id)
    
    def get_root_locations(self, universe_id: int) -> List[Location]:
        """Get root locations (no parent) in a universe."""
        return self.repository.get_root_locations(universe_id)
    
    def get_children(self, parent_id: int) -> List[Location]:
        """Get direct children of a location."""
        return self.repository.get_children(parent_id)
    
    def get_by_type(self, universe_id: int, location_type: LocationType) -> List[Location]:
        """Get locations by type."""
        return self.repository.get_by_type(universe_id, location_type)
    
    def update_location(self, location_id: int, name: str = None,
                       description: str = None, location_type: LocationType = None,
                       parent_id: int = None) -> Optional[Location]:
        """Update a location.
        
        Args:
            location_id: Location ID
            name: New name (optional)
            description: New description (optional)
            location_type: New type (optional)
            parent_id: New parent ID (optional, use -1 to remove parent)
            
        Returns:
            Updated Location or None if not found
            
        Raises:
            ValueError: If validation fails
        """
        location = self.repository.get_by_id(location_id)
        if not location:
            return None
        
        if name is not None and name.strip():
            location.name = name.strip()
        
        if description is not None:
            location.description = description
        
        if location_type is not None:
            location.location_type = location_type
        
        if parent_id is not None:
            if parent_id == -1:
                # Remove parent (make it root)
                location.parent_id = None
            else:
                # Validate new parent
                new_parent = self.repository.get_by_id(parent_id)
                if not new_parent:
                    raise ValueError(f"Parent location with ID {parent_id} not found")
                
                # Check for circular reference
                if new_parent.id == location.id:
                    raise ValueError("Location cannot be its own parent")
                
                if location.is_ancestor_of(new_parent):
                    raise ValueError("Cannot set descendant as parent (circular reference)")
                
                # Validate same universe
                if new_parent.universe_id != location.universe_id:
                    raise ValueError("Parent must be in the same universe")
                
                location.parent_id = parent_id
        
        self.repository.update(location)
        self.repository.commit()
        
        return location
    
    def delete_location(self, location_id: int, cascade: bool = False) -> bool:
        """Delete a location.
        
        Args:
            location_id: Location ID
            cascade: If True, delete children too; if False, fail if has children
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If location has children and cascade is False
        """
        location = self.repository.get_by_id(location_id)
        if not location:
            return False
        
        if not cascade and self.repository.has_children(location_id):
            raise ValueError("Location has children. Use cascade=True to delete all descendants.")
        
        if cascade:
            self.repository.delete_with_children(location_id)
        else:
            self.repository.delete(location_id)
        
        self.repository.commit()
        return True
    
    def search_locations(self, universe_id: int, search_term: str) -> List[Location]:
        """Search locations by name.
        
        Args:
            universe_id: Universe ID
            search_term: Search term
            
        Returns:
            List of matching locations
        """
        return self.repository.search_by_name(universe_id, search_term)
    
    def move_location(self, location_id: int, new_parent_id: Optional[int]) -> Location:
        """Move a location to a new parent.
        
        Args:
            location_id: Location to move
            new_parent_id: New parent ID (None for root)
            
        Returns:
            Updated location
        """
        return self.update_location(location_id, parent_id=new_parent_id if new_parent_id else -1)

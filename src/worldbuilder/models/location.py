"""Location model for hierarchical places in universes."""
from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from worldbuilder.models.base_entity import BaseEntity
from worldbuilder.enums import LocationType


class Location(BaseEntity):
    """Represents a location in a universe with hierarchical structure."""
    
    __tablename__ = "locations"
    
    # Foreign keys
    universe_id = Column(Integer, ForeignKey("universes.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    
    # Location attributes
    location_type = Column(SQLEnum(LocationType), nullable=False, default=LocationType.OTHER)
    
    # Relationships
    universe = relationship("Universe", backref="locations")
    parent = relationship("Location", remote_side="Location.id", backref="children")
    
    def __repr__(self):
        parent_name = self.parent.name if self.parent else "None"
        return f"<Location(id={self.id}, name='{self.name}', type={self.location_type.value}, parent='{parent_name}')>"
    
    def get_full_path(self) -> str:
        """Get full hierarchical path of location.
        
        Returns:
            String like "Continent > Region > City"
        """
        path = [self.name]
        current = self.parent
        while current:
            path.insert(0, current.name)
            current = current.parent
        return " > ".join(path)
    
    def get_depth(self) -> int:
        """Get depth in hierarchy (0 for root locations).
        
        Returns:
            Depth level
        """
        depth = 0
        current = self.parent
        while current:
            depth += 1
            current = current.parent
        return depth
    
    def is_ancestor_of(self, other: 'Location') -> bool:
        """Check if this location is an ancestor of another.
        
        Args:
            other: Location to check
            
        Returns:
            True if this is an ancestor of other
        """
        current = other.parent
        while current:
            if current.id == self.id:
                return True
            current = current.parent
        return False
    
    def get_all_descendants(self) -> list:
        """Get all descendant locations recursively.
        
        Returns:
            List of all descendant locations
        """
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants

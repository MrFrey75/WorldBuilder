"""Notable Figure model for characters in universes."""
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from worldbuilder.models.base_entity import BaseEntity


class NotableFigure(BaseEntity):
    """Represents a notable figure/character in a universe."""
    
    __tablename__ = "notable_figures"
    
    # Foreign keys
    universe_id = Column(Integer, ForeignKey("universes.id"), nullable=False)
    species_id = Column(Integer, ForeignKey("species.id"), nullable=True)  # Defaults to Human
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)  # Associated location
    
    # Figure attributes
    title = Column(String(255), nullable=True)  # e.g., "King", "Lord", "Doctor"
    age = Column(String(50), nullable=True)  # String to allow ranges or "unknown"
    occupation = Column(String(255), nullable=True)
    
    # Additional attributes stored as JSON
    # Example: {"hair_color": "blonde", "eye_color": "blue", "height": "6 feet"}
    attributes = Column(JSON, nullable=True)
    
    # Backstory and details
    backstory = Column(Text, nullable=True)
    personality = Column(Text, nullable=True)
    goals = Column(Text, nullable=True)
    
    # Relationships
    universe = relationship("Universe", backref="notable_figures")
    species = relationship("Species", backref="figures")
    location = relationship("Location", backref="figures")
    
    def __repr__(self):
        species_name = self.species.name if self.species else "Unknown"
        full_name = f"{self.title} {self.name}" if self.title else self.name
        return f"<NotableFigure(id={self.id}, name='{full_name}', species='{species_name}')>"
    
    def get_full_name(self) -> str:
        """Get full name with title.
        
        Returns:
            Full name including title if present
        """
        if self.title:
            return f"{self.title} {self.name}"
        return self.name
    
    def get_attribute(self, attr_name: str, default=None):
        """Get a specific attribute.
        
        Args:
            attr_name: Name of the attribute
            default: Default value if attribute not found
            
        Returns:
            Attribute value or default
        """
        if not self.attributes:
            return default
        return self.attributes.get(attr_name, default)
    
    def set_attribute(self, attr_name: str, value):
        """Set an attribute.
        
        Args:
            attr_name: Name of the attribute
            value: Value to set
        """
        if not self.attributes:
            self.attributes = {}
        self.attributes[attr_name] = value
    
    def get_summary(self) -> str:
        """Get a one-line summary of the figure.
        
        Returns:
            Summary string
        """
        parts = [self.get_full_name()]
        
        if self.occupation:
            parts.append(self.occupation)
        
        if self.species:
            parts.append(self.species.name)
        
        if self.age:
            parts.append(f"Age {self.age}")
        
        if self.location:
            parts.append(f"of {self.location.name}")
        
        return ", ".join(parts)

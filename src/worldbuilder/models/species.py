"""Species/Race model for defining creature types in universes."""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from enum import Enum
from worldbuilder.models.base_entity import BaseEntity


class SpeciesType(Enum):
    """Classification types for species."""
    SENTIENT = "Sentient"
    NON_SENTIENT = "Non-Sentient"
    MAGICAL = "Magical"
    DIVINE = "Divine"
    UNDEAD = "Undead"
    CONSTRUCT = "Construct"
    HYBRID = "Hybrid"
    OTHER = "Other"


class Species(BaseEntity):
    """Represents a species or race in a universe."""
    
    __tablename__ = "species"
    
    # Foreign keys
    universe_id = Column(Integer, ForeignKey("universes.id"), nullable=False)
    
    # Species attributes
    species_type = Column(SQLEnum(SpeciesType), nullable=False, default=SpeciesType.SENTIENT)
    is_playable = Column(Boolean, default=True, nullable=False)  # Can be used for characters
    
    # Physical characteristics (stored as JSON for flexibility)
    # Example: {"height": "5-6 feet", "lifespan": "80 years", "build": "Medium"}
    physical_traits = Column(JSON, nullable=True)
    
    # Abilities and characteristics
    abilities = Column(Text, nullable=True)
    culture = Column(Text, nullable=True)
    
    # Relationships
    universe = relationship("Universe", backref="species")
    
    def __repr__(self):
        return f"<Species(id={self.id}, name='{self.name}', type={self.species_type.value})>"
    
    def get_trait(self, trait_name: str, default=None):
        """Get a specific physical trait.
        
        Args:
            trait_name: Name of the trait
            default: Default value if trait not found
            
        Returns:
            Trait value or default
        """
        if not self.physical_traits:
            return default
        return self.physical_traits.get(trait_name, default)
    
    def set_trait(self, trait_name: str, value):
        """Set a physical trait.
        
        Args:
            trait_name: Name of the trait
            value: Value to set
        """
        if not self.physical_traits:
            self.physical_traits = {}
        self.physical_traits[trait_name] = value
    
    @staticmethod
    def create_default_human(universe_id: int) -> 'Species':
        """Create a default human species.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            Human species instance (not saved)
        """
        human = Species(
            name="Human",
            universe_id=universe_id,
            species_type=SpeciesType.SENTIENT,
            is_playable=True,
            description="The standard human race",
            physical_traits={
                "height": "5-6 feet",
                "lifespan": "70-100 years",
                "build": "Medium",
                "skin_tones": "Varied",
                "hair_colors": "Varied"
            },
            abilities="Adaptable, versatile, quick learners",
            culture="Highly diverse, varies by region and time period"
        )
        return human

"""Artifact model for magical items, relics, weapons, etc."""
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from worldbuilder.models.base_entity import Base


class ArtifactType(str, Enum):
    """Types of artifacts."""
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    TOOL = "tool"
    BOOK = "book"
    SCROLL = "scroll"
    POTION = "potion"
    RELIC = "relic"
    ARTIFACT = "artifact"
    MAGICAL_ITEM = "magical_item"
    TECHNOLOGY = "technology"
    VEHICLE = "vehicle"
    BUILDING = "building"
    TREASURE = "treasure"
    ART = "art"
    JEWELRY = "jewelry"
    OTHER = "other"


class Artifact(Base):
    """Artifact entity (items, relics, magical objects, etc.)."""
    
    __tablename__ = 'artifacts'
    
    id = Column(Integer, primary_key=True)
    universe_id = Column(Integer, ForeignKey('universes.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(200), nullable=False)
    artifact_type = Column(SQLEnum(ArtifactType), nullable=False)
    description = Column(Text)
    
    # Artifact details
    appearance = Column(Text)
    material = Column(String(200))
    origin_story = Column(Text)
    powers_abilities = Column(Text)
    
    # Status and location
    current_location_id = Column(Integer, ForeignKey('locations.id', ondelete='SET NULL'))
    current_owner_id = Column(Integer, ForeignKey('notable_figures.id', ondelete='SET NULL'))
    creator_id = Column(Integer, ForeignKey('notable_figures.id', ondelete='SET NULL'))
    
    # Characteristics
    is_magical = Column(Integer, default=0)  # SQLite uses integers for booleans
    is_sentient = Column(Integer, default=0)
    is_cursed = Column(Integer, default=0)
    rarity = Column(String(50))  # common, uncommon, rare, legendary, etc.
    
    # Historical info
    created_date = Column(String(200))
    discovered_date = Column(String(200))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # SQLAlchemy relationships
    universe = relationship("Universe", backref="artifacts")
    current_location = relationship("Location", foreign_keys=[current_location_id])
    current_owner = relationship("NotableFigure", foreign_keys=[current_owner_id])
    creator = relationship("NotableFigure", foreign_keys=[creator_id])
    
    def __repr__(self):
        return f"<Artifact(id={self.id}, name='{self.name}', type={self.artifact_type.value})>"
    
    @property
    def magical(self) -> bool:
        """Get magical status as boolean."""
        return bool(self.is_magical)
    
    @magical.setter
    def magical(self, value: bool):
        """Set magical status."""
        self.is_magical = 1 if value else 0
    
    @property
    def sentient(self) -> bool:
        """Get sentient status as boolean."""
        return bool(self.is_sentient)
    
    @sentient.setter
    def sentient(self, value: bool):
        """Set sentient status."""
        self.is_sentient = 1 if value else 0
    
    @property
    def cursed(self) -> bool:
        """Get cursed status as boolean."""
        return bool(self.is_cursed)
    
    @cursed.setter
    def cursed(self, value: bool):
        """Set cursed status."""
        self.is_cursed = 1 if value else 0

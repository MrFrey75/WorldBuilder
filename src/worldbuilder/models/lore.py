"""Lore model for mythology, legends, stories, and beliefs."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from worldbuilder.models.base_entity import Base
from worldbuilder.enums import LoreType


class Lore(Base):
    """Lore entity (myths, legends, beliefs, etc.)."""
    
    __tablename__ = 'lore'
    
    id = Column(Integer, primary_key=True)
    universe_id = Column(Integer, ForeignKey('universes.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(200), nullable=False)
    lore_type = Column(SQLEnum(LoreType), nullable=False)
    description = Column(Text)
    
    # Lore details
    full_text = Column(Text)
    summary = Column(Text)
    moral_lesson = Column(Text)
    symbolism = Column(Text)
    
    # Context
    origin_location_id = Column(Integer, ForeignKey('locations.id', ondelete='SET NULL'))
    origin_species_id = Column(Integer, ForeignKey('species.id', ondelete='SET NULL'))
    origin_organization_id = Column(Integer, ForeignKey('organizations.id', ondelete='SET NULL'))
    
    # Historical context
    time_period = Column(String(200))
    author_id = Column(Integer, ForeignKey('notable_figures.id', ondelete='SET NULL'))
    
    # Veracity
    is_true = Column(Integer)  # NULL=unknown, 0=false, 1=true
    belief_level = Column(String(50))  # widespread, regional, obscure, forgotten, etc.
    
    # Related entities (described in text but may reference real entities)
    related_figures = Column(Text)  # Comma-separated or JSON
    related_locations = Column(Text)
    related_events = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # SQLAlchemy relationships
    universe = relationship("Universe", backref="lore")
    origin_location = relationship("Location", foreign_keys=[origin_location_id])
    origin_species = relationship("Species", foreign_keys=[origin_species_id])
    origin_organization = relationship("Organization", foreign_keys=[origin_organization_id])
    author = relationship("NotableFigure", foreign_keys=[author_id])
    
    def __repr__(self):
        return f"<Lore(id={self.id}, name='{self.name}', type={self.lore_type.value})>"
    
    @property
    def true(self) -> bool:
        """Get truth status as boolean (None if unknown)."""
        if self.is_true is None:
            return None
        return bool(self.is_true)
    
    @true.setter
    def true(self, value):
        """Set truth status."""
        if value is None:
            self.is_true = None
        else:
            self.is_true = 1 if value else 0

"""Organization model for groups, guilds, kingdoms, etc."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from worldbuilder.models.base_entity import Base
from worldbuilder.enums import OrganizationType


class Organization(Base):
    """Organization entity (kingdoms, guilds, factions, etc.)."""
    
    __tablename__ = 'organizations'
    
    id = Column(Integer, primary_key=True)
    universe_id = Column(Integer, ForeignKey('universes.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(200), nullable=False)
    organization_type = Column(SQLEnum(OrganizationType), nullable=False)
    description = Column(Text)
    
    # Organization details
    motto = Column(String(500))
    symbol_description = Column(Text)
    colors = Column(String(200))
    headquarters_location_id = Column(Integer, ForeignKey('locations.id', ondelete='SET NULL'))
    
    # Status
    is_active = Column(Integer, default=1)  # SQLite uses integers for booleans
    founded_date = Column(String(200))
    dissolved_date = Column(String(200))
    
    # Leadership
    current_leader_id = Column(Integer, ForeignKey('notable_figures.id', ondelete='SET NULL'))
    leadership_structure = Column(Text)
    
    # Relationships
    parent_organization_id = Column(Integer, ForeignKey('organizations.id', ondelete='SET NULL'))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # SQLAlchemy relationships
    universe = relationship("Universe", backref="organizations")
    headquarters = relationship("Location", foreign_keys=[headquarters_location_id])
    leader = relationship("NotableFigure", foreign_keys=[current_leader_id])
    parent = relationship("Organization", remote_side=[id], foreign_keys=[parent_organization_id])
    children = relationship("Organization", foreign_keys=[parent_organization_id], 
                          remote_side=[parent_organization_id], overlaps="parent")
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}', type={self.organization_type.value})>"
    
    @property
    def active(self) -> bool:
        """Get active status as boolean."""
        return bool(self.is_active)
    
    @active.setter
    def active(self, value: bool):
        """Set active status."""
        self.is_active = 1 if value else 0

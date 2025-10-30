"""Relationship model for connections between entities."""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime
from worldbuilder.models.base_entity import Base


class RelationshipType(Enum):
    """Types of relationships between entities."""
    # Family relationships
    PARENT = "Parent"
    CHILD = "Child"
    SIBLING = "Sibling"
    SPOUSE = "Spouse"
    RELATIVE = "Relative"
    
    # Social relationships
    FRIEND = "Friend"
    ENEMY = "Enemy"
    ALLY = "Ally"
    RIVAL = "Rival"
    MENTOR = "Mentor"
    STUDENT = "Student"
    
    # Professional relationships
    EMPLOYER = "Employer"
    EMPLOYEE = "Employee"
    COLLEAGUE = "Colleague"
    BUSINESS_PARTNER = "Business Partner"
    
    # Political relationships
    RULER = "Ruler"
    SUBJECT = "Subject"
    DIPLOMAT = "Diplomat"
    
    # Location relationships
    RESIDENT = "Resident"
    OWNER = "Owner"
    VISITOR = "Visitor"
    
    # Other
    CREATOR = "Creator"
    CREATION = "Creation"
    MEMBER = "Member"
    LEADER = "Leader"
    CUSTOM = "Custom"


class RelationshipStrength(Enum):
    """Strength/intensity of relationship."""
    WEAK = "Weak"
    MODERATE = "Moderate"
    STRONG = "Strong"
    VERY_STRONG = "Very Strong"


class Relationship(Base):
    """Represents a relationship between two entities."""
    
    __tablename__ = "relationships"
    
    # IDs
    id = Column(Integer, primary_key=True)
    universe_id = Column(Integer, ForeignKey("universes.id"), nullable=False)
    
    # Source entity (the "subject" of the relationship)
    source_entity_type = Column(String(50), nullable=False)  # e.g., "notable_figure", "location"
    source_entity_id = Column(Integer, nullable=False)
    
    # Target entity (the "object" of the relationship)
    target_entity_type = Column(String(50), nullable=False)
    target_entity_id = Column(Integer, nullable=False)
    
    # Relationship properties
    relationship_type = Column(SQLEnum(RelationshipType), nullable=False)
    custom_type_name = Column(String(100), nullable=True)  # Used when type is CUSTOM
    strength = Column(SQLEnum(RelationshipStrength), nullable=True, default=RelationshipStrength.MODERATE)
    
    # Additional details
    description = Column(Text, nullable=True)
    start_date = Column(String(100), nullable=True)  # Flexible date string
    end_date = Column(String(100), nullable=True)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = historical/ended
    
    # Timestamps
    created_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String(50), default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    universe = relationship("Universe", backref="relationships")
    
    def __repr__(self):
        type_name = self.custom_type_name if self.relationship_type == RelationshipType.CUSTOM else self.relationship_type.value
        return f"<Relationship(id={self.id}, {self.source_entity_type}:{self.source_entity_id} --{type_name}--> {self.target_entity_type}:{self.target_entity_id})>"
    
    def get_type_display(self) -> str:
        """Get display name for relationship type.
        
        Returns:
            Display name of relationship type
        """
        if self.relationship_type == RelationshipType.CUSTOM and self.custom_type_name:
            return self.custom_type_name
        return self.relationship_type.value
    
    def get_inverse_type(self) -> RelationshipType:
        """Get the inverse relationship type if applicable.
        
        Returns:
            Inverse relationship type or same type
        """
        inverses = {
            RelationshipType.PARENT: RelationshipType.CHILD,
            RelationshipType.CHILD: RelationshipType.PARENT,
            RelationshipType.EMPLOYER: RelationshipType.EMPLOYEE,
            RelationshipType.EMPLOYEE: RelationshipType.EMPLOYER,
            RelationshipType.RULER: RelationshipType.SUBJECT,
            RelationshipType.SUBJECT: RelationshipType.RULER,
            RelationshipType.MENTOR: RelationshipType.STUDENT,
            RelationshipType.STUDENT: RelationshipType.MENTOR,
            RelationshipType.CREATOR: RelationshipType.CREATION,
            RelationshipType.CREATION: RelationshipType.CREATOR,
        }
        return inverses.get(self.relationship_type, self.relationship_type)
    
    def is_bidirectional(self) -> bool:
        """Check if relationship type is bidirectional (same in both directions).
        
        Returns:
            True if relationship is the same in both directions
        """
        bidirectional_types = {
            RelationshipType.SIBLING,
            RelationshipType.SPOUSE,
            RelationshipType.FRIEND,
            RelationshipType.ENEMY,
            RelationshipType.ALLY,
            RelationshipType.RIVAL,
            RelationshipType.COLLEAGUE,
            RelationshipType.BUSINESS_PARTNER,
            RelationshipType.DIPLOMAT,
        }
        return self.relationship_type in bidirectional_types

"""Relationship-related enumerations."""
from enum import Enum


class RelationshipType(Enum):
    """Types of relationships between entities."""
    UNKWNOWN = "unknown"
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

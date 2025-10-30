"""Event model for historical events in universes."""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from enum import Enum
from datetime import datetime
from worldbuilder.models.base_entity import Base


class EventType(Enum):
    """Types/categories of events."""
    BIRTH = "Birth"
    DEATH = "Death"
    BATTLE = "Battle"
    WAR = "War"
    CORONATION = "Coronation"
    MARRIAGE = "Marriage"
    DISCOVERY = "Discovery"
    INVENTION = "Invention"
    FOUNDING = "Founding"
    DESTRUCTION = "Destruction"
    MEETING = "Meeting"
    TREATY = "Treaty"
    PROPHECY = "Prophecy"
    QUEST = "Quest"
    NATURAL_DISASTER = "Natural Disaster"
    POLITICAL = "Political Event"
    CULTURAL = "Cultural Event"
    RELIGIOUS = "Religious Event"
    OTHER = "Other"


class EventImportance(Enum):
    """Significance levels for events."""
    MINOR = "Minor"
    MODERATE = "Moderate"
    MAJOR = "Major"
    CRITICAL = "Critical"
    LEGENDARY = "Legendary"


class DatePrecision(Enum):
    """Precision levels for event dates."""
    EXACT = "Exact Date/Time"
    DAY = "Specific Day"
    MONTH = "Specific Month"
    YEAR = "Specific Year"
    DECADE = "Decade"
    CENTURY = "Century"
    ERA = "Era/Period"
    APPROXIMATE = "Approximate"
    RELATIVE = "Relative to Other Event"
    UNKNOWN = "Unknown"


class Event(Base):
    """Represents a historical event in a universe."""
    
    __tablename__ = "events"
    
    # IDs
    id = Column(Integer, primary_key=True)
    universe_id = Column(Integer, ForeignKey("universes.id"), nullable=False)
    name = Column(String(255), nullable=False)
    
    # Event properties
    event_type = Column(SQLEnum(EventType), nullable=False, default=EventType.OTHER)
    importance = Column(SQLEnum(EventImportance), nullable=False, default=EventImportance.MODERATE)
    
    # Description
    description = Column(Text, nullable=True)
    
    # Date/time information
    date_string = Column(String(255), nullable=True)  # Human-readable date
    date_precision = Column(SQLEnum(DatePrecision), nullable=False, default=DatePrecision.APPROXIMATE)
    date_sort_value = Column(Integer, nullable=True)  # Numeric value for sorting
    
    # Duration
    is_instantaneous = Column(Integer, default=1)  # 1 = instant, 0 = has duration
    end_date_string = Column(String(255), nullable=True)
    end_date_sort_value = Column(Integer, nullable=True)
    
    # Related entities (stored as JSON)
    # Example: {"notable_figures": [1, 2, 3], "locations": [5], "organizations": []}
    related_entities = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String(50), default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    universe = relationship("Universe", backref="events")
    
    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', date='{self.date_string}', type={self.event_type.value})>"
    
    def get_duration_display(self) -> str:
        """Get human-readable duration.
        
        Returns:
            Duration string
        """
        if self.is_instantaneous:
            return "Instantaneous"
        if self.end_date_string:
            return f"{self.date_string} - {self.end_date_string}"
        return f"From {self.date_string} (ongoing)"
    
    def add_related_entity(self, entity_type: str, entity_id: int):
        """Add a related entity to the event.
        
        Args:
            entity_type: Type of entity (e.g., "notable_figures")
            entity_id: Entity ID
        """
        if not self.related_entities:
            self.related_entities = {}
        
        if entity_type not in self.related_entities:
            self.related_entities[entity_type] = []
        
        if entity_id not in self.related_entities[entity_type]:
            self.related_entities[entity_type].append(entity_id)
    
    def remove_related_entity(self, entity_type: str, entity_id: int):
        """Remove a related entity from the event.
        
        Args:
            entity_type: Type of entity
            entity_id: Entity ID
        """
        if not self.related_entities or entity_type not in self.related_entities:
            return
        
        if entity_id in self.related_entities[entity_type]:
            self.related_entities[entity_type].remove(entity_id)
    
    def get_related_entities(self, entity_type: str) -> list:
        """Get list of related entity IDs of a specific type.
        
        Args:
            entity_type: Type of entity
            
        Returns:
            List of entity IDs
        """
        if not self.related_entities:
            return []
        return self.related_entities.get(entity_type, [])


class Timeline(Base):
    """Represents a timeline within a universe."""
    
    __tablename__ = "timelines"
    
    # IDs
    id = Column(Integer, primary_key=True)
    universe_id = Column(Integer, ForeignKey("universes.id"), nullable=False)
    name = Column(String(255), nullable=False)
    
    # Properties
    description = Column(Text, nullable=True)
    is_main_timeline = Column(Integer, default=0)  # 1 = main timeline, 0 = alternate/specific
    
    # Event IDs (stored as JSON list)
    event_ids = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String(50), default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    universe = relationship("Universe", backref="timelines")
    
    def __repr__(self):
        timeline_type = "Main" if self.is_main_timeline else "Alternate"
        return f"<Timeline(id={self.id}, name='{self.name}', type={timeline_type})>"
    
    def add_event(self, event_id: int):
        """Add an event to this timeline.
        
        Args:
            event_id: Event ID
        """
        if not self.event_ids:
            self.event_ids = []
        
        # Create a new list to trigger SQLAlchemy update
        current_ids = list(self.event_ids)
        if event_id not in current_ids:
            current_ids.append(event_id)
            self.event_ids = current_ids
    
    def remove_event(self, event_id: int):
        """Remove an event from this timeline.
        
        Args:
            event_id: Event ID
        """
        if self.event_ids and event_id in self.event_ids:
            # Create a new list to trigger SQLAlchemy update
            current_ids = list(self.event_ids)
            current_ids.remove(event_id)
            self.event_ids = current_ids
    
    def get_event_ids(self) -> list:
        """Get list of event IDs in this timeline.
        
        Returns:
            List of event IDs
        """
        return self.event_ids or []

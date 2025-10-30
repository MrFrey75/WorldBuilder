"""Event and Timeline services for business logic operations."""
from typing import List, Optional, Dict
from worldbuilder.models.event import Event, Timeline
from worldbuilder.enums import EventType, EventImportance, DatePrecision
from worldbuilder.database.event_repository import EventRepository, TimelineRepository


class EventService:
    """Service layer for Event business logic."""
    
    def __init__(self, repository: EventRepository):
        self.repository = repository
    
    def create_event(self, name: str, universe_id: int, event_type: EventType = None,
                    importance: EventImportance = None, description: str = None,
                    date_string: str = None, date_precision: DatePrecision = None,
                    date_sort_value: int = None, is_instantaneous: bool = True,
                    end_date_string: str = None, end_date_sort_value: int = None,
                    related_entities: Dict = None) -> Event:
        """Create a new event.
        
        Args:
            name: Event name (required)
            universe_id: Universe ID (required)
            event_type: Type of event
            importance: Importance level
            description: Event description
            date_string: Human-readable date
            date_precision: Date precision level
            date_sort_value: Numeric value for sorting
            is_instantaneous: Whether event is instantaneous
            end_date_string: End date for durations
            end_date_sort_value: End date sort value
            related_entities: Dict of related entity IDs by type
            
        Returns:
            Created Event entity
            
        Raises:
            ValueError: If validation fails
        """
        if not name or not name.strip():
            raise ValueError("Event name cannot be empty")
        
        if not universe_id:
            raise ValueError("Universe ID is required")
        
        event = Event(
            name=name.strip(),
            universe_id=universe_id,
            event_type=event_type or EventType.OTHER,
            importance=importance or EventImportance.MODERATE,
            description=description,
            date_string=date_string,
            date_precision=date_precision or DatePrecision.APPROXIMATE,
            date_sort_value=date_sort_value,
            is_instantaneous=1 if is_instantaneous else 0,
            end_date_string=end_date_string,
            end_date_sort_value=end_date_sort_value,
            related_entities=related_entities or {}
        )
        
        self.repository.add(event)
        self.repository.commit()
        
        return event
    
    def get_event(self, event_id: int) -> Optional[Event]:
        """Get event by ID."""
        return self.repository.get_by_id(event_id)
    
    def get_all_events(self, universe_id: int) -> List[Event]:
        """Get all events in a universe."""
        return self.repository.get_by_universe(universe_id)
    
    def get_by_type(self, universe_id: int, event_type: EventType) -> List[Event]:
        """Get events by type."""
        return self.repository.get_by_type(universe_id, event_type)
    
    def get_by_importance(self, universe_id: int, importance: EventImportance) -> List[Event]:
        """Get events by importance."""
        return self.repository.get_by_importance(universe_id, importance)
    
    def get_sorted_by_date(self, universe_id: int) -> List[Event]:
        """Get events sorted chronologically."""
        return self.repository.get_sorted_by_date(universe_id)
    
    def update_event(self, event_id: int, name: str = None, event_type: EventType = None,
                    importance: EventImportance = None, description: str = None,
                    date_string: str = None, date_precision: DatePrecision = None,
                    date_sort_value: int = None, is_instantaneous: bool = None,
                    end_date_string: str = None, end_date_sort_value: int = None) -> Optional[Event]:
        """Update an event.
        
        Args:
            event_id: Event ID
            name: New name (optional)
            event_type: New type (optional)
            importance: New importance (optional)
            description: New description (optional)
            date_string: New date string (optional)
            date_precision: New precision (optional)
            date_sort_value: New sort value (optional)
            is_instantaneous: New duration type (optional)
            end_date_string: New end date (optional)
            end_date_sort_value: New end sort value (optional)
            
        Returns:
            Updated Event or None if not found
        """
        event = self.repository.get_by_id(event_id)
        if not event:
            return None
        
        if name is not None and name.strip():
            event.name = name.strip()
        
        if event_type is not None:
            event.event_type = event_type
        
        if importance is not None:
            event.importance = importance
        
        if description is not None:
            event.description = description
        
        if date_string is not None:
            event.date_string = date_string
        
        if date_precision is not None:
            event.date_precision = date_precision
        
        if date_sort_value is not None:
            event.date_sort_value = date_sort_value
        
        if is_instantaneous is not None:
            event.is_instantaneous = 1 if is_instantaneous else 0
        
        if end_date_string is not None:
            event.end_date_string = end_date_string
        
        if end_date_sort_value is not None:
            event.end_date_sort_value = end_date_sort_value
        
        self.repository.update(event)
        self.repository.commit()
        
        return event
    
    def delete_event(self, event_id: int) -> bool:
        """Delete an event.
        
        Args:
            event_id: Event ID
            
        Returns:
            True if deleted, False if not found
        """
        result = self.repository.delete(event_id)
        if result:
            self.repository.commit()
        return result
    
    def search_events(self, universe_id: int, search_term: str) -> List[Event]:
        """Search events by name.
        
        Args:
            universe_id: Universe ID
            search_term: Search term
            
        Returns:
            List of matching events
        """
        return self.repository.search_by_name(universe_id, search_term)


class TimelineService:
    """Service layer for Timeline business logic."""
    
    def __init__(self, repository: TimelineRepository):
        self.repository = repository
    
    def create_timeline(self, name: str, universe_id: int, description: str = None,
                       is_main_timeline: bool = False) -> Timeline:
        """Create a new timeline.
        
        Args:
            name: Timeline name (required)
            universe_id: Universe ID (required)
            description: Timeline description
            is_main_timeline: Whether this is the main timeline
            
        Returns:
            Created Timeline entity
            
        Raises:
            ValueError: If validation fails
        """
        if not name or not name.strip():
            raise ValueError("Timeline name cannot be empty")
        
        if not universe_id:
            raise ValueError("Universe ID is required")
        
        # If setting as main, unset any existing main timeline
        if is_main_timeline:
            existing_main = self.repository.get_main_timeline(universe_id)
            if existing_main:
                existing_main.is_main_timeline = 0
                self.repository.update(existing_main)
        
        timeline = Timeline(
            name=name.strip(),
            universe_id=universe_id,
            description=description,
            is_main_timeline=1 if is_main_timeline else 0,
            event_ids=[]
        )
        
        self.repository.add(timeline)
        self.repository.commit()
        
        return timeline
    
    def get_timeline(self, timeline_id: int) -> Optional[Timeline]:
        """Get timeline by ID."""
        return self.repository.get_by_id(timeline_id)
    
    def get_all_timelines(self, universe_id: int) -> List[Timeline]:
        """Get all timelines in a universe."""
        return self.repository.get_by_universe(universe_id)
    
    def get_main_timeline(self, universe_id: int) -> Optional[Timeline]:
        """Get main timeline for a universe."""
        return self.repository.get_main_timeline(universe_id)
    
    def update_timeline(self, timeline_id: int, name: str = None, description: str = None,
                       is_main_timeline: bool = None) -> Optional[Timeline]:
        """Update a timeline.
        
        Args:
            timeline_id: Timeline ID
            name: New name (optional)
            description: New description (optional)
            is_main_timeline: New main status (optional)
            
        Returns:
            Updated Timeline or None if not found
        """
        timeline = self.repository.get_by_id(timeline_id)
        if not timeline:
            return None
        
        if name is not None and name.strip():
            timeline.name = name.strip()
        
        if description is not None:
            timeline.description = description
        
        if is_main_timeline is not None:
            # If setting as main, unset any existing main timeline
            if is_main_timeline:
                existing_main = self.repository.get_main_timeline(timeline.universe_id)
                if existing_main and existing_main.id != timeline_id:
                    existing_main.is_main_timeline = 0
                    self.repository.update(existing_main)
            
            timeline.is_main_timeline = 1 if is_main_timeline else 0
        
        self.repository.update(timeline)
        self.repository.commit()
        
        return timeline
    
    def delete_timeline(self, timeline_id: int) -> bool:
        """Delete a timeline.
        
        Args:
            timeline_id: Timeline ID
            
        Returns:
            True if deleted, False if not found
        """
        result = self.repository.delete(timeline_id)
        if result:
            self.repository.commit()
        return result
    
    def add_event_to_timeline(self, timeline_id: int, event_id: int) -> bool:
        """Add an event to a timeline.
        
        Args:
            timeline_id: Timeline ID
            event_id: Event ID
            
        Returns:
            True if successful
        """
        timeline = self.repository.get_by_id(timeline_id)
        if not timeline:
            return False
        
        timeline.add_event(event_id)
        self.repository.update(timeline)
        self.repository.commit()
        
        return True
    
    def remove_event_from_timeline(self, timeline_id: int, event_id: int) -> bool:
        """Remove an event from a timeline.
        
        Args:
            timeline_id: Timeline ID
            event_id: Event ID
            
        Returns:
            True if successful
        """
        timeline = self.repository.get_by_id(timeline_id)
        if not timeline:
            return False
        
        timeline.remove_event(event_id)
        self.repository.update(timeline)
        self.repository.commit()
        
        return True
    
    def search_timelines(self, universe_id: int, search_term: str) -> List[Timeline]:
        """Search timelines by name.
        
        Args:
            universe_id: Universe ID
            search_term: Search term
            
        Returns:
            List of matching timelines
        """
        return self.repository.search_by_name(universe_id, search_term)

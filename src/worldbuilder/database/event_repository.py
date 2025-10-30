"""Event and Timeline repositories for data access operations."""
from typing import List, Optional
from sqlalchemy import and_
from worldbuilder.database.repository import BaseRepository
from worldbuilder.models.event import Event, Timeline, EventType, EventImportance


class EventRepository(BaseRepository[Event]):
    """Repository for Event entity operations."""
    
    def __init__(self, session):
        super().__init__(session, Event)
    
    def get_by_universe(self, universe_id: int) -> List[Event]:
        """Get all events in a universe.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            List of events
        """
        return self.session.query(Event).filter_by(universe_id=universe_id).all()
    
    def get_by_type(self, universe_id: int, event_type: EventType) -> List[Event]:
        """Get events by type.
        
        Args:
            universe_id: Universe ID
            event_type: Event type
            
        Returns:
            List of events
        """
        return self.session.query(Event).filter(
            and_(
                Event.universe_id == universe_id,
                Event.event_type == event_type
            )
        ).all()
    
    def get_by_importance(self, universe_id: int, importance: EventImportance) -> List[Event]:
        """Get events by importance level.
        
        Args:
            universe_id: Universe ID
            importance: Importance level
            
        Returns:
            List of events
        """
        return self.session.query(Event).filter(
            and_(
                Event.universe_id == universe_id,
                Event.importance == importance
            )
        ).all()
    
    def get_sorted_by_date(self, universe_id: int) -> List[Event]:
        """Get events sorted by date.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            List of events sorted by date_sort_value
        """
        return self.session.query(Event).filter_by(universe_id=universe_id).order_by(Event.date_sort_value).all()
    
    def search_by_name(self, universe_id: int, search_term: str) -> List[Event]:
        """Search events by name.
        
        Args:
            universe_id: Universe ID
            search_term: Search term
            
        Returns:
            List of matching events
        """
        return self.session.query(Event).filter(
            and_(
                Event.universe_id == universe_id,
                Event.name.ilike(f"%{search_term}%")
            )
        ).all()


class TimelineRepository(BaseRepository[Timeline]):
    """Repository for Timeline entity operations."""
    
    def __init__(self, session):
        super().__init__(session, Timeline)
    
    def get_by_universe(self, universe_id: int) -> List[Timeline]:
        """Get all timelines in a universe.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            List of timelines
        """
        return self.session.query(Timeline).filter_by(universe_id=universe_id).all()
    
    def get_main_timeline(self, universe_id: int) -> Optional[Timeline]:
        """Get the main timeline for a universe.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            Main timeline or None
        """
        return self.session.query(Timeline).filter(
            and_(
                Timeline.universe_id == universe_id,
                Timeline.is_main_timeline == 1
            )
        ).first()
    
    def search_by_name(self, universe_id: int, search_term: str) -> List[Timeline]:
        """Search timelines by name.
        
        Args:
            universe_id: Universe ID
            search_term: Search term
            
        Returns:
            List of matching timelines
        """
        return self.session.query(Timeline).filter(
            and_(
                Timeline.universe_id == universe_id,
                Timeline.name.ilike(f"%{search_term}%")
            )
        ).all()

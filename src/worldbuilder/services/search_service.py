"""Search service for global entity searches."""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from worldbuilder.models import (Universe, Location, Species, NotableFigure, 
                                 Relationship, Event, Timeline)


class SearchResult:
    """Represents a single search result."""
    
    def __init__(self, entity_type: str, entity_id: int, entity: Any, 
                 matched_field: str, match_snippet: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.entity = entity
        self.matched_field = matched_field
        self.match_snippet = match_snippet
    
    def __repr__(self):
        return f"<SearchResult({self.entity_type}:{self.entity_id}, field='{self.matched_field}')>"


class SearchService:
    """Service for searching across all entity types."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def global_search(self, query: str, universe_id: int = None, 
                     entity_types: List[str] = None) -> List[SearchResult]:
        """Perform a global search across all entities.
        
        Args:
            query: Search query string
            universe_id: Optional universe ID to limit search
            entity_types: Optional list of entity types to search
            
        Returns:
            List of SearchResult objects
        """
        if not query or not query.strip():
            return []
        
        query = query.strip().lower()
        results = []
        
        # Default to all entity types if none specified
        if not entity_types:
            entity_types = ['universe', 'location', 'species', 'notable_figure', 
                          'relationship', 'event', 'timeline']
        
        # Search each entity type
        if 'universe' in entity_types and not universe_id:
            results.extend(self._search_universes(query))
        
        if 'location' in entity_types:
            results.extend(self._search_locations(query, universe_id))
        
        if 'species' in entity_types:
            results.extend(self._search_species(query, universe_id))
        
        if 'notable_figure' in entity_types:
            results.extend(self._search_figures(query, universe_id))
        
        if 'relationship' in entity_types:
            results.extend(self._search_relationships(query, universe_id))
        
        if 'event' in entity_types:
            results.extend(self._search_events(query, universe_id))
        
        if 'timeline' in entity_types:
            results.extend(self._search_timelines(query, universe_id))
        
        return results
    
    def _search_universes(self, query: str) -> List[SearchResult]:
        """Search Universe entities."""
        results = []
        universes = self.session.query(Universe).all()
        
        for universe in universes:
            # Search name
            if query in universe.name.lower():
                results.append(SearchResult(
                    'universe', universe.id, universe,
                    'name', universe.name
                ))
            # Search description
            elif universe.description and query in universe.description.lower():
                snippet = self._get_snippet(universe.description, query)
                results.append(SearchResult(
                    'universe', universe.id, universe,
                    'description', snippet
                ))
        
        return results
    
    def _search_locations(self, query: str, universe_id: int = None) -> List[SearchResult]:
        """Search Location entities."""
        results = []
        q = self.session.query(Location)
        if universe_id:
            q = q.filter_by(universe_id=universe_id)
        
        locations = q.all()
        
        for location in locations:
            if query in location.name.lower():
                results.append(SearchResult(
                    'location', location.id, location,
                    'name', location.name
                ))
            elif location.description and query in location.description.lower():
                snippet = self._get_snippet(location.description, query)
                results.append(SearchResult(
                    'location', location.id, location,
                    'description', snippet
                ))
        
        return results
    
    def _search_species(self, query: str, universe_id: int = None) -> List[SearchResult]:
        """Search Species entities."""
        results = []
        q = self.session.query(Species)
        if universe_id:
            q = q.filter_by(universe_id=universe_id)
        
        species_list = q.all()
        
        for species in species_list:
            if query in species.name.lower():
                results.append(SearchResult(
                    'species', species.id, species,
                    'name', species.name
                ))
            elif species.description and query in species.description.lower():
                snippet = self._get_snippet(species.description, query)
                results.append(SearchResult(
                    'species', species.id, species,
                    'description', snippet
                ))
        
        return results
    
    def _search_figures(self, query: str, universe_id: int = None) -> List[SearchResult]:
        """Search NotableFigure entities."""
        results = []
        q = self.session.query(NotableFigure)
        if universe_id:
            q = q.filter_by(universe_id=universe_id)
        
        figures = q.all()
        
        for figure in figures:
            if query in figure.name.lower():
                results.append(SearchResult(
                    'notable_figure', figure.id, figure,
                    'name', figure.name
                ))
            elif figure.title and query in figure.title.lower():
                results.append(SearchResult(
                    'notable_figure', figure.id, figure,
                    'title', figure.title
                ))
            elif figure.backstory and query in figure.backstory.lower():
                snippet = self._get_snippet(figure.backstory, query)
                results.append(SearchResult(
                    'notable_figure', figure.id, figure,
                    'backstory', snippet
                ))
        
        return results
    
    def _search_relationships(self, query: str, universe_id: int = None) -> List[SearchResult]:
        """Search Relationship entities."""
        results = []
        q = self.session.query(Relationship)
        if universe_id:
            q = q.filter_by(universe_id=universe_id)
        
        relationships = q.all()
        
        for rel in relationships:
            # Search custom type name
            if rel.custom_type_name and query in rel.custom_type_name.lower():
                results.append(SearchResult(
                    'relationship', rel.id, rel,
                    'custom_type_name', rel.custom_type_name
                ))
            # Search description
            elif rel.description and query in rel.description.lower():
                snippet = self._get_snippet(rel.description, query)
                results.append(SearchResult(
                    'relationship', rel.id, rel,
                    'description', snippet
                ))
        
        return results
    
    def _search_events(self, query: str, universe_id: int = None) -> List[SearchResult]:
        """Search Event entities."""
        results = []
        q = self.session.query(Event)
        if universe_id:
            q = q.filter_by(universe_id=universe_id)
        
        events = q.all()
        
        for event in events:
            if query in event.name.lower():
                results.append(SearchResult(
                    'event', event.id, event,
                    'name', event.name
                ))
            elif event.description and query in event.description.lower():
                snippet = self._get_snippet(event.description, query)
                results.append(SearchResult(
                    'event', event.id, event,
                    'description', snippet
                ))
            elif event.date_string and query in event.date_string.lower():
                results.append(SearchResult(
                    'event', event.id, event,
                    'date_string', event.date_string
                ))
        
        return results
    
    def _search_timelines(self, query: str, universe_id: int = None) -> List[SearchResult]:
        """Search Timeline entities."""
        results = []
        q = self.session.query(Timeline)
        if universe_id:
            q = q.filter_by(universe_id=universe_id)
        
        timelines = q.all()
        
        for timeline in timelines:
            if query in timeline.name.lower():
                results.append(SearchResult(
                    'timeline', timeline.id, timeline,
                    'name', timeline.name
                ))
            elif timeline.description and query in timeline.description.lower():
                snippet = self._get_snippet(timeline.description, query)
                results.append(SearchResult(
                    'timeline', timeline.id, timeline,
                    'description', snippet
                ))
        
        return results
    
    def _get_snippet(self, text: str, query: str, context_chars: int = 50) -> str:
        """Extract a snippet of text around the search query.
        
        Args:
            text: Full text to extract from
            query: Search query
            context_chars: Number of characters before/after to include
            
        Returns:
            Text snippet with query highlighted
        """
        text_lower = text.lower()
        query_lower = query.lower()
        
        pos = text_lower.find(query_lower)
        if pos == -1:
            return text[:100] + "..." if len(text) > 100 else text
        
        start = max(0, pos - context_chars)
        end = min(len(text), pos + len(query) + context_chars)
        
        snippet = text[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
        
        return snippet

"""Notable Figure service for business logic operations."""
from typing import List, Optional, Dict, Any
from worldbuilder.models.notable_figure import NotableFigure
from worldbuilder.database.notable_figure_repository import NotableFigureRepository


class NotableFigureService:
    """Service layer for NotableFigure business logic."""
    
    def __init__(self, repository: NotableFigureRepository):
        self.repository = repository
    
    def create_figure(self, name: str, universe_id: int,
                     species_id: int = None, location_id: int = None,
                     title: str = None, age: str = None, occupation: str = None,
                     description: str = None, attributes: Dict[str, Any] = None,
                     backstory: str = None, personality: str = None,
                     goals: str = None) -> NotableFigure:
        """Create a new notable figure.
        
        Args:
            name: Figure name (required)
            universe_id: Universe ID (required)
            species_id: Species ID (optional, defaults to Human if available)
            location_id: Location ID (optional)
            title: Title (e.g., "King", "Lord")
            age: Age (can be range or "unknown")
            occupation: Occupation
            description: Description
            attributes: Additional attributes dict
            backstory: Backstory text
            personality: Personality description
            goals: Goals and motivations
            
        Returns:
            Created NotableFigure entity
            
        Raises:
            ValueError: If validation fails
        """
        if not name or not name.strip():
            raise ValueError("Figure name cannot be empty")
        
        if not universe_id:
            raise ValueError("Universe ID is required")
        
        figure = NotableFigure(
            name=name.strip(),
            universe_id=universe_id,
            species_id=species_id,
            location_id=location_id,
            title=title,
            age=age,
            occupation=occupation,
            description=description,
            attributes=attributes or {},
            backstory=backstory,
            personality=personality,
            goals=goals
        )
        
        self.repository.add(figure)
        self.repository.commit()
        
        return figure
    
    def get_figure(self, figure_id: int) -> Optional[NotableFigure]:
        """Get figure by ID."""
        return self.repository.get_by_id(figure_id)
    
    def get_all_figures(self, universe_id: int) -> List[NotableFigure]:
        """Get all figures in a universe."""
        return self.repository.get_by_universe(universe_id)
    
    def get_by_species(self, species_id: int) -> List[NotableFigure]:
        """Get figures of a specific species."""
        return self.repository.get_by_species(species_id)
    
    def get_by_location(self, location_id: int) -> List[NotableFigure]:
        """Get figures at a specific location."""
        return self.repository.get_by_location(location_id)
    
    def get_by_occupation(self, universe_id: int, occupation: str) -> List[NotableFigure]:
        """Get figures by occupation."""
        return self.repository.get_by_occupation(universe_id, occupation)
    
    def update_figure(self, figure_id: int, name: str = None,
                     species_id: int = None, location_id: int = None,
                     title: str = None, age: str = None, occupation: str = None,
                     description: str = None, attributes: Dict[str, Any] = None,
                     backstory: str = None, personality: str = None,
                     goals: str = None) -> Optional[NotableFigure]:
        """Update a notable figure.
        
        Args:
            figure_id: Figure ID
            name: New name (optional)
            species_id: New species ID (optional, use -1 to remove)
            location_id: New location ID (optional, use -1 to remove)
            title: New title (optional)
            age: New age (optional)
            occupation: New occupation (optional)
            description: New description (optional)
            attributes: New attributes dict (optional)
            backstory: New backstory (optional)
            personality: New personality (optional)
            goals: New goals (optional)
            
        Returns:
            Updated NotableFigure or None if not found
        """
        figure = self.repository.get_by_id(figure_id)
        if not figure:
            return None
        
        if name is not None and name.strip():
            figure.name = name.strip()
        
        if species_id is not None:
            figure.species_id = None if species_id == -1 else species_id
        
        if location_id is not None:
            figure.location_id = None if location_id == -1 else location_id
        
        if title is not None:
            figure.title = title if title.strip() else None
        
        if age is not None:
            figure.age = age if age.strip() else None
        
        if occupation is not None:
            figure.occupation = occupation if occupation.strip() else None
        
        if description is not None:
            figure.description = description
        
        if attributes is not None:
            figure.attributes = attributes
        
        if backstory is not None:
            figure.backstory = backstory
        
        if personality is not None:
            figure.personality = personality
        
        if goals is not None:
            figure.goals = goals
        
        self.repository.update(figure)
        self.repository.commit()
        
        return figure
    
    def delete_figure(self, figure_id: int) -> bool:
        """Delete a notable figure.
        
        Args:
            figure_id: Figure ID
            
        Returns:
            True if deleted, False if not found
        """
        result = self.repository.delete(figure_id)
        if result:
            self.repository.commit()
        return result
    
    def search_figures(self, universe_id: int, search_term: str) -> List[NotableFigure]:
        """Search figures by name.
        
        Args:
            universe_id: Universe ID
            search_term: Search term
            
        Returns:
            List of matching figures
        """
        return self.repository.search_by_name(universe_id, search_term)

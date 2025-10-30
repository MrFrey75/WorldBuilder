"""Universe service for business logic operations."""
from typing import List, Optional
from worldbuilder.models.universe import Universe
from worldbuilder.database.universe_repository import UniverseRepository


class UniverseService:
    """Service layer for Universe business logic."""
    
    def __init__(self, repository: UniverseRepository):
        self.repository = repository
    
    def create_universe(self, name: str, description: str = None, 
                       author: str = None, genre: str = None) -> Universe:
        """Create a new universe.
        
        Args:
            name: Universe name (required)
            description: Universe description
            author: Author name
            genre: Genre (e.g., Fantasy, Sci-Fi, Horror)
            
        Returns:
            Created Universe entity
            
        Raises:
            ValueError: If name is empty or universe with name already exists
        """
        if not name or not name.strip():
            raise ValueError("Universe name cannot be empty")
        
        # Check if universe with same name exists
        existing = self.repository.get_by_name(name)
        if existing:
            raise ValueError(f"Universe with name '{name}' already exists")
        
        universe = Universe(
            name=name.strip(),
            description=description,
            author=author,
            genre=genre,
            is_active=True
        )
        
        self.repository.add(universe)
        self.repository.commit()
        
        return universe
    
    def get_universe(self, universe_id: int) -> Optional[Universe]:
        """Get universe by ID."""
        return self.repository.get_by_id(universe_id)
    
    def get_all_universes(self) -> List[Universe]:
        """Get all universes."""
        return self.repository.get_all()
    
    def get_active_universes(self) -> List[Universe]:
        """Get only active universes."""
        return self.repository.get_active_universes()
    
    def update_universe(self, universe_id: int, name: str = None, 
                       description: str = None, author: str = None, 
                       genre: str = None) -> Optional[Universe]:
        """Update an existing universe.
        
        Args:
            universe_id: ID of universe to update
            name: New name (optional)
            description: New description (optional)
            author: New author (optional)
            genre: New genre (optional)
            
        Returns:
            Updated Universe entity or None if not found
        """
        universe = self.repository.get_by_id(universe_id)
        if not universe:
            return None
        
        if name is not None and name.strip():
            # Check if new name conflicts with another universe
            existing = self.repository.get_by_name(name)
            if existing and existing.id != universe_id:
                raise ValueError(f"Universe with name '{name}' already exists")
            universe.name = name.strip()
        
        if description is not None:
            universe.description = description
        
        if author is not None:
            universe.author = author
        
        if genre is not None:
            universe.genre = genre
        
        self.repository.update(universe)
        self.repository.commit()
        
        return universe
    
    def delete_universe(self, universe_id: int) -> bool:
        """Delete a universe.
        
        Args:
            universe_id: ID of universe to delete
            
        Returns:
            True if deleted, False if not found
        """
        result = self.repository.delete(universe_id)
        if result:
            self.repository.commit()
        return result
    
    def set_active_universe(self, universe_id: int) -> bool:
        """Set a universe as active (and deactivate others).
        
        Args:
            universe_id: ID of universe to activate
            
        Returns:
            True if successful, False if not found
        """
        universe = self.repository.get_by_id(universe_id)
        if not universe:
            return False
        
        # Deactivate all universes
        all_universes = self.repository.get_all()
        for u in all_universes:
            u.is_active = False
        
        # Activate the selected one
        universe.is_active = True
        
        self.repository.commit()
        return True
    
    def search_universes(self, search_term: str) -> List[Universe]:
        """Search universes by name.
        
        Args:
            search_term: Search term for universe name
            
        Returns:
            List of matching universes
        """
        return self.repository.search_by_name(search_term)

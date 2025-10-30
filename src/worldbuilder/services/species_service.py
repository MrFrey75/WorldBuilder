"""Species service for business logic operations."""
from typing import List, Optional, Dict, Any
from worldbuilder.models.species import Species
from worldbuilder.enums import SpeciesType
from worldbuilder.database.species_repository import SpeciesRepository


class SpeciesService:
    """Service layer for Species business logic."""
    
    def __init__(self, repository: SpeciesRepository):
        self.repository = repository
    
    def create_species(self, name: str, universe_id: int,
                      species_type: SpeciesType = SpeciesType.SENTIENT,
                      description: str = None, is_playable: bool = True,
                      physical_traits: Dict[str, Any] = None,
                      abilities: str = None, culture: str = None) -> Species:
        """Create a new species.
        
        Args:
            name: Species name (required)
            universe_id: Universe ID (required)
            species_type: Type of species
            description: Species description
            is_playable: Whether can be used for characters
            physical_traits: Dictionary of physical characteristics
            abilities: Special abilities description
            culture: Cultural description
            
        Returns:
            Created Species entity
            
        Raises:
            ValueError: If validation fails
        """
        if not name or not name.strip():
            raise ValueError("Species name cannot be empty")
        
        if not universe_id:
            raise ValueError("Universe ID is required")
        
        # Check for duplicate name in universe
        existing = self.repository.get_by_name(universe_id, name.strip())
        if existing:
            raise ValueError(f"Species with name '{name}' already exists in this universe")
        
        species = Species(
            name=name.strip(),
            universe_id=universe_id,
            species_type=species_type,
            description=description,
            is_playable=is_playable,
            physical_traits=physical_traits or {},
            abilities=abilities,
            culture=culture
        )
        
        self.repository.add(species)
        self.repository.commit()
        
        return species
    
    def create_default_human(self, universe_id: int) -> Species:
        """Create a default human species for a universe.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            Created human species
        """
        # Check if human already exists
        existing = self.repository.get_by_name(universe_id, "Human")
        if existing:
            return existing
        
        human = Species.create_default_human(universe_id)
        self.repository.add(human)
        self.repository.commit()
        
        return human
    
    def get_species(self, species_id: int) -> Optional[Species]:
        """Get species by ID."""
        return self.repository.get_by_id(species_id)
    
    def get_all_species(self, universe_id: int) -> List[Species]:
        """Get all species in a universe."""
        return self.repository.get_by_universe(universe_id)
    
    def get_by_type(self, universe_id: int, species_type: SpeciesType) -> List[Species]:
        """Get species by type."""
        return self.repository.get_by_type(universe_id, species_type)
    
    def get_playable_species(self, universe_id: int) -> List[Species]:
        """Get playable species."""
        return self.repository.get_playable_species(universe_id)
    
    def update_species(self, species_id: int, name: str = None,
                      description: str = None, species_type: SpeciesType = None,
                      is_playable: bool = None, physical_traits: Dict[str, Any] = None,
                      abilities: str = None, culture: str = None) -> Optional[Species]:
        """Update a species.
        
        Args:
            species_id: Species ID
            name: New name (optional)
            description: New description (optional)
            species_type: New type (optional)
            is_playable: New playable status (optional)
            physical_traits: New traits dict (optional)
            abilities: New abilities (optional)
            culture: New culture (optional)
            
        Returns:
            Updated Species or None if not found
            
        Raises:
            ValueError: If validation fails
        """
        species = self.repository.get_by_id(species_id)
        if not species:
            return None
        
        if name is not None and name.strip():
            # Check for duplicate name
            existing = self.repository.get_by_name(species.universe_id, name.strip())
            if existing and existing.id != species_id:
                raise ValueError(f"Species with name '{name}' already exists in this universe")
            species.name = name.strip()
        
        if description is not None:
            species.description = description
        
        if species_type is not None:
            species.species_type = species_type
        
        if is_playable is not None:
            species.is_playable = is_playable
        
        if physical_traits is not None:
            species.physical_traits = physical_traits
        
        if abilities is not None:
            species.abilities = abilities
        
        if culture is not None:
            species.culture = culture
        
        self.repository.update(species)
        self.repository.commit()
        
        return species
    
    def delete_species(self, species_id: int) -> bool:
        """Delete a species.
        
        Args:
            species_id: Species ID
            
        Returns:
            True if deleted, False if not found
        """
        result = self.repository.delete(species_id)
        if result:
            self.repository.commit()
        return result
    
    def search_species(self, universe_id: int, search_term: str) -> List[Species]:
        """Search species by name.
        
        Args:
            universe_id: Universe ID
            search_term: Search term
            
        Returns:
            List of matching species
        """
        return self.repository.search_by_name(universe_id, search_term)

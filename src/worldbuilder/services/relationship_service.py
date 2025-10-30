"""Relationship service for business logic operations."""
from typing import List, Optional, Tuple
from worldbuilder.models.relationship import Relationship, RelationshipType, RelationshipStrength
from worldbuilder.database.relationship_repository import RelationshipRepository


class RelationshipService:
    """Service layer for Relationship business logic."""
    
    def __init__(self, repository: RelationshipRepository):
        self.repository = repository
    
    def create_relationship(self, universe_id: int, source_type: str, source_id: int,
                          target_type: str, target_id: int, relationship_type: RelationshipType,
                          custom_type_name: str = None, strength: RelationshipStrength = None,
                          description: str = None, start_date: str = None, end_date: str = None,
                          is_active: bool = True, create_inverse: bool = True) -> Relationship:
        """Create a new relationship.
        
        Args:
            universe_id: Universe ID
            source_type: Source entity type (e.g., "notable_figure")
            source_id: Source entity ID
            target_type: Target entity type
            target_id: Target entity ID
            relationship_type: Type of relationship
            custom_type_name: Custom name if type is CUSTOM
            strength: Relationship strength
            description: Additional description
            start_date: When relationship started
            end_date: When relationship ended (if applicable)
            is_active: Whether relationship is currently active
            create_inverse: Whether to auto-create inverse relationship
            
        Returns:
            Created Relationship entity
            
        Raises:
            ValueError: If validation fails
        """
        if not universe_id:
            raise ValueError("Universe ID is required")
        
        if not source_type or not source_id:
            raise ValueError("Source entity type and ID are required")
        
        if not target_type or not target_id:
            raise ValueError("Target entity type and ID are required")
        
        if source_type == target_type and source_id == target_id:
            raise ValueError("Cannot create relationship from entity to itself")
        
        if relationship_type == RelationshipType.CUSTOM and not custom_type_name:
            raise ValueError("Custom type name is required for CUSTOM relationship type")
        
        # Check for existing relationship
        existing = self.repository.find_relationship(
            source_type, source_id, target_type, target_id, relationship_type
        )
        if existing:
            raise ValueError("Relationship already exists between these entities")
        
        relationship = Relationship(
            universe_id=universe_id,
            source_entity_type=source_type,
            source_entity_id=source_id,
            target_entity_type=target_type,
            target_entity_id=target_id,
            relationship_type=relationship_type,
            custom_type_name=custom_type_name,
            strength=strength or RelationshipStrength.MODERATE,
            description=description,
            start_date=start_date,
            end_date=end_date,
            is_active=1 if is_active else 0
        )
        
        self.repository.add(relationship)
        self.repository.commit()
        
        # Create inverse relationship if applicable
        if create_inverse and not relationship.is_bidirectional():
            inverse_type = relationship.get_inverse_type()
            # Check if inverse already exists
            inverse_exists = self.repository.find_relationship(
                target_type, target_id, source_type, source_id, inverse_type
            )
            if not inverse_exists:
                inverse_rel = Relationship(
                    universe_id=universe_id,
                    source_entity_type=target_type,
                    source_entity_id=target_id,
                    target_entity_type=source_type,
                    target_entity_id=source_id,
                    relationship_type=inverse_type,
                    custom_type_name=custom_type_name,
                    strength=strength or RelationshipStrength.MODERATE,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=1 if is_active else 0
                )
                self.repository.add(inverse_rel)
                self.repository.commit()
        
        return relationship
    
    def get_relationship(self, relationship_id: int) -> Optional[Relationship]:
        """Get relationship by ID."""
        return self.repository.get_by_id(relationship_id)
    
    def get_all_relationships(self, universe_id: int) -> List[Relationship]:
        """Get all relationships in a universe."""
        return self.repository.get_by_universe(universe_id)
    
    def get_relationships_for_entity(self, entity_type: str, entity_id: int) -> List[Relationship]:
        """Get all relationships involving an entity."""
        return self.repository.get_all_for_entity(entity_type, entity_id)
    
    def get_outgoing_relationships(self, entity_type: str, entity_id: int) -> List[Relationship]:
        """Get relationships where entity is the source."""
        return self.repository.get_by_source(entity_type, entity_id)
    
    def get_incoming_relationships(self, entity_type: str, entity_id: int) -> List[Relationship]:
        """Get relationships where entity is the target."""
        return self.repository.get_by_target(entity_type, entity_id)
    
    def get_by_type(self, universe_id: int, relationship_type: RelationshipType) -> List[Relationship]:
        """Get relationships by type."""
        return self.repository.get_by_type(universe_id, relationship_type)
    
    def get_active_relationships(self, universe_id: int) -> List[Relationship]:
        """Get active relationships."""
        return self.repository.get_active_relationships(universe_id)
    
    def update_relationship(self, relationship_id: int, relationship_type: RelationshipType = None,
                          custom_type_name: str = None, strength: RelationshipStrength = None,
                          description: str = None, start_date: str = None, end_date: str = None,
                          is_active: bool = None) -> Optional[Relationship]:
        """Update a relationship.
        
        Args:
            relationship_id: Relationship ID
            relationship_type: New type (optional)
            custom_type_name: New custom name (optional)
            strength: New strength (optional)
            description: New description (optional)
            start_date: New start date (optional)
            end_date: New end date (optional)
            is_active: New active status (optional)
            
        Returns:
            Updated Relationship or None if not found
        """
        relationship = self.repository.get_by_id(relationship_id)
        if not relationship:
            return None
        
        if relationship_type is not None:
            relationship.relationship_type = relationship_type
        
        if custom_type_name is not None:
            relationship.custom_type_name = custom_type_name
        
        if strength is not None:
            relationship.strength = strength
        
        if description is not None:
            relationship.description = description
        
        if start_date is not None:
            relationship.start_date = start_date
        
        if end_date is not None:
            relationship.end_date = end_date
        
        if is_active is not None:
            relationship.is_active = 1 if is_active else 0
        
        self.repository.update(relationship)
        self.repository.commit()
        
        return relationship
    
    def delete_relationship(self, relationship_id: int) -> bool:
        """Delete a relationship.
        
        Args:
            relationship_id: Relationship ID
            
        Returns:
            True if deleted, False if not found
        """
        result = self.repository.delete(relationship_id)
        if result:
            self.repository.commit()
        return result
    
    def delete_all_for_entity(self, entity_type: str, entity_id: int) -> int:
        """Delete all relationships for an entity.
        
        Args:
            entity_type: Entity type
            entity_id: Entity ID
            
        Returns:
            Number of relationships deleted
        """
        count = self.repository.delete_all_for_entity(entity_type, entity_id)
        self.repository.commit()
        return count
    
    def end_relationship(self, relationship_id: int, end_date: str = None) -> Optional[Relationship]:
        """Mark a relationship as ended.
        
        Args:
            relationship_id: Relationship ID
            end_date: Date relationship ended
            
        Returns:
            Updated relationship or None if not found
        """
        return self.update_relationship(relationship_id, end_date=end_date, is_active=False)

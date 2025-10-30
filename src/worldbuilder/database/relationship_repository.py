"""Relationship repository for data access operations."""
from typing import List, Optional, Tuple
from sqlalchemy import and_, or_
from worldbuilder.database.repository import BaseRepository
from worldbuilder.models.relationship import Relationship, RelationshipType, RelationshipStrength


class RelationshipRepository(BaseRepository[Relationship]):
    """Repository for Relationship entity operations."""
    
    def __init__(self, session):
        super().__init__(session, Relationship)
    
    def get_by_universe(self, universe_id: int) -> List[Relationship]:
        """Get all relationships in a universe.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            List of relationships
        """
        return self.session.query(Relationship).filter_by(universe_id=universe_id).all()
    
    def get_by_source(self, entity_type: str, entity_id: int) -> List[Relationship]:
        """Get relationships where entity is the source.
        
        Args:
            entity_type: Type of entity (e.g., "notable_figure")
            entity_id: Entity ID
            
        Returns:
            List of relationships
        """
        return self.session.query(Relationship).filter(
            and_(
                Relationship.source_entity_type == entity_type,
                Relationship.source_entity_id == entity_id
            )
        ).all()
    
    def get_by_target(self, entity_type: str, entity_id: int) -> List[Relationship]:
        """Get relationships where entity is the target.
        
        Args:
            entity_type: Type of entity
            entity_id: Entity ID
            
        Returns:
            List of relationships
        """
        return self.session.query(Relationship).filter(
            and_(
                Relationship.target_entity_type == entity_type,
                Relationship.target_entity_id == entity_id
            )
        ).all()
    
    def get_all_for_entity(self, entity_type: str, entity_id: int) -> List[Relationship]:
        """Get all relationships involving an entity (source or target).
        
        Args:
            entity_type: Type of entity
            entity_id: Entity ID
            
        Returns:
            List of all relationships involving the entity
        """
        return self.session.query(Relationship).filter(
            or_(
                and_(
                    Relationship.source_entity_type == entity_type,
                    Relationship.source_entity_id == entity_id
                ),
                and_(
                    Relationship.target_entity_type == entity_type,
                    Relationship.target_entity_id == entity_id
                )
            )
        ).all()
    
    def get_by_type(self, universe_id: int, relationship_type: RelationshipType) -> List[Relationship]:
        """Get relationships by type.
        
        Args:
            universe_id: Universe ID
            relationship_type: Type of relationship
            
        Returns:
            List of relationships of given type
        """
        return self.session.query(Relationship).filter(
            and_(
                Relationship.universe_id == universe_id,
                Relationship.relationship_type == relationship_type
            )
        ).all()
    
    def get_active_relationships(self, universe_id: int) -> List[Relationship]:
        """Get active (non-ended) relationships.
        
        Args:
            universe_id: Universe ID
            
        Returns:
            List of active relationships
        """
        return self.session.query(Relationship).filter(
            and_(
                Relationship.universe_id == universe_id,
                Relationship.is_active == 1
            )
        ).all()
    
    def find_relationship(self, source_type: str, source_id: int,
                         target_type: str, target_id: int,
                         relationship_type: RelationshipType = None) -> Optional[Relationship]:
        """Find a specific relationship between two entities.
        
        Args:
            source_type: Source entity type
            source_id: Source entity ID
            target_type: Target entity type
            target_id: Target entity ID
            relationship_type: Optional type filter
            
        Returns:
            Relationship if found, None otherwise
        """
        query = self.session.query(Relationship).filter(
            and_(
                Relationship.source_entity_type == source_type,
                Relationship.source_entity_id == source_id,
                Relationship.target_entity_type == target_type,
                Relationship.target_entity_id == target_id
            )
        )
        
        if relationship_type:
            query = query.filter(Relationship.relationship_type == relationship_type)
        
        return query.first()
    
    def delete_all_for_entity(self, entity_type: str, entity_id: int) -> int:
        """Delete all relationships involving an entity.
        
        Args:
            entity_type: Type of entity
            entity_id: Entity ID
            
        Returns:
            Number of relationships deleted
        """
        relationships = self.get_all_for_entity(entity_type, entity_id)
        count = len(relationships)
        
        for rel in relationships:
            self.session.delete(rel)
        
        return count

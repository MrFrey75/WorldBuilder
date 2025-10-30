"""Repository for Artifact entities."""
from typing import List, Optional
from sqlalchemy.orm import Session
from worldbuilder.models import Artifact
from worldbuilder.enums import ArtifactType


class ArtifactRepository:
    """Repository for managing Artifact entities."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, artifact: Artifact) -> Artifact:
        """Create a new artifact."""
        self.session.add(artifact)
        self.session.commit()
        self.session.refresh(artifact)
        return artifact
    
    def get_by_id(self, artifact_id: int) -> Optional[Artifact]:
        """Get an artifact by ID."""
        return self.session.query(Artifact).filter_by(id=artifact_id).first()
    
    def get_all(self, universe_id: int = None) -> List[Artifact]:
        """Get all artifacts, optionally filtered by universe."""
        query = self.session.query(Artifact)
        if universe_id:
            query = query.filter_by(universe_id=universe_id)
        return query.order_by(Artifact.name).all()
    
    def get_by_type(self, universe_id: int, artifact_type: ArtifactType) -> List[Artifact]:
        """Get artifacts by type."""
        return self.session.query(Artifact)\
            .filter_by(universe_id=universe_id, artifact_type=artifact_type)\
            .order_by(Artifact.name).all()
    
    def get_magical(self, universe_id: int) -> List[Artifact]:
        """Get all magical artifacts."""
        return self.session.query(Artifact)\
            .filter_by(universe_id=universe_id, is_magical=1)\
            .order_by(Artifact.name).all()
    
    def get_by_owner(self, owner_id: int) -> List[Artifact]:
        """Get artifacts owned by a specific figure."""
        return self.session.query(Artifact)\
            .filter_by(current_owner_id=owner_id)\
            .order_by(Artifact.name).all()
    
    def get_by_location(self, location_id: int) -> List[Artifact]:
        """Get artifacts at a specific location."""
        return self.session.query(Artifact)\
            .filter_by(current_location_id=location_id)\
            .order_by(Artifact.name).all()
    
    def get_by_creator(self, creator_id: int) -> List[Artifact]:
        """Get artifacts created by a specific figure."""
        return self.session.query(Artifact)\
            .filter_by(creator_id=creator_id)\
            .order_by(Artifact.name).all()
    
    def get_by_rarity(self, universe_id: int, rarity: str) -> List[Artifact]:
        """Get artifacts by rarity level."""
        return self.session.query(Artifact)\
            .filter_by(universe_id=universe_id, rarity=rarity)\
            .order_by(Artifact.name).all()
    
    def update(self, artifact: Artifact) -> Artifact:
        """Update an artifact."""
        self.session.commit()
        self.session.refresh(artifact)
        return artifact
    
    def delete(self, artifact_id: int) -> bool:
        """Delete an artifact."""
        artifact = self.get_by_id(artifact_id)
        if artifact:
            self.session.delete(artifact)
            self.session.commit()
            return True
        return False

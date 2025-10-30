"""Services for Organization, Artifact, and Lore entities."""
from typing import List, Optional
from worldbuilder.database import OrganizationRepository, ArtifactRepository, LoreRepository
from worldbuilder.models import (Organization, OrganizationType, Artifact, ArtifactType, 
                                 Lore, LoreType)


class OrganizationService:
    """Service for managing organizations."""
    
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository
    
    def create_organization(self, name: str, universe_id: int, org_type: OrganizationType,
                          description: str = None, **kwargs) -> Organization:
        """Create a new organization."""
        organization = Organization(
            name=name,
            universe_id=universe_id,
            organization_type=org_type,
            description=description,
            **kwargs
        )
        return self.repository.create(organization)
    
    def get_organization(self, organization_id: int) -> Optional[Organization]:
        """Get an organization by ID."""
        return self.repository.get_by_id(organization_id)
    
    def get_all_organizations(self, universe_id: int) -> List[Organization]:
        """Get all organizations in a universe."""
        return self.repository.get_all(universe_id)
    
    def get_by_type(self, universe_id: int, org_type: OrganizationType) -> List[Organization]:
        """Get organizations by type."""
        return self.repository.get_by_type(universe_id, org_type)
    
    def update_organization(self, organization: Organization) -> Organization:
        """Update an organization."""
        return self.repository.update(organization)
    
    def delete_organization(self, organization_id: int) -> bool:
        """Delete an organization."""
        return self.repository.delete(organization_id)


class ArtifactService:
    """Service for managing artifacts."""
    
    def __init__(self, repository: ArtifactRepository):
        self.repository = repository
    
    def create_artifact(self, name: str, universe_id: int, artifact_type: ArtifactType,
                       description: str = None, **kwargs) -> Artifact:
        """Create a new artifact."""
        artifact = Artifact(
            name=name,
            universe_id=universe_id,
            artifact_type=artifact_type,
            description=description,
            **kwargs
        )
        return self.repository.create(artifact)
    
    def get_artifact(self, artifact_id: int) -> Optional[Artifact]:
        """Get an artifact by ID."""
        return self.repository.get_by_id(artifact_id)
    
    def get_all_artifacts(self, universe_id: int) -> List[Artifact]:
        """Get all artifacts in a universe."""
        return self.repository.get_all(universe_id)
    
    def get_magical_artifacts(self, universe_id: int) -> List[Artifact]:
        """Get all magical artifacts."""
        return self.repository.get_magical(universe_id)
    
    def update_artifact(self, artifact: Artifact) -> Artifact:
        """Update an artifact."""
        return self.repository.update(artifact)
    
    def delete_artifact(self, artifact_id: int) -> bool:
        """Delete an artifact."""
        return self.repository.delete(artifact_id)


class LoreService:
    """Service for managing lore entries."""
    
    def __init__(self, repository: LoreRepository):
        self.repository = repository
    
    def create_lore(self, name: str, universe_id: int, lore_type: LoreType,
                   description: str = None, **kwargs) -> Lore:
        """Create a new lore entry."""
        lore = Lore(
            name=name,
            universe_id=universe_id,
            lore_type=lore_type,
            description=description,
            **kwargs
        )
        return self.repository.create(lore)
    
    def get_lore(self, lore_id: int) -> Optional[Lore]:
        """Get a lore entry by ID."""
        return self.repository.get_by_id(lore_id)
    
    def get_all_lore(self, universe_id: int) -> List[Lore]:
        """Get all lore entries in a universe."""
        return self.repository.get_all(universe_id)
    
    def get_by_type(self, universe_id: int, lore_type: LoreType) -> List[Lore]:
        """Get lore entries by type."""
        return self.repository.get_by_type(universe_id, lore_type)
    
    def update_lore(self, lore: Lore) -> Lore:
        """Update a lore entry."""
        return self.repository.update(lore)
    
    def delete_lore(self, lore_id: int) -> bool:
        """Delete a lore entry."""
        return self.repository.delete(lore_id)

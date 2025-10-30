"""Repository for Organization entities."""
from typing import List, Optional
from sqlalchemy.orm import Session
from worldbuilder.models import Organization
from worldbuilder.enums import OrganizationType


class OrganizationRepository:
    """Repository for managing Organization entities."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, organization: Organization) -> Organization:
        """Create a new organization."""
        self.session.add(organization)
        self.session.commit()
        self.session.refresh(organization)
        return organization
    
    def get_by_id(self, organization_id: int) -> Optional[Organization]:
        """Get an organization by ID."""
        return self.session.query(Organization).filter_by(id=organization_id).first()
    
    def get_all(self, universe_id: int = None) -> List[Organization]:
        """Get all organizations, optionally filtered by universe."""
        query = self.session.query(Organization)
        if universe_id:
            query = query.filter_by(universe_id=universe_id)
        return query.order_by(Organization.name).all()
    
    def get_by_type(self, universe_id: int, org_type: OrganizationType) -> List[Organization]:
        """Get organizations by type."""
        return self.session.query(Organization)\
            .filter_by(universe_id=universe_id, organization_type=org_type)\
            .order_by(Organization.name).all()
    
    def get_active(self, universe_id: int) -> List[Organization]:
        """Get all active organizations."""
        return self.session.query(Organization)\
            .filter_by(universe_id=universe_id, is_active=1)\
            .order_by(Organization.name).all()
    
    def get_by_location(self, location_id: int) -> List[Organization]:
        """Get organizations headquartered at a location."""
        return self.session.query(Organization)\
            .filter_by(headquarters_location_id=location_id)\
            .order_by(Organization.name).all()
    
    def get_by_leader(self, leader_id: int) -> List[Organization]:
        """Get organizations led by a specific figure."""
        return self.session.query(Organization)\
            .filter_by(current_leader_id=leader_id)\
            .order_by(Organization.name).all()
    
    def get_children(self, parent_id: int) -> List[Organization]:
        """Get child organizations of a parent."""
        return self.session.query(Organization)\
            .filter_by(parent_organization_id=parent_id)\
            .order_by(Organization.name).all()
    
    def update(self, organization: Organization) -> Organization:
        """Update an organization."""
        self.session.commit()
        self.session.refresh(organization)
        return organization
    
    def delete(self, organization_id: int) -> bool:
        """Delete an organization."""
        organization = self.get_by_id(organization_id)
        if organization:
            self.session.delete(organization)
            self.session.commit()
            return True
        return False

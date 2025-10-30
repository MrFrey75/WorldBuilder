"""Repository for Lore entities."""
from typing import List, Optional
from sqlalchemy.orm import Session
from worldbuilder.models import Lore, LoreType


class LoreRepository:
    """Repository for managing Lore entities."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, lore: Lore) -> Lore:
        """Create a new lore entry."""
        self.session.add(lore)
        self.session.commit()
        self.session.refresh(lore)
        return lore
    
    def get_by_id(self, lore_id: int) -> Optional[Lore]:
        """Get a lore entry by ID."""
        return self.session.query(Lore).filter_by(id=lore_id).first()
    
    def get_all(self, universe_id: int = None) -> List[Lore]:
        """Get all lore entries, optionally filtered by universe."""
        query = self.session.query(Lore)
        if universe_id:
            query = query.filter_by(universe_id=universe_id)
        return query.order_by(Lore.name).all()
    
    def get_by_type(self, universe_id: int, lore_type: LoreType) -> List[Lore]:
        """Get lore entries by type."""
        return self.session.query(Lore)\
            .filter_by(universe_id=universe_id, lore_type=lore_type)\
            .order_by(Lore.name).all()
    
    def get_by_location(self, location_id: int) -> List[Lore]:
        """Get lore entries originating from a location."""
        return self.session.query(Lore)\
            .filter_by(origin_location_id=location_id)\
            .order_by(Lore.name).all()
    
    def get_by_species(self, species_id: int) -> List[Lore]:
        """Get lore entries from a specific species."""
        return self.session.query(Lore)\
            .filter_by(origin_species_id=species_id)\
            .order_by(Lore.name).all()
    
    def get_by_organization(self, organization_id: int) -> List[Lore]:
        """Get lore entries from a specific organization."""
        return self.session.query(Lore)\
            .filter_by(origin_organization_id=organization_id)\
            .order_by(Lore.name).all()
    
    def get_by_author(self, author_id: int) -> List[Lore]:
        """Get lore entries written by a specific figure."""
        return self.session.query(Lore)\
            .filter_by(author_id=author_id)\
            .order_by(Lore.name).all()
    
    def get_true_lore(self, universe_id: int) -> List[Lore]:
        """Get lore entries that are actually true."""
        return self.session.query(Lore)\
            .filter_by(universe_id=universe_id, is_true=1)\
            .order_by(Lore.name).all()
    
    def get_false_lore(self, universe_id: int) -> List[Lore]:
        """Get lore entries that are false."""
        return self.session.query(Lore)\
            .filter_by(universe_id=universe_id, is_true=0)\
            .order_by(Lore.name).all()
    
    def update(self, lore: Lore) -> Lore:
        """Update a lore entry."""
        self.session.commit()
        self.session.refresh(lore)
        return lore
    
    def delete(self, lore_id: int) -> bool:
        """Delete a lore entry."""
        lore = self.get_by_id(lore_id)
        if lore:
            self.session.delete(lore)
            self.session.commit()
            return True
        return False

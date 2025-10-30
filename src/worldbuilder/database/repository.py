"""Base repository interface for data access."""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.orm import Session

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """Interface for repository pattern implementation."""
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities."""
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Add new entity."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update existing entity."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete entity by ID."""
        pass
    
    @abstractmethod
    def commit(self) -> None:
        """Commit changes to database."""
        pass


class BaseRepository(IRepository[T]):
    """Base implementation of repository pattern."""
    
    def __init__(self, session: Session, model_class: type):
        self.session = session
        self.model_class = model_class
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID."""
        return self.session.query(self.model_class).filter_by(id=entity_id).first()
    
    def get_all(self) -> List[T]:
        """Get all entities."""
        return self.session.query(self.model_class).all()
    
    def add(self, entity: T) -> T:
        """Add new entity."""
        self.session.add(entity)
        return entity
    
    def update(self, entity: T) -> T:
        """Update existing entity."""
        self.session.merge(entity)
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """Delete entity by ID."""
        entity = self.get_by_id(entity_id)
        if entity:
            self.session.delete(entity)
            return True
        return False
    
    def commit(self) -> None:
        """Commit changes to database."""
        self.session.commit()

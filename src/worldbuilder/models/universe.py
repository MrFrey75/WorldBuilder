"""Universe model representing a fictional world/universe."""
from sqlalchemy import Column, String, Boolean
from worldbuilder.models.base_entity import BaseEntity


class Universe(BaseEntity):
    """Represents a fictional universe/world."""
    
    __tablename__ = "universes"
    
    author = Column(String(255), nullable=True)
    genre = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Universe(id={self.id}, name='{self.name}', author='{self.author}')>"

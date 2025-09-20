"""
Publisher model for the Tailspin Toys Crowd Funding platform.
This module defines the Publisher SQLAlchemy model with validation and serialization methods.
"""
from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Publisher(BaseModel):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many games
    games = relationship("Game", back_populates="publisher")

    @validates('name')
    def validate_name(self, key, name):
        """
        Validate publisher name field.
        
        Args:
            key (str): Field name being validated
            name (str): Name value to validate
            
        Returns:
            str: Validated name string
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key, description):
        """
        Validate publisher description field.
        
        Args:
            key (str): Field name being validated
            description (str|None): Description value to validate
            
        Returns:
            str: Validated description string
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)

    def __repr__(self):
        """
        Return string representation of the Publisher instance.
        
        Returns:
            str: String representation showing publisher name
        """
        return f'<Publisher {self.name}>'

    def to_dict(self):
        """
        Convert Publisher instance to dictionary representation.
        
        Returns:
            dict: Dictionary containing publisher data with game count
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }
"""
Favorite Product Model
"""
from datetime import datetime

class Favorite:
    """
    Favorite Product Model
    Stores user's favorite/wishlist products
    """
    def __init__(self, favorite_id=None, user_id=None, product_id=None, created_at=None):
        self.favorite_id = favorite_id
        self.user_id = user_id
        self.product_id = product_id
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        """Convert favorite to dictionary"""
        return {
            'favorite_id': self.favorite_id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }

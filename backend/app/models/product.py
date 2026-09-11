from app import db
from datetime import datetime
import json

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # course, ebook, software, membership, etc
    price = db.Column(db.Float)
    link = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    features = db.Column(db.JSON)  # Array of features
    target_audience = db.Column(db.Text)  # Target market description
    key_benefits = db.Column(db.JSON)  # Array of benefits
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contents = db.relationship('Content', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'link': self.link,
            'image_url': self.image_url,
            'features': self.features,
            'target_audience': self.target_audience,
            'key_benefits': self.key_benefits,
            'created_at': self.created_at.isoformat(),
        }

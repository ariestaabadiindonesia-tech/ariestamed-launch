from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # youtube, instagram, facebook, tiktok
    platform_post_id = db.Column(db.String(255))  # External platform ID
    scheduled_at = db.Column(db.DateTime)
    published_at = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='draft')  # draft, scheduled, published, failed
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analytics = db.relationship('Analytics', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content_id': self.content_id,
            'platform': self.platform,
            'platform_post_id': self.platform_post_id,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
        }

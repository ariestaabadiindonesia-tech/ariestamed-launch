from app import db
from datetime import datetime

class Content(db.Model):
    __tablename__ = 'contents'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(50))  # caption, post, story, video_desc, etc
    platform = db.Column(db.String(50))  # youtube, instagram, facebook, tiktok, all
    hashtags = db.Column(db.JSON)  # Array of hashtags
    mentions = db.Column(db.JSON)  # Array of mentions
    image_url = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    call_to_action = db.Column(db.String(255))
    status = db.Column(db.String(50), default='draft')  # draft, approved, scheduled, published
    ai_generated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='content', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'title': self.title,
            'text': self.text,
            'content_type': self.content_type,
            'platform': self.platform,
            'hashtags': self.hashtags,
            'mentions': self.mentions,
            'image_url': self.image_url,
            'video_url': self.video_url,
            'call_to_action': self.call_to_action,
            'status': self.status,
            'ai_generated': self.ai_generated,
            'created_at': self.created_at.isoformat(),
        }

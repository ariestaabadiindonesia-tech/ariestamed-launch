from app import db
from datetime import datetime

class Analytics(db.Model):
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    platform = db.Column(db.String(50))  # youtube, instagram, facebook, tiktok
    
    # Metrics
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
    reach = db.Column(db.Integer, default=0)
    impressions = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0.0)
    click_through_rate = db.Column(db.Float, default=0.0)
    conversion_rate = db.Column(db.Float, default=0.0)
    
    # Timestamps
    measured_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'platform': self.platform,
            'views': self.views,
            'likes': self.likes,
            'comments': self.comments,
            'shares': self.shares,
            'clicks': self.clicks,
            'conversions': self.conversions,
            'engagement_rate': self.engagement_rate,
            'measured_at': self.measured_at.isoformat(),
        }

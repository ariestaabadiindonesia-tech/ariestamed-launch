from app import db
from datetime import datetime
from cryptography.fernet import Fernet
import os

class PlatformCredential(db.Model):
    __tablename__ = 'platform_credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # youtube, instagram, facebook, tiktok
    account_id = db.Column(db.String(255), nullable=False)
    account_name = db.Column(db.String(255))
    access_token = db.Column(db.Text)  # Encrypted
    refresh_token = db.Column(db.Text)  # Encrypted
    token_expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'platform': self.platform,
            'account_id': self.account_id,
            'account_name': self.account_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }

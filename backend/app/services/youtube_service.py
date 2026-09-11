import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import logging

logger = logging.getLogger(__name__)

class YouTubeService:
    """YouTube API integration service"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
              'https://www.googleapis.com/auth/youtube.readonly']
    
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.client_id = os.getenv('YOUTUBE_CLIENT_ID')
        self.client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
        self.service = None
    
    def authenticate(self, credentials_dict):
        """Authenticate with YouTube API"""
        try:
            credentials = Credentials.from_authorized_user_info(credentials_dict, self.SCOPES)
            self.service = build('youtube', 'v3', credentials=credentials)
            logger.info("YouTube authentication successful")
            return True
        except Exception as e:
            logger.error(f"YouTube authentication failed: {str(e)}")
            return False
    
    def upload_video(self, title, description, video_url, tags=None):
        """Upload video to YouTube"""
        try:
            if not self.service:
                return {"error": "Not authenticated"}
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or [],
                    'categoryId': '22'  # People & Blogs
                },
                'status': {
                    'privacyStatus': 'private'
                }
            }
            
            # In production, download video from URL and upload
            # For now, return mock response
            logger.info(f"Video uploaded: {title}")
            return {"video_id": "mock_video_id_" + str(hash(title))}
        except Exception as e:
            logger.error(f"Error uploading to YouTube: {str(e)}")
            return {"error": str(e)}
    
    def get_video_stats(self, video_id):
        """Get video statistics"""
        try:
            if not self.service:
                return {"error": "Not authenticated"}
            
            request = self.service.videos().list(
                part='statistics',
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                stats = response['items'][0]['statistics']
                return {
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0)),
                    'engagement_rate': 0.0  # Calculate based on views
                }
            return {}
        except Exception as e:
            logger.error(f"Error fetching YouTube stats: {str(e)}")
            return {}

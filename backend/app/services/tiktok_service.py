import os
import requests
import logging

logger = logging.getLogger(__name__)

class TikTokService:
    """TikTok API integration service"""
    
    API_BASE_URL = "https://open.tiktok.com/v1"
    
    def __init__(self):
        self.client_key = os.getenv('TIKTOK_CLIENT_KEY')
        self.client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
        self.access_token = os.getenv('TIKTOK_ACCESS_TOKEN')
    
    def upload_video(self, video_url, caption, cover_image=None):
        """Upload video to TikTok"""
        try:
            url = f"{self.API_BASE_URL}/video/upload/"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            data = {
                'video_url': video_url,
                'caption': caption
            }
            
            if cover_image:
                data['cover_image_url'] = cover_image
            
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                logger.error(f"TikTok upload failed: {response.text}")
                return {"error": response.text}
            
            video_id = response.json()['data']['video_id']
            logger.info(f"Uploaded to TikTok: {video_id}")
            return {"video_id": video_id}
        except Exception as e:
            logger.error(f"Error uploading to TikTok: {str(e)}")
            return {"error": str(e)}
    
    def get_video_stats(self, video_id):
        """Get video statistics"""
        try:
            url = f"{self.API_BASE_URL}/video/query/"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            params = {
                'video_id': video_id,
                'fields': 'view_count,like_count,comment_count,share_count'
            }
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                logger.error(f"TikTok stats request failed: {response.text}")
                return {}
            
            data = response.json()['data']
            return {
                'views': data.get('view_count', 0),
                'likes': data.get('like_count', 0),
                'comments': data.get('comment_count', 0),
                'shares': data.get('share_count', 0),
                'engagement_rate': 0.0
            }
        except Exception as e:
            logger.error(f"Error fetching TikTok stats: {str(e)}")
            return {}

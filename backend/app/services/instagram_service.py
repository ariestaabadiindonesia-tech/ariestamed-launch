import os
import requests
import logging

logger = logging.getLogger(__name__)

class InstagramService:
    """Instagram Graph API integration service"""
    
    API_BASE_URL = "https://graph.instagram.com/v18.0"
    
    def __init__(self):
        self.business_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        self.access_token = os.getenv('INSTAGRAM_USER_ACCESS_TOKEN')
    
    def post_image(self, image_url, caption, media_type='IMAGE'):
        """Post image to Instagram"""
        try:
            # First, create container
            container_url = f"{self.API_BASE_URL}/{self.business_account_id}/media"
            
            container_data = {
                'image_url': image_url,
                'caption': caption,
                'access_token': self.access_token
            }
            
            container_response = requests.post(container_url, data=container_data)
            if container_response.status_code != 200:
                logger.error(f"Container creation failed: {container_response.text}")
                return {"error": container_response.text}
            
            container_id = container_response.json()['id']
            
            # Publish container
            publish_url = f"{self.API_BASE_URL}/{self.business_account_id}/media_publish"
            publish_data = {
                'creation_id': container_id,
                'access_token': self.access_token
            }
            
            publish_response = requests.post(publish_url, data=publish_data)
            if publish_response.status_code != 200:
                logger.error(f"Publish failed: {publish_response.text}")
                return {"error": publish_response.text}
            
            post_id = publish_response.json()['id']
            logger.info(f"Posted to Instagram: {post_id}")
            return {"post_id": post_id}
        except Exception as e:
            logger.error(f"Error posting to Instagram: {str(e)}")
            return {"error": str(e)}
    
    def get_post_insights(self, post_id):
        """Get post insights"""
        try:
            insight_url = f"{self.API_BASE_URL}/{post_id}/insights"
            params = {
                'metric': 'engagement,impressions,reach',
                'access_token': self.access_token
            }
            
            response = requests.get(insight_url, params=params)
            if response.status_code != 200:
                logger.error(f"Insights request failed: {response.text}")
                return {}
            
            insights = response.json()['data']
            
            result = {
                'likes': 0,
                'comments': 0,
                'shares': 0,
                'reach': 0,
                'impressions': 0,
                'engagement_rate': 0.0
            }
            
            for metric in insights:
                if metric['name'] == 'engagement':
                    result['engagement'] = metric['values'][0]['value']
                elif metric['name'] == 'reach':
                    result['reach'] = metric['values'][0]['value']
                elif metric['name'] == 'impressions':
                    result['impressions'] = metric['values'][0]['value']
            
            return result
        except Exception as e:
            logger.error(f"Error fetching Instagram insights: {str(e)}")
            return {}

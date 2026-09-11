import os
import requests
import logging

logger = logging.getLogger(__name__)

class FacebookService:
    """Facebook Graph API integration service"""
    
    API_BASE_URL = "https://graph.facebook.com/v18.0"
    
    def __init__(self):
        self.page_access_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
        self.page_id = os.getenv('FACEBOOK_PAGE_ID', '')
    
    def post_feed(self, message, link=None, picture=None):
        """Post to Facebook feed"""
        try:
            url = f"{self.API_BASE_URL}/{self.page_id}/feed"
            
            data = {
                'message': message,
                'access_token': self.page_access_token
            }
            
            if link:
                data['link'] = link
            if picture:
                data['picture'] = picture
            
            response = requests.post(url, data=data)
            if response.status_code != 200:
                logger.error(f"Facebook post failed: {response.text}")
                return {"error": response.text}
            
            post_id = response.json()['id']
            logger.info(f"Posted to Facebook: {post_id}")
            return {"post_id": post_id}
        except Exception as e:
            logger.error(f"Error posting to Facebook: {str(e)}")
            return {"error": str(e)}
    
    def get_post_insights(self, post_id):
        """Get post insights"""
        try:
            url = f"{self.API_BASE_URL}/{post_id}/insights"
            params = {
                'metric': 'post_impressions,post_engaged_users,post_clicks',
                'access_token': self.page_access_token
            }
            
            response = requests.get(url, params=params)
            if response.status_code != 200:
                logger.error(f"Insights request failed: {response.text}")
                return {}
            
            insights = response.json()['data']
            
            result = {
                'likes': 0,
                'comments': 0,
                'shares': 0,
                'clicks': 0,
                'reach': 0,
                'engagement_rate': 0.0
            }
            
            for metric in insights:
                if metric['name'] == 'post_impressions':
                    result['reach'] = metric['values'][0]['value']
                elif metric['name'] == 'post_engaged_users':
                    result['engagement'] = metric['values'][0]['value']
                elif metric['name'] == 'post_clicks':
                    result['clicks'] = metric['values'][0]['value']
            
            return result
        except Exception as e:
            logger.error(f"Error fetching Facebook insights: {str(e)}")
            return {}

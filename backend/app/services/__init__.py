# Export all services
from .ai_service import AIContentGenerator
from .youtube_service import YouTubeService
from .instagram_service import InstagramService
from .facebook_service import FacebookService
from .tiktok_service import TikTokService

# Initialize services
ai_service = AIContentGenerator()
youtube_service = YouTubeService()
instagram_service = InstagramService()
facebook_service = FacebookService()
tiktok_service = TikTokService()

__all__ = [
    'ai_service',
    'youtube_service',
    'instagram_service',
    'facebook_service',
    'tiktok_service'
]

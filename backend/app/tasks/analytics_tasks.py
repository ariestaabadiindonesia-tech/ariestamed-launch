from celery import shared_task
from datetime import datetime, timedelta
from app import db
from app.models import Post, Analytics
from app.services import youtube_service, instagram_service, facebook_service, tiktok_service
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_youtube_analytics(post_id):
    """Fetch analytics from YouTube"""
    try:
        post = Post.query.get(post_id)
        if not post or not post.platform_post_id:
            return {"status": "error", "message": "Post not found or not published"}
        
        metrics = youtube_service.get_video_stats(post.platform_post_id)
        
        analytics = Analytics(
            post_id=post_id,
            platform='youtube',
            views=metrics.get('views', 0),
            likes=metrics.get('likes', 0),
            comments=metrics.get('comments', 0),
            engagement_rate=metrics.get('engagement_rate', 0.0)
        )
        db.session.add(analytics)
        db.session.commit()
        
        return {"status": "success", "metrics": metrics}
    except Exception as exc:
        logger.error(f"Error fetching YouTube analytics: {str(exc)}")
        return {"status": "error", "message": str(exc)}

@shared_task
def fetch_instagram_analytics(post_id):
    """Fetch analytics from Instagram"""
    try:
        post = Post.query.get(post_id)
        if not post or not post.platform_post_id:
            return {"status": "error", "message": "Post not found or not published"}
        
        metrics = instagram_service.get_post_insights(post.platform_post_id)
        
        analytics = Analytics(
            post_id=post_id,
            platform='instagram',
            likes=metrics.get('likes', 0),
            comments=metrics.get('comments', 0),
            shares=metrics.get('shares', 0),
            reach=metrics.get('reach', 0),
            impressions=metrics.get('impressions', 0),
            engagement_rate=metrics.get('engagement_rate', 0.0)
        )
        db.session.add(analytics)
        db.session.commit()
        
        return {"status": "success", "metrics": metrics}
    except Exception as exc:
        logger.error(f"Error fetching Instagram analytics: {str(exc)}")
        return {"status": "error", "message": str(exc)}

@shared_task
def fetch_facebook_analytics(post_id):
    """Fetch analytics from Facebook"""
    try:
        post = Post.query.get(post_id)
        if not post or not post.platform_post_id:
            return {"status": "error", "message": "Post not found or not published"}
        
        metrics = facebook_service.get_post_insights(post.platform_post_id)
        
        analytics = Analytics(
            post_id=post_id,
            platform='facebook',
            likes=metrics.get('likes', 0),
            comments=metrics.get('comments', 0),
            shares=metrics.get('shares', 0),
            clicks=metrics.get('clicks', 0),
            reach=metrics.get('reach', 0),
            engagement_rate=metrics.get('engagement_rate', 0.0)
        )
        db.session.add(analytics)
        db.session.commit()
        
        return {"status": "success", "metrics": metrics}
    except Exception as exc:
        logger.error(f"Error fetching Facebook analytics: {str(exc)}")
        return {"status": "error", "message": str(exc)}

@shared_task
def fetch_tiktok_analytics(post_id):
    """Fetch analytics from TikTok"""
    try:
        post = Post.query.get(post_id)
        if not post or not post.platform_post_id:
            return {"status": "error", "message": "Post not found or not published"}
        
        metrics = tiktok_service.get_video_stats(post.platform_post_id)
        
        analytics = Analytics(
            post_id=post_id,
            platform='tiktok',
            views=metrics.get('views', 0),
            likes=metrics.get('likes', 0),
            comments=metrics.get('comments', 0),
            shares=metrics.get('shares', 0),
            engagement_rate=metrics.get('engagement_rate', 0.0)
        )
        db.session.add(analytics)
        db.session.commit()
        
        return {"status": "success", "metrics": metrics}
    except Exception as exc:
        logger.error(f"Error fetching TikTok analytics: {str(exc)}")
        return {"status": "error", "message": str(exc)}

@shared_task
def refresh_all_analytics():
    """Refresh analytics for all published posts from last 30 days"""
    try:
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_posts = Post.query.filter(
            Post.status == 'published',
            Post.published_at >= thirty_days_ago
        ).all()
        
        for post in recent_posts:
            if post.platform == 'youtube':
                fetch_youtube_analytics.delay(post.id)
            elif post.platform == 'instagram':
                fetch_instagram_analytics.delay(post.id)
            elif post.platform == 'facebook':
                fetch_facebook_analytics.delay(post.id)
            elif post.platform == 'tiktok':
                fetch_tiktok_analytics.delay(post.id)
        
        logger.info(f"Refreshed analytics for {len(recent_posts)} posts")
        return {"status": "success", "posts_updated": len(recent_posts)}
    except Exception as exc:
        logger.error(f"Error refreshing analytics: {str(exc)}")
        return {"status": "error", "message": str(exc)}

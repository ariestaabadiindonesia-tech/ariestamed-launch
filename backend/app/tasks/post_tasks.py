from celery import shared_task
from datetime import datetime, timedelta
from app import db
from app.models import Post, Content
from app.services import youtube_service, instagram_service, facebook_service, tiktok_service
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def post_to_youtube(self, post_id):
    """Post content to YouTube"""
    try:
        post = Post.query.get(post_id)
        if not post:
            return {"status": "error", "message": "Post not found"}
        
        content = post.content
        result = youtube_service.upload_video(
            title=content.title,
            description=content.text,
            video_url=content.video_url,
            tags=content.hashtags or []
        )
        
        post.platform_post_id = result['video_id']
        post.status = 'published'
        post.published_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Posted to YouTube: {post_id}")
        return {"status": "success", "platform_post_id": result['video_id']}
    except Exception as exc:
        logger.error(f"Error posting to YouTube: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)

@shared_task(bind=True, max_retries=3)
def post_to_instagram(self, post_id):
    """Post content to Instagram"""
    try:
        post = Post.query.get(post_id)
        if not post:
            return {"status": "error", "message": "Post not found"}
        
        content = post.content
        caption = content.text
        if content.hashtags:
            caption += " " + " ".join(content.hashtags)
        
        result = instagram_service.post_image(
            image_url=content.image_url,
            caption=caption
        )
        
        post.platform_post_id = result['post_id']
        post.status = 'published'
        post.published_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Posted to Instagram: {post_id}")
        return {"status": "success", "platform_post_id": result['post_id']}
    except Exception as exc:
        logger.error(f"Error posting to Instagram: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)

@shared_task(bind=True, max_retries=3)
def post_to_facebook(self, post_id):
    """Post content to Facebook"""
    try:
        post = Post.query.get(post_id)
        if not post:
            return {"status": "error", "message": "Post not found"}
        
        content = post.content
        result = facebook_service.post_feed(
            message=content.text,
            link=content.product.link if content.product else None,
            picture=content.image_url
        )
        
        post.platform_post_id = result['post_id']
        post.status = 'published'
        post.published_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Posted to Facebook: {post_id}")
        return {"status": "success", "platform_post_id": result['post_id']}
    except Exception as exc:
        logger.error(f"Error posting to Facebook: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)

@shared_task(bind=True, max_retries=3)
def post_to_tiktok(self, post_id):
    """Post content to TikTok"""
    try:
        post = Post.query.get(post_id)
        if not post:
            return {"status": "error", "message": "Post not found"}
        
        content = post.content
        caption = content.text
        if content.hashtags:
            caption += " " + " ".join(content.hashtags[:3])  # TikTok limits hashtags
        
        result = tiktok_service.upload_video(
            video_url=content.video_url,
            caption=caption,
            cover_image=content.image_url
        )
        
        post.platform_post_id = result['video_id']
        post.status = 'published'
        post.published_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Posted to TikTok: {post_id}")
        return {"status": "success", "platform_post_id": result['video_id']}
    except Exception as exc:
        logger.error(f"Error posting to TikTok: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)

@shared_task
def process_scheduled_posts():
    """Check and publish scheduled posts"""
    try:
        now = datetime.utcnow()
        scheduled_posts = Post.query.filter(
            Post.status == 'scheduled',
            Post.scheduled_at <= now
        ).all()
        
        for post in scheduled_posts:
            if post.platform == 'youtube':
                post_to_youtube.delay(post.id)
            elif post.platform == 'instagram':
                post_to_instagram.delay(post.id)
            elif post.platform == 'facebook':
                post_to_facebook.delay(post.id)
            elif post.platform == 'tiktok':
                post_to_tiktok.delay(post.id)
        
        logger.info(f"Processed {len(scheduled_posts)} scheduled posts")
        return {"status": "success", "processed": len(scheduled_posts)}
    except Exception as exc:
        logger.error(f"Error processing scheduled posts: {str(exc)}")
        return {"status": "error", "message": str(exc)}

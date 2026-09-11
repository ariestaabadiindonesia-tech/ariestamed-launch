from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import posts_bp
from app.models import Post, Content, Product
from app import db, redis_client
from app.tasks.post_tasks import post_to_youtube, post_to_instagram, post_to_facebook, post_to_tiktok, process_scheduled_posts
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@posts_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    """Schedule a post"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        content_id = data.get('content_id')
        platform = data.get('platform')
        
        if not content_id or not platform:
            return jsonify({"error": "content_id and platform are required"}), 400
        
        content = Content.query.get(content_id)
        if not content or content.product.owner.id != user_id:
            return jsonify({"error": "Content not found"}), 404
        
        scheduled_at = data.get('scheduled_at')
        if scheduled_at:
            scheduled_at = datetime.fromisoformat(scheduled_at)
        else:
            scheduled_at = datetime.utcnow()
        
        post = Post(
            user_id=user_id,
            content_id=content_id,
            platform=platform,
            scheduled_at=scheduled_at,
            status='scheduled' if scheduled_at > datetime.utcnow() else 'draft'
        )
        
        db.session.add(post)
        db.session.commit()
        
        logger.info(f"Post scheduled: {post.id}")
        return jsonify({
            "message": "Post scheduled successfully",
            "post": post.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}")
        return jsonify({"error": str(e)}), 500

@posts_bp.route('', methods=['GET'])
@jwt_required()
def get_posts():
    """Get all posts for current user"""
    try:
        user_id = get_jwt_identity()
        
        query = Post.query.filter_by(user_id=user_id)
        
        if request.args.get('status'):
            query = query.filter_by(status=request.args.get('status'))
        
        if request.args.get('platform'):
            query = query.filter_by(platform=request.args.get('platform'))
        
        posts = query.all()
        
        return jsonify({
            "posts": [p.to_dict() for p in posts],
            "count": len(posts)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching posts: {str(e)}")
        return jsonify({"error": str(e)}), 500

@posts_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    """Get single post"""
    try:
        user_id = get_jwt_identity()
        post = Post.query.filter_by(id=post_id, user_id=user_id).first()
        
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        return jsonify(post.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching post: {str(e)}")
        return jsonify({"error": str(e)}), 500

@posts_bp.route('/<int:post_id>/publish', methods=['POST'])
@jwt_required()
def publish_post(post_id):
    """Publish post immediately"""
    try:
        user_id = get_jwt_identity()
        post = Post.query.filter_by(id=post_id, user_id=user_id).first()
        
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        # Queue publishing task based on platform
        if post.platform == 'youtube':
            task = post_to_youtube.delay(post.id)
        elif post.platform == 'instagram':
            task = post_to_instagram.delay(post.id)
        elif post.platform == 'facebook':
            task = post_to_facebook.delay(post.id)
        elif post.platform == 'tiktok':
            task = post_to_tiktok.delay(post.id)
        else:
            return jsonify({"error": "Unsupported platform"}), 400
        
        return jsonify({
            "message": "Post publishing started",
            "task_id": task.id
        }), 202
    except Exception as e:
        logger.error(f"Error publishing post: {str(e)}")
        return jsonify({"error": str(e)}), 500

@posts_bp.route('/<int:post_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_post(post_id):
    """Cancel scheduled post"""
    try:
        user_id = get_jwt_identity()
        post = Post.query.filter_by(id=post_id, user_id=user_id).first()
        
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        if post.status == 'published':
            return jsonify({"error": "Cannot cancel published post"}), 400
        
        post.status = 'cancelled'
        db.session.commit()
        
        logger.info(f"Post cancelled: {post_id}")
        return jsonify({
            "message": "Post cancelled successfully",
            "post": post.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error cancelling post: {str(e)}")
        return jsonify({"error": str(e)}), 500

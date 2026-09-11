from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import analytics_bp
from app.models import Post, Analytics, Product
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)

@analytics_bp.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post_analytics(post_id):
    """Get analytics for a specific post"""
    try:
        user_id = get_jwt_identity()
        post = Post.query.filter_by(id=post_id, user_id=user_id).first()
        
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        analytics = Analytics.query.filter_by(post_id=post_id).all()
        
        return jsonify({
            "post_id": post_id,
            "platform": post.platform,
            "analytics": [a.to_dict() for a in analytics]
        }), 200
    except Exception as e:
        logger.error(f"Error fetching post analytics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/platform/<platform>', methods=['GET'])
@jwt_required()
def get_platform_analytics(platform):
    """Get aggregated analytics for a platform"""
    try:
        user_id = get_jwt_identity()
        
        # Get user's posts on this platform
        posts = Post.query.filter_by(user_id=user_id, platform=platform).all()
        post_ids = [p.id for p in posts]
        
        if not post_ids:
            return jsonify({
                "platform": platform,
                "total_views": 0,
                "total_engagement": 0,
                "average_engagement_rate": 0
            }), 200
        
        # Get analytics for these posts
        analytics_data = Analytics.query.filter(Analytics.post_id.in_(post_ids)).all()
        
        total_views = sum(a.views for a in analytics_data)
        total_likes = sum(a.likes for a in analytics_data)
        total_comments = sum(a.comments for a in analytics_data)
        total_shares = sum(a.shares for a in analytics_data)
        
        total_engagement = total_likes + total_comments + total_shares
        avg_engagement_rate = sum(a.engagement_rate for a in analytics_data) / len(analytics_data) if analytics_data else 0
        
        return jsonify({
            "platform": platform,
            "total_views": total_views,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "total_engagement": total_engagement,
            "average_engagement_rate": round(avg_engagement_rate, 2),
            "post_count": len(post_ids)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching platform analytics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        user_id = get_jwt_identity()
        
        # Get user's posts
        posts = Post.query.filter_by(user_id=user_id).all()
        published_posts = [p for p in posts if p.status == 'published']
        scheduled_posts = [p for p in posts if p.status == 'scheduled']
        
        # Get analytics
        post_ids = [p.id for p in posts]
        analytics_data = Analytics.query.filter(Analytics.post_id.in_(post_ids)).all() if post_ids else []
        
        total_views = sum(a.views for a in analytics_data)
        total_engagement = sum(a.likes + a.comments + a.shares for a in analytics_data)
        
        # Get platform breakdown
        platform_stats = {}
        for platform in ['youtube', 'instagram', 'facebook', 'tiktok']:
            platform_posts = [p for p in posts if p.platform == platform]
            platform_post_ids = [p.id for p in platform_posts]
            platform_analytics = [a for a in analytics_data if a.post_id in platform_post_ids]
            
            platform_stats[platform] = {
                'posts': len(platform_posts),
                'views': sum(a.views for a in platform_analytics),
                'engagement': sum(a.likes + a.comments + a.shares for a in platform_analytics)
            }
        
        return jsonify({
            "total_posts": len(posts),
            "published_posts": len(published_posts),
            "scheduled_posts": len(scheduled_posts),
            "total_views": total_views,
            "total_engagement": total_engagement,
            "platforms": platform_stats
        }), 200
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/report', methods=['GET'])
@jwt_required()
def get_analytics_report():
    """Get detailed analytics report"""
    try:
        user_id = get_jwt_identity()
        
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        platform = request.args.get('platform')
        
        # Parse dates
        start_date = datetime.fromisoformat(start_date_str) if start_date_str else datetime.utcnow() - timedelta(days=30)
        end_date = datetime.fromisoformat(end_date_str) if end_date_str else datetime.utcnow()
        
        # Build query
        query = Post.query.filter_by(user_id=user_id)
        
        if platform:
            query = query.filter_by(platform=platform)
        
        query = query.filter(
            Post.published_at >= start_date,
            Post.published_at <= end_date
        )
        
        posts = query.all()
        post_ids = [p.id for p in posts]
        
        analytics_data = Analytics.query.filter(Analytics.post_id.in_(post_ids)).all() if post_ids else []
        
        return jsonify({
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "posts": len(posts),
            "metrics": {
                "total_views": sum(a.views for a in analytics_data),
                "total_likes": sum(a.likes for a in analytics_data),
                "total_comments": sum(a.comments for a in analytics_data),
                "total_shares": sum(a.shares for a in analytics_data),
                "average_engagement_rate": round(sum(a.engagement_rate for a in analytics_data) / len(analytics_data), 2) if analytics_data else 0
            },
            "top_posts": [
                {
                    "post_id": p.id,
                    "platform": p.platform,
                    "views": max([a.views for a in analytics_data if a.post_id == p.id], default=0),
                    "engagement": sum([a.likes + a.comments + a.shares for a in analytics_data if a.post_id == p.id])
                }
                for p in sorted(posts, key=lambda x: max([a.views for a in analytics_data if a.post_id == x.id], default=0), reverse=True)[:5]
            ]
        }), 200
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({"error": str(e)}), 500

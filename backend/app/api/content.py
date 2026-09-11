from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import content_bp
from app.models import Content, Product
from app import db
from app.tasks.content_tasks import generate_content_ai, generate_content_variations
import logging

logger = logging.getLogger(__name__)

@content_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_content():
    """Generate content using AI"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        product_id = data.get('product_id')
        if not product_id:
            return jsonify({"error": "product_id is required"}), 400
        
        # Verify product belongs to user
        product = Product.query.filter_by(id=product_id, user_id=user_id).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        # Queue AI content generation task
        task = generate_content_ai.delay(
            product_id=product_id,
            content_type=data.get('content_type', 'caption'),
            platform=data.get('platform', 'instagram'),
            tone=data.get('tone', 'professional'),
            length=data.get('length', 'medium')
        )
        
        return jsonify({
            "message": "Content generation started",
            "task_id": task.id
        }), 202
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        return jsonify({"error": str(e)}), 500

@content_bp.route('', methods=['POST'])
@jwt_required()
def create_content():
    """Create content manually"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('product_id') or not data.get('text'):
            return jsonify({"error": "product_id and text are required"}), 400
        
        # Verify product belongs to user
        product = Product.query.filter_by(id=data['product_id'], user_id=user_id).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        content = Content(
            product_id=data['product_id'],
            title=data.get('title', 'Untitled'),
            text=data['text'],
            content_type=data.get('content_type', 'caption'),
            platform=data.get('platform', 'instagram'),
            hashtags=data.get('hashtags', []),
            mentions=data.get('mentions', []),
            image_url=data.get('image_url'),
            video_url=data.get('video_url'),
            call_to_action=data.get('call_to_action'),
            status='draft'
        )
        
        db.session.add(content)
        db.session.commit()
        
        logger.info(f"Content created: {content.id}")
        return jsonify({
            "message": "Content created successfully",
            "content": content.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating content: {str(e)}")
        return jsonify({"error": str(e)}), 500

@content_bp.route('', methods=['GET'])
@jwt_required()
def get_content():
    """Get all content for user's products"""
    try:
        user_id = get_jwt_identity()
        
        # Get all products for user
        products = Product.query.filter_by(user_id=user_id).all()
        product_ids = [p.id for p in products]
        
        # Filter by product_id if provided
        query = Content.query.filter(Content.product_id.in_(product_ids))
        
        if request.args.get('product_id'):
            query = query.filter_by(product_id=int(request.args.get('product_id')))
        
        if request.args.get('status'):
            query = query.filter_by(status=request.args.get('status'))
        
        if request.args.get('platform'):
            query = query.filter_by(platform=request.args.get('platform'))
        
        contents = query.all()
        
        return jsonify({
            "contents": [c.to_dict() for c in contents],
            "count": len(contents)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching content: {str(e)}")
        return jsonify({"error": str(e)}), 500

@content_bp.route('/<int:content_id>', methods=['GET'])
@jwt_required()
def get_content_item(content_id):
    """Get single content item"""
    try:
        user_id = get_jwt_identity()
        content = Content.query.get(content_id)
        
        if not content or content.product.owner.id != user_id:
            return jsonify({"error": "Content not found"}), 404
        
        return jsonify(content.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching content: {str(e)}")
        return jsonify({"error": str(e)}), 500

@content_bp.route('/<int:content_id>', methods=['PUT'])
@jwt_required()
def update_content(content_id):
    """Update content"""
    try:
        user_id = get_jwt_identity()
        content = Content.query.get(content_id)
        
        if not content or content.product.owner.id != user_id:
            return jsonify({"error": "Content not found"}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            content.title = data['title']
        if 'text' in data:
            content.text = data['text']
        if 'hashtags' in data:
            content.hashtags = data['hashtags']
        if 'call_to_action' in data:
            content.call_to_action = data['call_to_action']
        if 'image_url' in data:
            content.image_url = data['image_url']
        if 'video_url' in data:
            content.video_url = data['video_url']
        
        db.session.commit()
        logger.info(f"Content updated: {content_id}")
        
        return jsonify({
            "message": "Content updated successfully",
            "content": content.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error updating content: {str(e)}")
        return jsonify({"error": str(e)}), 500

@content_bp.route('/<int:content_id>/approve', methods=['PUT'])
@jwt_required()
def approve_content(content_id):
    """Approve content for posting"""
    try:
        user_id = get_jwt_identity()
        content = Content.query.get(content_id)
        
        if not content or content.product.owner.id != user_id:
            return jsonify({"error": "Content not found"}), 404
        
        content.status = 'approved'
        db.session.commit()
        
        logger.info(f"Content approved: {content_id}")
        return jsonify({
            "message": "Content approved successfully",
            "content": content.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error approving content: {str(e)}")
        return jsonify({"error": str(e)}), 500

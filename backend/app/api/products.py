from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import products_bp
from app.models import Product, User
from app import db
import logging

logger = logging.getLogger(__name__)

@products_bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    """Create new product"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({"error": "Product name is required"}), 400
        
        product = Product(
            user_id=user_id,
            name=data['name'],
            description=data.get('description'),
            category=data.get('category'),
            price=data.get('price'),
            link=data.get('link'),
            image_url=data.get('image_url'),
            features=data.get('features', []),
            target_audience=data.get('target_audience'),
            key_benefits=data.get('key_benefits', [])
        )
        
        db.session.add(product)
        db.session.commit()
        
        logger.info(f"Product created: {product.id}")
        return jsonify({
            "message": "Product created successfully",
            "product": product.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        return jsonify({"error": str(e)}), 500

@products_bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    """Get all products for current user"""
    try:
        user_id = get_jwt_identity()
        products = Product.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            "products": [p.to_dict() for p in products],
            "count": len(products)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        return jsonify({"error": str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    """Get product by ID"""
    try:
        user_id = get_jwt_identity()
        product = Product.query.filter_by(id=product_id, user_id=user_id).first()
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        return jsonify(product.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        return jsonify({"error": str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Update product"""
    try:
        user_id = get_jwt_identity()
        product = Product.query.filter_by(id=product_id, user_id=user_id).first()
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'category' in data:
            product.category = data['category']
        if 'price' in data:
            product.price = data['price']
        if 'link' in data:
            product.link = data['link']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'features' in data:
            product.features = data['features']
        if 'key_benefits' in data:
            product.key_benefits = data['key_benefits']
        if 'target_audience' in data:
            product.target_audience = data['target_audience']
        
        db.session.commit()
        logger.info(f"Product updated: {product_id}")
        
        return jsonify({
            "message": "Product updated successfully",
            "product": product.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        return jsonify({"error": str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Delete product"""
    try:
        user_id = get_jwt_identity()
        product = Product.query.filter_by(id=product_id, user_id=user_id).first()
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        db.session.delete(product)
        db.session.commit()
        
        logger.info(f"Product deleted: {product_id}")
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting product: {str(e)}")
        return jsonify({"error": str(e)}), 500

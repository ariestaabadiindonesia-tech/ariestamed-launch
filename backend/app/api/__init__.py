from flask import Blueprint

# Auth API
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Products API
products_bp = Blueprint('products', __name__, url_prefix='/api/products')

# Content API
content_bp = Blueprint('content', __name__, url_prefix='/api/content')

# Posts API
posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

# Analytics API
analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

# Import routes
from app.api import auth, products, content, posts, analytics

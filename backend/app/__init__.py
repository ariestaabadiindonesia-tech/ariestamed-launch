from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
redis_client = Redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'))

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ariestamed.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.api import auth_bp, products_bp, content_bp, posts_bp, analytics_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(analytics_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

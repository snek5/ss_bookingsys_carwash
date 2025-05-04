from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # ✅ Import Flask-Migrate
import os

# Initialize database and login manager
db = SQLAlchemy()
login_manager = LoginManager()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'instance', 'car_wash.db')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/car_wash')

def create_app():
    app = Flask(__name__, static_folder="static")
    
    # Select configuration based on environment
    config_class = DevelopmentConfig if os.getenv('FLASK_ENV') == 'development' else ProductionConfig
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    
    # ✅ Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Register Blueprints
    from .views.main import main
    from .views.admin import admin
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')

    return app

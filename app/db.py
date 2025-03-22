from . import db, create_app
from .models import Booking, Admin

app = create_app()

with app.app_context():
    db.drop_all()  # Drop all existing tables
    db.create_all()  # Create all tables
    print("Database tables created!")
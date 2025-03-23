from . import db
from flask_login import UserMixin

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)  # 7 digits
    car_plate = db.Column(db.String(20), unique=True, nullable=False)
    car_type = db.Column(db.String(50), nullable=False)
    wash_type = db.Column(db.String(50), nullable=False)  # ["Exterior", "Interior + Exterior", "Polish"]
    date = db.Column(db.String(10), nullable=False) # YYYY-MM-DD
    time = db.Column(db.String(5), nullable=False)  # HH:MM format

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

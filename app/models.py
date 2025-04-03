from . import db
from flask_login import UserMixin

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    car_type = db.Column(db.String(50), nullable=False)
    wash_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    time = db.Column(db.String(5), nullable=False)   # HH:MM
    status = db.Column(db.String(20), default="Pending")  # New column

    def to_dict(self):
        return {
            "id": self.id,
            "title": f"{self.name} - {self.car_type} ({self.wash_type})",
            "start": f"{self.date}T{self.time}:00",
            "status": self.status
        }

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

from . import db
from flask_login import UserMixin
from datetime import datetime, timezone

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)  # Added field
    car_plate = db.Column(db.String(15), nullable=False)      # Added field
    car_type = db.Column(db.String(50), nullable=False)
    wash_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)                 # Changed to Date type
    time = db.Column(db.Time, nullable=False)                 # Changed to Time type
    status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # Added for tracking

    def to_dict(self):
        return {
            "id": self.id,
            "title": f"{self.name} - {self.car_type} ({self.wash_type})",
            "start": f"{self.date.strftime('%Y-%m-%d')}T{self.time.strftime('%H:%M')}",
            "status": self.status,
            "car_plate": self.car_plate,
            "contact_number": self.contact_number
        }

    def __repr__(self):
        return f'<Booking {self.id} - {self.name}>'
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

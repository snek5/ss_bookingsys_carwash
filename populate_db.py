from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

# Assuming your Flask app's data model is in a file named `models.py`
from app.models import Booking, db

# Initialize Faker
fake = Faker()

# Define the car types and wash types
car_types = ["Sedan", "Truck", "SUV", "Others"]
wash_types = ["Exterior", "Interior + Exterior", "Polish"]

# Define the date range for 2025
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

# Calculate the total number of days in 2025
delta = end_date - start_date
total_days = delta.days

# Create an SQLite engine and session
engine = create_engine('sqlite:///instance/car_wash.db')  # Replace with your actual database URL
Session = sessionmaker(bind=engine)
session = Session()

# Function to generate a random date within 2025
def random_date():
    random_day = random.randint(0, total_days)
    return start_date + timedelta(days=random_day)

# Function to generate a random time in HH:MM format
def random_time():
    return f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"

# Populate the Booking table with 1000 rows
for _ in range(1000):
    booking = Booking(
        name=fake.name(),
        contact_number=fake.numerify(text='#######'),  # 7 digits
        car_plate=fake.license_plate(),
        car_type=random.choice(car_types),
        wash_type=random.choice(wash_types),
        date=random_date().strftime('%Y-%m-%d'),
        time=random_time()
    )
    session.add(booking)

# Commit the session to save the data to the database
session.commit()

print("Database populated with 1000 bookings.")
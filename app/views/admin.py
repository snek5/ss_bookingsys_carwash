from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import Admin, Booking, db
from .. import login_manager

admin = Blueprint('admin', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Admin.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@admin.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('admin.register'))

        # Check if the username already exists
        existing_user = Admin.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect(url_for('admin.register'))

        # Create a new admin user
        new_user = Admin(
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')  # Fixed hashing method
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('admin.login'))

    return render_template('register.html')

@admin.route('/dashboard')
@login_required
def dashboard():
    bookings = Booking.query.all()
    return render_template('admin.html', bookings=bookings)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
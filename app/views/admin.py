from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import Admin, Booking, db
from .. import login_manager
from ..forms import LoginForm, RegisterForm  # ✅ Import WTForms

admin = Blueprint("admin", __name__)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # ✅ Create LoginForm instance

    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password.data, form.password.data):
            login_user(user)
            return redirect(url_for("admin.dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html", form=form)  # ✅ Pass form to template

@admin.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()  # ✅ Create RegisterForm instance

    if form.validate_on_submit():
        # Check if username exists
        existing_user = Admin.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for("admin.register"))

        # Hash password and create new admin
        new_user = Admin(
            username=form.username.data,
            password=generate_password_hash(form.password.data, method="pbkdf2:sha256"),
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("admin.login"))

    return render_template("register.html", form=form)  # ✅ Pass form to template

@admin.route("/dashboard")
@login_required
def dashboard():
    bookings = Booking.query.all()

    # Count different car types
    suv_count = Booking.query.filter_by(car_type="SUV").count()
    sedan_count = Booking.query.filter_by(car_type="Sedan").count()
    truck_count = Booking.query.filter_by(car_type="Truck").count()
    other_count = Booking.query.filter(Booking.car_type.notin_(["SUV", "Sedan", "Truck"])).count()

    return render_template(
        "admin.html",
        bookings=bookings,
        suv_count=suv_count,
        sedan_count=sedan_count,
        truck_count=truck_count,
        other_count=other_count,
    )

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))

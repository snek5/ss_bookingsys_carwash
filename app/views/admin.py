from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, login_user, logout_user
from flask_paginate import Pagination, get_page_args
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import Admin, Booking, db
from .. import login_manager
from ..forms import LoginForm, RegisterForm, BookingForm  # ✅ Import WTForms
from datetime import datetime, timedelta

admin = Blueprint("admin", __name__)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # ✅ Create LoginForm instance

    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
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
    search_query = request.args.get("search", "").strip()
    filter_car_type = request.args.get("filter_car_type", "")
    filter_wash_type = request.args.get("filter_wash_type", "")
    filter_today = request.args.get("filter_today", "")
    sort_by = request.args.get("sort_by", "date")
    sort_order = request.args.get("sort_order", "asc")

    today = datetime.today().strftime("%Y-%m-%d")
    query = Booking.query

    if search_query:
        query = query.filter(
            (Booking.name.ilike(f"%{search_query}%")) |
            (Booking.car_plate.ilike(f"%{search_query}%")) |
            (Booking.contact_number.ilike(f"%{search_query}%"))
        )

    if filter_car_type:
        query = query.filter(Booking.car_type == filter_car_type)
    if filter_wash_type:
        query = query.filter(Booking.wash_type == filter_wash_type)
    if filter_today:
        query = query.filter(Booking.date == today)

    if sort_by in ["name", "date", "time"]:
        query = query.order_by(
            getattr(Booking, sort_by).desc() if sort_order == "desc" else getattr(Booking, sort_by).asc()
        )

    # 🟢 Get pagination arguments
    page, per_page, _ = get_page_args(page_parameter="page", per_page_parameter="per_page")
    per_page = 10

    # 🟢 Paginate results
    bookings = query.paginate(page=page, per_page=per_page, error_out=False)

    # 🟢 Count different car types for stats
    suv_count = Booking.query.filter_by(car_type="SUV").count()
    sedan_count = Booking.query.filter_by(car_type="Sedan").count()
    truck_count = Booking.query.filter_by(car_type="Truck").count()
    other_count = Booking.query.filter(Booking.car_type.notin_(["SUV", "Sedan", "Truck"])).count()

    return render_template(
        "admin.html",
        bookings=bookings,  # ✅ Pass full pagination object
        pagination=bookings,  # ✅ Pagination works in template
        suv_count=suv_count,
        sedan_count=sedan_count,
        truck_count=truck_count,
        other_count=other_count,
        search_query=search_query,
        filter_car_type=filter_car_type,
        filter_wash_type=filter_wash_type,
        filter_today=filter_today,
        sort_by=sort_by,
        sort_order=sort_order
    )


@admin.route("/booking/add", methods=["GET", "POST"])
@login_required
def add_booking():
    form = BookingForm()
    if form.validate_on_submit():
        new_booking = Booking(
            name=form.name.data,
            contact_number=form.contact_number.data,
            car_plate=form.car_plate.data,
            car_type=form.car_type.data,
            wash_type=form.wash_type.data,
            date=form.date.data.strftime("%Y-%m-%d"),
            time=form.time.data.strftime("%H:%M"),
        )
        db.session.add(new_booking)
        db.session.commit()
        flash("Booking added successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("booking_form.html", form=form, action="Add")

@admin.route("/booking/edit/<int:booking_id>", methods=["GET", "POST"])
@login_required
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    # ✅ Convert stored strings to datetime.date and datetime.time objects (Only if needed)
    if isinstance(booking.date, str):  # Check if stored as string
        booking.date = datetime.strptime(booking.date, "%Y-%m-%d").date()  # Convert 'YYYY-MM-DD' string to date object
    if isinstance(booking.time, str):
        booking.time = datetime.strptime(booking.time, "%H:%M").time()  # Convert 'HH:MM' string to time object

    form = BookingForm(obj=booking)  # ✅ Prefill form with corrected data

    if form.validate_on_submit():
        booking.name = form.name.data
        booking.contact_number = form.contact_number.data
        booking.car_plate = form.car_plate.data
        booking.car_type = form.car_type.data
        booking.wash_type = form.wash_type.data
        booking.date = form.date.data.strftime("%Y-%m-%d")  # ✅ Convert date object back to string
        booking.time = form.time.data.strftime("%H:%M")  # ✅ Convert time object back to string

        db.session.commit()
        flash("Booking updated successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("booking_form.html", form=form, action="Edit")

@admin.route("/booking/delete/<int:booking_id>", methods=["POST"])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash("Booking deleted successfully!", "success")
    return redirect(url_for("admin.dashboard"))

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))

# Calendar function
# 🚀 Define wash durations
WASH_DURATIONS = {
    "Sedan": {"Exterior Only": 30, "Interior + Exterior": 45, "Exterior and Polish": 60},
    "SUV": {"Exterior Only": 45, "Interior + Exterior": 60, "Exterior and Polish": 90},
    "Truck": {"Exterior Only": 60, "Interior + Exterior": 90, "Exterior and Polish": 120},
}

@admin.route("/calendar")
@login_required
def calendar_view():
    return render_template("calendar.html")

@admin.route("/api/bookings")
@login_required
def get_bookings():
    bookings = Booking.query.all()
    events = []

    for booking in bookings:
        start_time = datetime.strptime(booking.time, "%H:%M")
        duration = WASH_DURATIONS.get(booking.car_type, {}).get(booking.wash_type, 30)  # Default: 30 mins
        end_time = start_time + timedelta(minutes=duration)

        events.append({
            "id": booking.id,
            "title": f"{booking.name} - {booking.car_type} - {booking.wash_type}",
            "start": f"{booking.date}T{start_time.strftime('%H:%M')}",
            "end": f"{booking.date}T{end_time.strftime('%H:%M')}",
            "color": "#007bff" if booking.wash_type == "Exterior Only" else "#28a745" if booking.wash_type == "Interior + Exterior" else "#ffc107",
        })

    return jsonify(events)
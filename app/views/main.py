from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
from ..models import Booking, db
from ..forms import BookingForm
from ..sms import confirmation_sms


main = Blueprint('main', __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    form = BookingForm()
    if form.validate_on_submit():
        new_booking = Booking(
            name=form.name.data,
            contact_number=form.contact_number.data,
            car_plate=form.car_plate.data,
            car_type=form.car_type.data,
            wash_type=form.wash_type.data,  # ✅ Save wash type
            date=form.date.data,
            time=form.time.data,
            status="Pending"
        )
        db.session.add(new_booking)
        db.session.commit()
        confirmation_sms(contact_number=str(new_booking.contact_number), 
                        car_plate=str(new_booking.car_plate),
                        car_type=str(new_booking.car_type),
                        wash_type=str(new_booking.wash_type),
                        date=str(new_booking.date),
                        time=str(new_booking.time)
                        )
        # print(contact_number, car_plate, car_type, wash_type, date, time)
        print("Booking details sent")
        flash("Booking successful!", "success")
        return redirect(url_for("main.index"))
    else:
        print(form.errors)
    return render_template("index.html", form=form)


@main.route("/api/check-availability")
def check_availability():
    date = request.args.get("date")
    time = request.args.get("time")
    car_type = request.args.get("car_type")
    wash_type = request.args.get("wash_type")

    # Calculate wash duration based on car type and wash type
    WASH_DURATIONS = {
        "Sedan": {"Exterior Only": 30, "Interior + Exterior": 45, "Polish": 60},
        "SUV": {"Exterior Only": 45, "Interior + Exterior": 60, "Polish": 90},
        "Truck": {"Exterior Only": 60, "Interior + Exterior": 90, "Polish": 120},
    }

    duration = WASH_DURATIONS.get(car_type, {}).get(wash_type, 30)

    # Convert time to datetime object
    start_time = datetime.strptime(time, "%H:%M").time()
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=duration)).time()

    # Check for overlapping bookings
    overlapping_bookings = Booking.query.filter(
        Booking.date == date,
        Booking.time.between(start_time, end_time)
    ).count()

    return jsonify({"available": overlapping_bookings == 0})

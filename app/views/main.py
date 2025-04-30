from flask import Blueprint, render_template, request, redirect, url_for, flash
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

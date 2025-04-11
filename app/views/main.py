from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Booking, db
from ..forms import BookingForm

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
        )
        db.session.add(new_booking)
        db.session.commit()
        flash("Booking successful!", "success")
        return redirect(url_for("main.index"))

    return render_template("index.html", form=form)

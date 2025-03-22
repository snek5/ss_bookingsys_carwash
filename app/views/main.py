from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Booking, db
from ..forms import BookingForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = BookingForm()
    if form.validate_on_submit():
        # Get form data
        name = form.name.data
        car_plate = form.car_plate.data
        car_type = form.car_type.data
        date = form.date.data.strftime('%Y-%m-%d')  # Convert to string
        time = form.time.data.strftime('%H:%M')     # Convert to string

        # Save to database
        new_booking = Booking(name=name, car_plate=car_plate, car_type=car_type, date=date, time=time)
        db.session.add(new_booking)
        db.session.commit()

        flash("Booking successful!", "success")
        return redirect(url_for('main.index'))

    return render_template('index.html', form=form)

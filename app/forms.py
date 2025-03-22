from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class BookingForm(FlaskForm):
    name = StringField("Customer Name", validators=[DataRequired(), Length(min=2, max=100)])
    car_plate = StringField("Car Plate Number", validators=[DataRequired(), Length(min=2, max=20)])
    car_type = SelectField("Car Type", choices=[("SUV", "SUV"), ("Sedan", "Sedan"), ("Truck", "Truck")])
    date = DateField("Date", validators=[DataRequired()])
    time = TimeField("Time", validators=[DataRequired()])
    submit = SubmitField("Book Now")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Register")

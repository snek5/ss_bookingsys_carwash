from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

class BookingForm(FlaskForm):
    name = StringField("Customer Name", validators=[DataRequired(), Length(min=2, max=100)])
    contact_number = StringField(
        "Contact Number",
        validators=[
            DataRequired(),
            Length(min=7, max=7, message="Contact number must be exactly 7 digits."),
            Regexp(r"^\d{7}$", message="Contact number must contain only digits (0-9)."),
        ],
    )
    car_plate = StringField("Car Plate Number", validators=[DataRequired(), Length(min=2, max=20)])
    car_type = SelectField("Car Type", choices=[("SUV", "SUV"), ("Sedan", "Sedan"), ("Truck", "Truck")])
    wash_type = SelectField(
        "Type of Wash",
        choices=[
            ("Exterior", "Exterior"),
            ("Interior + Exterior", "Interior + Exterior"),
            ("Polish", "Polish"),
        ],
    )
    status = SelectField("Status", 
                         choices=[("Pending", "Pending"), 
                                  ("Completed", "Completed"),
                                  ("Cancelled", "Cancelled")])
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

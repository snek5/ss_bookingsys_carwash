import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

def confirmation_sms(contact_number, car_plate, car_type, wash_type, date, time):
    message = client.messages.create(
    body=f"Thank you for booking your car {car_plate} with us. We look forward to serve you. For confirmation here is the booking details: \n Car Type: {car_type} \n Wash Type: {wash_type} \n Date: {date} \n Time: {time}",
    messaging_service_sid= os.getenv("TWILIO_MESSAGING_SERVICE_SID"),
    to=f"+673{contact_number}",
)
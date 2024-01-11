
from twilio.rest import Client
from flight_data import FlightData
from dotenv import load_dotenv
import os

load_dotenv()

AUTH_TOKEN=os.getenv("AUTH_TOKEN")

account_sid =os.getenv("account_sid")
TO_PHONE_NO =os.getenv("TO_PHONE_NO")
MY_TWILIO_NUMBER=os.getenv("MY_TWILIO_NUMBER")

auth_token = AUTH_TOKEN


class NotificationManager():
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self,flight : FlightData):
        self.client = Client(account_sid, auth_token)

        self.body_message=(f"Low Price Alert !! Only $ {flight.price} to fly from {flight.origin_city}-"
                               f"{flight.origin_airport}"
                               f" to {flight.destination_city}-{flight.destination_airport},from {flight.out_date}"
                               f"to {flight.return_date}.")
        if flight.stop_overs !=0:
            self.body_message+=f"Flight has 1 stop over , via {flight.via_city}"

        self.send_message(self.body_message)
        

    def send_message(self,msg):
        message = self.client.messages.create(
            body=msg,
            from_=MY_TWILIO_NUMBER,
            to=TO_PHONE_NO
        )
        print(message.status)
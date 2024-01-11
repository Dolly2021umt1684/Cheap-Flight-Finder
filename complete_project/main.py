from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from dotenv import load_dotenv
import os

load_dotenv()

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
datamanager=DataManager()
sheet_data=datamanager.data
print(sheet_data)

# fetching the IATA codes from flight_data
for element in sheet_data:
    update=FlightSearch().searching_iata(element['city'])
    element['iataCode']=update

# print(sheet_data)

# updating the fetched IATA code to google sheet through data_manager
for element in sheet_data:
    update=datamanager.update_row(element)

# now searching for data
for element in sheet_data:
    flight=FlightSearch().search_flights(element['iataCode'])
    if flight == None:
        continue
    elif flight.price<int(element['lowestPrice']):
        msg=NotificationManager(flight)


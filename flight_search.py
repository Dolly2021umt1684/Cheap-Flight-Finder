import requests
from datetime import datetime
from datetime import timedelta
from pprint import pprint
from flight_data import FlightData
from dotenv import load_dotenv
import os

load_dotenv()

API_key = os.getenv("API_key")

END_POINT='https://api.tequila.kiwi.com/locations/query'
SEARCH_END_POINT= 'https://api.tequila.kiwi.com/v2/search'
#
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.


    def searching_iata(self,city):
            header={
                        'apikey':API_key
                    }
            params={
                         'term':f'{city}'
                    }
            response=requests.get(url=END_POINT,headers=header,params=params)
            print(response.status_code)
            return response.json()['locations'][0]['code']

    def search_flights(self, dest_code):
        now = datetime.now()
        date_from = now.strftime("%d/%m/%Y")
        date_to = (now.date() + timedelta(days=180)).strftime("%d/%m/%Y")
        return_from = (now.date() + timedelta(days=7)).strftime("%d/%m/%Y")
        return_to = (now.date() + timedelta(days=28)).strftime("%d/%m/%Y")

        header = {
            'apikey': API_key
        }
        params = {
            'fly_from': 'LON',
            'fly_to': dest_code,
            'date_from': f'{date_from}',
            'date_to': f'{date_to}',
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'curr': 'GBP',
            'one_for_city': 1,
            'max_stopovers': 0

        }
        response = requests.get(url=SEARCH_END_POINT, headers=header, params=params)

        # print(pprint( response.json()))
        try:
            data = response.json()['data'][0]
        except IndexError:

            params['max_stopovers']=3
            response = requests.get(url=SEARCH_END_POINT, headers=header, params=params)
            try:
                data=response.json()['data'][0]
                flight_data = FlightData(
                    price=data['price'],
                    origin_city=data['cityFrom'],
                    origin_airport=data['route'][0]['flyFrom'],
                    destination_city=data['cityTo'],
                    destination_airport=data['route'][0]['flyTo'],
                    out_date=data['route'][0]['local_departure'].split('T')[0],
                    return_date=data['route'][1]['local_departure'].split('T')[0],
                    stop_overs=1,
                    via_city=data['route'][0]['cityTo']
                )
                print(f"{flight_data.destination_city} : $ {flight_data.price}")
                return flight_data
            except IndexError:
                print(f'couldnt find any flight for your destination {dest_code}')
                return None
        else:
            flight_data = FlightData(
                price=data['price'],
                origin_city=data['cityFrom'],
                origin_airport=data['route'][0]['flyFrom'],
                destination_city=data['cityTo'],
                destination_airport=data['route'][0]['flyTo'],
                out_date=data['route'][0]['local_departure'].split('T')[0],
                return_date=data['route'][1]['local_departure'].split('T')[0]
            )
            print(f"{flight_data.destination_city} : $ {flight_data.price}" )
            return flight_data

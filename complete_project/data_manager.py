import requests
from dotenv import load_dotenv
import os
from pprint import pprint
# for printing out data in formatted way

load_dotenv()

USERNAME=os.getenv("USERNAME")
FILE_NAME=os.getenv("FILE_NAME")
SHEETNAME=os.getenv("SHEETNAME")

GET_END_POINT= f"https://api.sheety.co/{USERNAME}/{FILE_NAME}/{SHEETNAME}"


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.data=None
        self.start()

    # this is for getting the text written in sheet
    def start(self):
        response=requests.get(url=GET_END_POINT)
        # print(pprint( response.json()))
        self.data=response.json()['prices']

    # now function for updating a row
    def update_row(self,dict):
        UPDATE_ENDPOINT = f"https://api.sheety.co/{USERNAME}/{FILE_NAME}/{SHEETNAME}/{dict['id']}"
        change_params={
            'price':{
            'city': f'{dict["city"]}',
            'iataCode' : f'{dict["iataCode"]}',
            'lowestPrice' : f'{dict["lowestPrice"]}'
        }
        }
        response=requests.put(url=UPDATE_ENDPOINT,json= change_params)
        print(response.status_code)
        print(response.text)


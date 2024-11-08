import os
import requests
from requests.auth import HTTPBasicAuth

from notification_manager import NotificationManager

SHEETY_API_ENDPOINT = 'https://api.sheety.co/2c3e1d40b4a9d85b3e040828660d4350/flightDeals/prices'

class DataManager:
    def __init__(self, flight_search):
        # private variable which will store username and password for sheety
        self._user = os.environ.get('SHEETY_USERNAME')
        self._password = os.environ.get('SHEETY_PASSWORD')
        # authorization will be needed for making api call
        self._authorization = HTTPBasicAuth(self._user, self._password)

        self.flight_search = flight_search
        self.destination_data = {}


    # TODO: fetch the data stored in google sheet using sheety api
    def get_destination_data(self):
        response = requests.get(url=SHEETY_API_ENDPOINT, auth=self._authorization)
        data = response.json()
        self.destination_data = data['prices']

    # TODO: for each row, update the iata code
    def update_destination_iata_code(self):
        for data in self.destination_data:
            new_city  = {
                'price': {
                    'iataCode': self.flight_search.get_airport_code(data['city'])
                }
            }
            requests.put(url=f'{SHEETY_API_ENDPOINT}/{data['id']}', json=new_city, auth=self._authorization)
        print('IATA code updated')

    # TODO: if flight fare is than the given price, then update the column
    def update_flight_details(self, source_iata, source_name, from_time, to_time):
        for data in self.destination_data:
            flight_data = self.flight_search.search_flights(
                source_airport= source_iata,
                destination_airport= data['iataCode'],
                from_time= from_time,
                to_time= to_time
            )
            print(len(flight_data))
            cheapest_flight = self.flight_search.search_cheapest_flight(flight_data)
            flight_deal = {
                'price': {
                    'deal': cheapest_flight['price'],
                    'travelDate': cheapest_flight['departure'].arrival_date,
                    'returnDate': cheapest_flight['return'].arrival_date,
                    'flight': cheapest_flight['flight_number'],
                    'seatsLeft': cheapest_flight['seatsLeft']
                }
            }
            requests.put(url=f'{SHEETY_API_ENDPOINT}/{data['id']}', json=flight_deal, auth=self._authorization)
            # creating letter
            NotificationManager.create_notification_text(
                source= source_name,
                destination= data['city'],
                price= cheapest_flight['price'],
                seats= cheapest_flight['seatsLeft']
            )
        print('Price updated')




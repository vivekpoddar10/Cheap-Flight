import os
import requests
from flight_data import FlightData

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:
    def __init__(self):
        self._api_key = os.environ.get('FLIGHT_API_KEY')
        self._api_secret = os.environ.get('FLIGHT_API_SECRET')
        self._token = self._get_new_token()

    # TODO: getting access token before using the api
    def _get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        return response.json()['access_token']

    # TODO: get city code for the given city name
    def get_airport_code(self, city_name):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)
        try:
            iata_code = response.json()['data'][0]['iataCode']
        except IndexError | KeyError:
            print(f'No Airport Found for {city_name}')
            return 'Not Found'
        return iata_code

    # TODO: Search flight from source to destination
    def search_flights(self, source_airport, destination_airport, from_time, to_time):
        flight_data = []
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": source_airport,
            "destinationLocationCode": destination_airport,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "INR",
            "max": "10",
        }
        response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params =query)
        if response.status_code != 200:
            print(response.text)
        else:
            for item in response.json()['data']:
                departure_flight_data = FlightData(
                    source_airport= item['itineraries'][0]['segments'][0]['departure']['iataCode'],
                    destination_airport= item['itineraries'][0]['segments'][0]['arrival']['iataCode'],
                    departure_date= item['itineraries'][0]['segments'][0]['departure']['at'].split('T')[0],
                    arrival_date = item['itineraries'][0]['segments'][0]['arrival']['at'].split('T')[0],
                )
                return_flight_data = FlightData(
                    source_airport= item['itineraries'][1]['segments'][0]['departure']['iataCode'],
                    destination_airport= item['itineraries'][1]['segments'][0]['arrival']['iataCode'],
                    departure_date= item['itineraries'][1]['segments'][0]['departure']['at'].split('T')[0],
                    arrival_date = item['itineraries'][1]['segments'][0]['arrival']['at'].split('T')[0],

                )
                flight_data.append(
                    {
                        'price': float(item['price']['grandTotal']),
                        'seatsLeft': item['numberOfBookableSeats'],
                        'departure': departure_flight_data,
                        'return': return_flight_data,
                        'flight_number': item['itineraries'][0]['segments'][0]['carrierCode']
                    }
                )
            return flight_data

    #TODO: from all the search flight return the flight with lowest price
    def search_cheapest_flight(self, flight_data):
        min_price = flight_data[0]['price']
        min_index = 0
        for i in range(len(flight_data)):
            if flight_data[i]['price'] < min_price:
                min_price = flight_data[i]['price']
                min_index = i
        return flight_data[min_index]







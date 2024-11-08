FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
class FlightData:
    def __init__(self, source_airport, destination_airport, departure_date, arrival_date):
        self.source_airport = source_airport
        self.destination_airport = destination_airport
        self.departure_date = departure_date
        self.arrival_date = arrival_date



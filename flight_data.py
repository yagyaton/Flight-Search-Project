from requests.models import to_key_val_list


class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin_city, destination_city, from_date, reach_date, origin_airport, destination_airport, to_date, airline, stop_overs=0, via=""):
        self.price=price
        self.origin_city=origin_city
        self.destination_city=destination_city
        self.from_date=from_date
        self.reach_date=reach_date
        self.origin_airport=origin_airport
        self.destionation_airport=destination_airport
        self.to_date=to_date
        self.airline=airline
        self.stop_overs=stop_overs
        self.via=via

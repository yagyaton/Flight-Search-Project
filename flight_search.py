import requests
from flight_data import FlightData
from pprint import pprint

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.endpoint="https://tequila-api.kiwi.com/"
        self.api_key="f9VRoJo-ACqpdMcwG-6iIAUXL4MbrfuE"
        self.headers={
            "apikey": self.api_key
            }
    def get_location_iata(self, city="Paris"):
        # query={
        #     "term": city,
        #     "location_types": "city"
        # }
        response=requests.get(url=f"{self.endpoint}locations/query?term={city}&location_types=city&limit=1", headers=self.headers)
        response.raise_for_status()
        # print(len(response.json()['locations']))
        code=response.json()['locations'][0]['code']
        return code

    def search_for_prices(self, origin_code, fly_to_code,  date_from, date_to):
        params={
            "fly_from": origin_code,
            "fly_to": fly_to_code,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "INR",
            # "price_to": lowestprice
        }

        response=requests.get(url=f"{self.endpoint}v2/search", params=params, headers=self.headers)
        response.raise_for_status()
        data=response.json()
        # print(type(data))
        # print(data)
        try: 
            iddata=data['data'][0]

        except IndexError: #Change stopover to 1 and run request again, return whatever you get.
            params['max_stopovers']=1
            response=requests.get(url=f"{self.endpoint}v2/search", params=params, headers=self.headers)
            response.raise_for_status()
            data=response.json()
            try: 
                iddata=data['data'][0]
                pprint(iddata)
            except IndexError: #Still no flights, return none.
                print(f"No flights to {fly_to_code}, not even with 1 stepover.")
                return None

            flight_data=FlightData(price=iddata['price'], 
                origin_city=f"{iddata['cityFrom']}-{iddata['cityCodeFrom']}",
                destination_city=f"{iddata['cityTo']}-{iddata['cityCodeTo']}",
                origin_airport=iddata['flyFrom'],
                destination_airport=iddata['flyTo'],
                from_date=iddata['route'][0]['local_departure'].split("T")[0],
                reach_date=iddata['route'][0]['local_arrival'].split("T")[0],
                to_date=iddata['route'][2]['local_departure'].split("T")[0], #Gives the starting date of 3rd flight, which marks starting of return journey.
                airline=iddata['airlines'],
                stop_overs=1,
                via=iddata["route"][0]["cityTo"] #This will give the first destination, which is the "via" route.
                )
            print(f"{flight_data.destination_city}: {flight_data.price}")
            return flight_data

        else: #This block will return data with 0 stopovers
            flight_data=FlightData(price=iddata['price'], 
                origin_city=f"{iddata['cityFrom']}-{iddata['cityCodeFrom']}",
                destination_city=f"{iddata['cityTo']}-{iddata['cityCodeTo']}",
                origin_airport=iddata['flyFrom'],
                destination_airport=iddata['flyTo'],
                from_date=iddata['route'][0]['local_departure'].split("T")[0],
                reach_date=iddata['route'][0]['local_arrival'].split("T")[0],
                to_date=iddata['route'][1]['local_departure'].split("T")[0],
                airline=iddata['airlines']
                )
            print(f"{flight_data.destination_city}: {flight_data.price}")
            return flight_data

    


# obj=FlightSearch()
# obj.search_for_prices("DEL", "LON", "04/07/2021", "03/12/2021")
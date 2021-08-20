#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
from notification_manager import NotificationManager



#At the beginning of every run, it will check if all the inputs have and iata entry or not, if not, will fill it automatically.
manager=DataManager()
flightsearch=FlightSearch()
sendsms=NotificationManager()



#If user wants to enter more destinations, they can do it here.
#This uses a different function, it will write a complete new row.
write_more=True
while write_more:  
    write_more=False
    if input("If you want to add mode destinations to search for, enter 'yes': ").lower()=="yes":
        manager.addnewcity()
        write_more=True




# from dateutil.relativedelta import relativedelta
# six_months = date.today() + relativedelta(months=+6)
#Finding cheapest prices from today - 6 months.
today=datetime.now()
sixmonths=datetime.now() + timedelta(days=180)
origincity='DEL'

for row in manager.sheet_data:
    
    flight=flightsearch.search_for_prices(origin_code=origincity, 
        fly_to_code=row['iataCode'], 
        date_from=today.strftime("%d/%m/%Y"), 
        date_to=sixmonths.strftime("%d/%m/%Y")
        )
    if flight!=None and flight.price<row['lowestPrice']:
        sendsms.sendnotification(flight.origin_city, 
            flight.destination_city, 
            flight.origin_airport,
            flight.destionation_airport,
            flight.from_date, 
            flight.to_date, 
            flight.price, 
            maillist=manager.mail_list, 
            stopover=flight.stop_overs, 
            via=flight.via)





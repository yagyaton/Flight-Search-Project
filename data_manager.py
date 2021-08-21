import requests
from flight_search import FlightSearch

token="yoursheetytoken"
bearer_headers={
    "Authorization": f"Bearer {token}"
}
price_endpoint="https://api.sheety.co/f0d0f9070b166b7156b4985e92523e03/flightDeals/prices"
maillist_endpoint="https://api.sheety.co/f0d0f9070b166b7156b4985e92523e03/flightDeals/userMailingList"
# self.put_endpoint=f"{self.get_endpoint}/{row}"
class DataManager(FlightSearch):
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        super().__init__()
        self.sheet_data={}
        self.mail_list=[]
        self.getrows()  #To initially fill values in sheet_data
        self.getmaillist()  #To initially fill the values in mail_list, which, unlike sheet_data, do not change in the course of the exection of the program.

    #Getting all destination data (Name, iataCode, LowestPrices)
    def getrows(self):
        response=requests.get(url=price_endpoint, headers=bearer_headers)
        response.raise_for_status()
        self.sheet_data=response.json()['prices']
        print(self.sheet_data)
    

    #Write new rows into the destination and price sheet.
    def writerow(self, city, iata, price):
        query={
            "price": {
                "city": city,
                "iataCode": iata,
                "lowestPrice": price
            }
        }
        response=requests.post(url=price_endpoint, json=query, headers=bearer_headers)
        response.raise_for_status()
        print(response.text)
        self.getrows()
    
    #If a row is already there but their IATA codes aren't.
    #First in a for loop call the 
    def editrow(self):
        #Will fill the dictionary with all the sheety data.
        anychange=0
        for row in self.sheet_data:
            if row['iataCode']=="":
                anychange+=1
                row['iataCode']=self.get_location_iata(row['city'])
                prices={
                    "price": {
                        "iataCode": row['iataCode']
                    }
                }
                response=requests.put(url=f"{price_endpoint}/{row['id']}", json=prices, headers=bearer_headers)
                # response.raise_for_status()
                print(response.text)
        if anychange>0:
            self.getrows() #Only call it if any change has been made, to save API calls.

    #Takes user input and calls the writerow function to enter data into the sheet as a new row.
    def addnewcity(self):
        city=input("Enter a new city that you'd want to travel to: ")
        price=int(input("What's the maximum plane fare price you are looking for: "))
        code=self.get_location_iata(city)
        self.writerow(city, code, price)

    #Gets all user rows and saves the mail ids into a list and returns that list.
    def getmaillist(self):
        response=requests.get(url=maillist_endpoint, headers=bearer_headers)
        database=response.json()
        # print(database)
        for row in database['userMailingList']:
            self.mail_list.append(row['mailId'])
        print(self.mail_list)
        # return self.mail_list
        # I don't need to return mail list anywhere, since I'll just access the attribute self.mail_list from the object of the class.      


# obj=DataManager()
# obj.getrows()

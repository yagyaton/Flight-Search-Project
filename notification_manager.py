from twilio.rest import Client
import smtplib

#Code won't run, all keys and numbers are removed. Use your own if you need to.

id=yahooid
password=yahoopass
yahooport="smtp.mail.yahoo.com"
account_sid=sid
auth_token=auth

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def sendnotification(self, origin_city, destination_city, origin_airport, dest_airport, from_date, to_date, price, maillist, stopover, via):
        mainbody=""
        googleflighhtlink=f"https://www.google.co.in/flights?hl=en#flt={origin_airport}.{dest_airport}.{from_date}*{dest_airport}.{origin_airport}.{to_date}"
        if stopover==0:
            mainbody=f"Only ₹{price} to fly from {origin_city} to {destination_city}, from {from_date} to {to_date}!\n{googleflighhtlink}"
        else:
            mainbody=f"Only ₹{price} to fly from {origin_city} to {destination_city}, from {from_date} to {to_date}!\nFlight has {stopover} stop over, via {via} city.\n{googleflighhtlink}"
        #First, sending the sms.
        client=Client(account_sid, auth_token) 
        message = client.messages \
            .create(
                     body=f"\nLow Price Alert!\n{mainbody}".encode('utf-8'),
                     from_='twiliono',
                     to='my_no'
                 )

        print(message.status)

        #Now, sending the mail.
        with smtplib.SMTP(yahooport, 587) as mailer:
            mailer.starttls()
            mailer.login(user=id, password=password)
            mailer.sendmail(from_addr=id, to_addrs=maillist, msg=f"Subject:Low Price Alert!\n\n{mainbody}".encode('utf-8'))

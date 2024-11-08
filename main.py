import os
from datetime import datetime

from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

email = os.environ.get('SMTP_EMAIL')
password = os.environ.get('SMTP_PASSWORD')

to_email = 'sender@gmail.com'

today = datetime(year=2024, month=12, day=7)
to_time = datetime(year=2025, month=1, day=10)

flight_search = FlightSearch()
data_manager = DataManager(flight_search)

# getting the google sheet data
data_manager.get_destination_data()

# updating the sheet with flight price, travel date
# creating notification text
data_manager.update_flight_details(source_iata='DEL', source_name='Delhi' ,from_time=today, to_time=to_time)

# sending the notification
NotificationManager.send_notification(email, password, to_email)


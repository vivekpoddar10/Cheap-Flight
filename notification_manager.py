import smtplib
from pathlib import Path

class NotificationManager:
    @staticmethod
    def create_notification_text(source, destination, price, seats):
        replacement = {
            '[source]': source,
            '[destination]': destination,
            '[price]': str(price),
            '[seats]': str(seats)
        }

        with open('mail.txt', 'r') as file:
            data = file.read()
            text = data
            for old, new in replacement.items():
                text = text.replace(old, new)

        with open(f'./notification/{source} - {destination}.txt', 'w') as file:
            file.write(text)

    @staticmethod
    def send_notification(email, password, to_email):
        directory = Path('./notification')
        for file in directory.glob('*.txt'):
            title = file.name.rstrip('.txt')

            with open(file, 'r') as f:
                content = f.read()

            with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()
                connection.login(email, password)
                connection.sendmail(email, to_email, msg=f'Subject:Hurry! Getting Deal on {title} flight\n\n{content}')
                print(f'Email send for {title}')


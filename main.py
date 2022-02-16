import requests
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
import os

BASE_URL = "https://discord.com/api/v9"
CHANNEL_ID = os.environ.get("DISCORD_CHANNEL_ID")
API_TOKEN = os.environ.get("DISCORD_API_TOKEN")

def send_email(message):

    # assign key email aspects to variables for easier future editing
    subject = "Tip diario de ciberseguridad"
    body = message
    sender_email = "bot@altaplazamall.com"
    receiver_email = "soporte@altaplazamall.com"
    email=MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email 
    email["Subject"] = subject
    email.attach(MIMEText(body, "plain"))

    report = MIMEBase("application", "octate-stream")
    session = smtplib.SMTP('smtp-relay.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    text = email.as_string()
    session.sendmail(sender_email, receiver_email, text)
    session.quit()
    print('Mail Sent')
    

def get_messages(chanel_id):

    header = {
        "Authorization": API_TOKEN
    }

    parameters = {
        "limit":1
    }
    url_get_messages = f"{BASE_URL}/channels/{chanel_id}/messages"
    response = requests.get(url=url_get_messages, params=parameters, headers=header)
    data = json.loads(response.text)

    message = data[0]['content']
    send_email(message)


get_messages(CHANNEL_ID)

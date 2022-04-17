import requests
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import smtplib
import os
from PIL import Image, ImageFont, ImageDraw

### Other way to send emails
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes


BASE_URL = "https://discord.com/api/v9"
CHANNEL_ID = os.environ.get("DISCORD_CHANNEL_ID")
API_TOKEN = os.environ.get("DISCORD_API_TOKEN")


def create_image(message):

    my_image = Image.open("bot.jpeg")

    title_font = ImageFont.truetype(font="Ubuntu-Regular.ttf", size=20)

    title_text = message.strip("Buenos días estimad@s, les traigo el tip mañanero:")

    spaces = 25
    i = 0
    final_text = (
        "         Buenos días estimad@s, \n         les traigo el cyber tip del día:\n"
    )
    for char in title_text:
        # if i % spaces < 6 and char == " ":
        if i >= spaces and char == " ":
            final_text += "\n"
            final_text += char
            i = 0
        else:
            i += 1
            final_text += char

    image_editable = ImageDraw.Draw(my_image)

    image_editable.text((290, 85), final_text, (0, 0, 0), font=title_font)

    my_image.save("bot-message.jpg")


def send_email(message):

    create_image(message)

    # assign key email aspects to variables for easier future editing
    subject = "El tip diario de ciberseguridad"
    body = message
    sender_email = "bot@altaplazamall.com"
    receiver_email = "soporte@altaplazamall.com"
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email
    email["Subject"] = subject
    email.attach(MIMEText(body, "plain"))
    image = MIMEImage(open("bot-message.jpg", "rb").read())
    # image.add_header('Content-ID', '<image1>')
    image.add_header(
        "content-disposition", "attachment", filename="%s" % "bot-message.jpg"
    )
    email.attach(image)
    report = MIMEBase("application", "octate-stream")
    session = smtplib.SMTP("smtp-relay.gmail.com", 587)  # use gmail with port
    session.starttls()  # enable security
    text = email.as_string()
    session.sendmail(sender_email, receiver_email, text)
    session.quit()
    print("Mail Sent")


def get_messages(chanel_id):

    header = {"Authorization": API_TOKEN}

    parameters = {"limit": 1}
    url_get_messages = f"{BASE_URL}/channels/{chanel_id}/messages"
    response = requests.get(url=url_get_messages, params=parameters, headers=header)
    data = json.loads(response.text)

    message = data[0]["content"]
    # create_image(message)
    # send_email(message)
    send_html_mail(message)


def send_html_mail(message):
    create_image(message)
    msg = EmailMessage()

    # generic email headers
    msg["Subject"] = "El tip diario de ciberseguridad"
    msg["From"] = "Bot Altaplaza <bot@altaplazamall.com>"
    msg["To"] = "Soporte Altaplaza <soporte@altaplazamall.com>"

    # set the plain text body
    msg.set_content("Hola estimad@s les traigo el cyber tip del día.")

    # now create a Content-ID for the image
    image_cid = make_msgid(domain="altaplazamall.com")
    # if `domain` argument isn't provided, it will
    # use your computer's name

    # set an alternative html body
    msg.add_alternative(
        """\
    <html>
        <body>
            <img src="cid:{image_cid}">
        </body>
    </html>
    """.format(
            image_cid=image_cid[1:-1]
        ),
        subtype="html",
    )
    # image_cid looks like <long.random.number@xyz.com>
    # to use it as the img src, we don't need `<` or `>`
    # so we use [1:-1] to strip them off

    # now open the image and attach it to the email
    with open("bot-message.jpg", "rb") as img:

        # know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split("/")

        # attach it
        msg.get_payload()[1].add_related(
            img.read(), maintype=maintype, subtype=subtype, cid=image_cid
        )

    # the message is ready now
    # you can write it to a file
    # or send it using smtplib
    sender_email = "bot@altaplazamall.com"
    receiver_email = "soporte@altaplazamall.com"
    session = smtplib.SMTP("smtp-relay.gmail.com", 587)  # use gmail with port
    session.starttls()  # enable security
    text = msg.as_string()
    session.sendmail(sender_email, receiver_email, text)
    session.quit()
    print("Mail Sent")


get_messages(CHANNEL_ID)

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

"""
Bulk emailer for sending emails to students.

FIXME: Cannot bulk sending --> wrong methods, take longs to send --> queueing issue.
"""

def send_email(info: dict):
    msg = MIMEMultipart()
    msg["From"] = info["from"]
    msg["To"] = info["to"]
    msg["Subject"] = info["subject"]

    template = info["template"]
    code = info["code"]

    with open(f"./template/ied23.html") as template: # TODO: Replace with information from the database
        body = template.read().replace("[code]", info['code'])
        body = body.replace("[name]", info['name'])
        body = body.replace("(#000000)", '(' + info['number'] + ')')
        msg.attach(MIMEText(body, "html"))

    with open(f"./qrcodes/{code}.png", "rb") as attachment:
        img = MIMEImage(attachment.read())
        img.add_header('Content-ID', 'qr')
        msg.attach(img)


    text = msg.as_string()

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(info['from'], info['key'])
    server.sendmail(info['from'], info['to'], text)
    server.quit()



if __name__ == "__main__":
    info = {
    "from": "presto@vgu.edu.vn",
    "to":"10422021@student.vgu.edu.vn",
    "subject": "[IED23] Entrance Ticket",
    "template": "ied23.html",
    "name": "CSE2022",
    "number": "#CSE2022",
    "code": "CSE2022",
    "key": ""
    }

    send_email(info)
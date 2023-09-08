import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

sender = "fuisloy@gmail.com"
receiver = "10621018@student.vgu.edu.vn"

def send_email(code):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "[Presto] VGU By Night Ticket"

    with open(f"bin/template/email_template.html") as template: # TODO: Replace with information from the database
        body = template.read().replace("[code]", code)
        body = body.replace("[name]", "Phuong Linh")
        body = body.replace("(#000000)", "(#10621018)")
        msg.attach(MIMEText(body, "html"))

    with open(f"bin/qrcodes/{code}.png", "rb") as attachment:
        img = MIMEImage(attachment.read())
        img.add_header('Content-ID', 'qr')
        msg.attach(img)


    text = msg.as_string()

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(sender, "zzsfmfvfposwxqwh")
    server.sendmail(sender, receiver, text)
    server.quit()

if __name__ == "__main__":
    send_email('V79OC3')
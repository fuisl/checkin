import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class Emailer:
    '''
    Emailer class for sending tickets.
    '''
    def __init__(self, server="smtp.gmail.com", port=587):
        self.server = smtplib.SMTP(server, port)
        self.server.ehlo()
        self.server.starttls()
        self.login_status = False

    def login(self, email, password):
        """
        Login to the email server. Must be called before sending email.

        :param email: str --> email address
        :param password: str --> password
        """
        try:
            self.from_email = email
            self.server.login(email, password)
            self.login_status = True
            self.server.sendmail(self.from_email, "10422021@student.vgu.edu.vn", "Server is ready to send email.")
        
        except smtplib.SMTPResponseException as e:
            print("smtplib.SMTPResponseException: " + str(e.smtp_code) + " " + str(e.smtp_error))

    def send(self, info: dict):
        if not self.login_status:
            raise Exception("You must login to use this feature!")
        
        msg = self.content(info)

        try:
            self.server.sendmail(self.from_email, info["to"], msg)
        except smtplib.SMTPResponseException as e:
            print("smtplib.SMTPResponseException: " + str(e.smtp_code) + " " + str(e.smtp_error))
            return 1
        
    def send(self, infos: list):
        """
        Send email in bulks.

        :param infos: list --> list of dict, dict format in content
        """
        if not self.login_status:
            raise Exception("You must login to use this feature!")
        
        for info in infos:
            """
            for each ticket, send email.
            """
            self.send(info)

        return 0  # Success

    @staticmethod
    def content(self, info: dict):
        """
        Return content as string for sending email.

        :param info: dict --> information of the ticket
            - subject: str
            - to: str
            - name: str
            - code: str
            - ...: str
        """
        msg = MIMEMultipart()
        msg['Subject'] = info['subject']
        msg['From'] = self.from_email
        msg['To'] = info['to']

        template = ""  # path to template

        with open(template, 'r') as file:
            """
            Read the template file and replace all place holder with values.
            """
            content = file.read()
            content = content.replace("[code]", "codehere")
            content = content.replace("[name]", "namehere")
            content = content.replace("(#000000)", '(' + "#000000" + ')')
            # Replace all place holder with values. Why don't just use f"{}"? --> more control over the content
            msg.attach(MIMEText(content, 'html'))

        with open("path/to/QRCode", 'rb') as file:
            """
            Attach QR code to the email and place to the content.
            """
            img = MIMEImage(file.read())
            img.add_header('Content-ID', 'qr')  # Content-ID is used to refer to the image in the HTML content --> <img src="cid:qr">
            msg.attach(img)

        return msg.as_string()
    
    def __del__(self):
        self.server.quit()
        self.login_status = False
from email.message import EmailMessage
import ssl
import smtplib  

class EmailInterface:

    def __init__(self):
        self.email_sender = "cameronbaabsprinterhealthtest@gmail.com" # Test Account
        self.app_password = "segbkkbotmisvhbl"

    def send_email(self, email_receiver: str, subject: str, body: str) -> None:
        em = EmailMessage()
        em['From'] = self.email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_sender, self.app_password)
            smtp.sendmail(self.email_sender, email_receiver, em.as_string())
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


class EmailService:
    def __init__(self):
        self.from_addr = settings.MY_EMAIL_ADDRESS
        # пароль для mail.ru создается в настройках для внешних приложений
        self.my_email_pass = settings.MY_EMAIL_PASSWORD

    async def send_register_message(self, to_addr: str, to_name: str):
        msg = MIMEMultipart()
        msg['From'] = self.from_addr
        msg['To'] = to_addr
        msg['Subject'] = "Привет от питона"

        body = f"Это пробное сообщение. Привет {to_name}!"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL(settings.MY_SMTP_SERVER, 465)
        server.login(self.from_addr, self.my_email_pass)
        text = msg.as_string()
        server.sendmail(from_addr=self.from_addr, to_addrs=to_addr, msg=text)
        server.quit()


async def get_email():
    yield EmailService()

import smtplib
import logging
from settings import Settings
from email.message import EmailMessage


class EmailHandler:

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.settings = Settings()  # pyright: ignore[reportCallIssue]

    def build_message(self, from_address, to_address, message_text):
        msg = EmailMessage()
        msg["Subject"] = f"New SMS from {from_address}"
        msg["From"] = self.settings.smtp_from_address
        msg["To"] = to_address
        msg.set_content(f"{message_text}")
        self.send_message(to_address, msg)

    def send_message(self, to_address, msg):
        try:
            with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(self.settings.smtp_user, self.settings.smtp_pass)
                smtp.send_message(msg)
        except smtplib.SMTPSenderRefused as e:
            self.logger.warning(f"Sender refused: {e.smtp_code} - {e.smtp_error}")
        except smtplib.SMTPRecipientsRefused as e:
            for email, details in e.recipients.items():
                status_code = details[0]
                error_message = details[1]
                self.logger.warning(
                    f"Recipient: {email} | Code: {status_code} | Msg: {error_message} has been received from SMTP server"
                )
        self.logger.info(f"Email sent successfully to {to_address}")

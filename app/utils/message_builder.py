from email.mime.text import MIMEText
import base64

class MessageBuilder:
    @staticmethod
    def create_plain_message(sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes())
        return {'raw': raw_message.decode()}

    @staticmethod
    def create_html_message(sender, to, subject, html_content):
        message = MIMEText(html_content, "html")
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes())
        return {'raw': raw_message.decode()}
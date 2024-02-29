from ..models.email import EmailConfig


def load_email_config(dct: dict):
    return EmailConfig(
        sender_email=dct.get("email"),
        sender_login=dct.get("login"),
        sender_password=dct.get("password"),
        mail_server=dct.get("mail_server"),
        port=dct.get("port")
    )

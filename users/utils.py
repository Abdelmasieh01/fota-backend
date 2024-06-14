from django.core.mail import send_mail
from django.template.loader import get_template


def send_confirmation_email(email, token_id, user_id, host):
    if host == "localhost:8000":
        link = "http://localhost:8000/users/confirm-email?token_id={0}&user_id={1}".format(
            token_id, user_id)
    else:
        link = "https://{0}/users/confirm-email?token_id={1}&user_id={2}".format(
            host, token_id, user_id)
        
    message = get_template("users/email_template.txt").render({"link": link})
    send_mail(
        subject="Email Confirmation for FOTA SDV",
        message=message,
        from_email="gokuabdo31@gmail.com",
        recipient_list=[email],
        fail_silently=True
    )

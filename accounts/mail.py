from django.core.mail import send_mail
from django.template.loader import render_to_string
from huey.contrib import djhuey as huey

SUBJECT = "Confirm Your Account"


@huey.task()
def send_confirmation_email(user):
    html = render_to_string("accounts/mail.html", {"user": user})
    send_mail(
        SUBJECT,
        message=f"Confirmation Code: {user['confirmation_code']}",
        from_email="noreply@propertyhub.eniola.xyz",
        recipient_list=[user["email"]],
        html_message=html,
    )

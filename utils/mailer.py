from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template

from app import settings


def send_reset_password_email(to, url):
    subject = 'Reset Password'
    from_email = settings.EMAIL_HOST_USER
    template = get_template('reset_password.html')
    msg = EmailMultiAlternatives(subject, None, from_email, [to])
    msg.attach_alternative(template.render({'url': url}), "text/html")
    msg.send()

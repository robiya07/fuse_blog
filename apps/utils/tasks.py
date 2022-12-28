from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.models import User
from apps.utils.tokens import account_activation_token
from root.settings import EMAIL_HOST_USER


@shared_task
def send_email(email, message, subject):
    print('start')
    from_email = EMAIL_HOST_USER
    recipient_list = [email]
    result = send_mail(subject, message, from_email, recipient_list)
    print('finish')
    return result


@shared_task
def send_to_gmail(email, domain, _type):
    from_email = EMAIL_HOST_USER
    user = User.objects.filter(email=email).first()
    recipient_list = [email]
    template = 'auth/activation-account.html'
    message = render_to_string(template, {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(str(user.pk))),
        'token': account_activation_token.make_token(user),
        'type': _type
    })
    if _type == 'activate':
        subject = 'Activate your account'
    elif _type == 'reset':
        print('Accept task')
        subject = 'Reset your password'
    else:
        raise ValueError
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    result = email.send()
    print('Send mail')
    return result

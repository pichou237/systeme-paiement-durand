import random
from django.core.mail import EmailMessage
from .models import User, OneTimePasscode
from django.conf import settings

def generateOtp(): # or we can use the library pyotp
    otp = ""
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp

def send_code_to_user(email):
    subject = "one time code password for email verification"
    otp_code = generateOtp()
    user = User.objects.get(email=email)
    current_site = "pamelfichieu.com"
    email_body = f"Hi {user.first_name}, thanks for signing up on {current_site} please verify your email with the \n one time passcode {otp_code}"
    from_email = settings.EMAIL_HOST_USER

    OneTimePasscode.objects.create(user=user, code=otp_code)

    d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    d_email.send(fail_silently=True)

def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()

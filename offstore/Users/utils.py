import random
from django.core.mail import EmailMessage
from .models import User, OneTimePasscode
from django.conf import settings
import logging
from django.utils import timezone
logger = logging.getLogger(__name__)

def generateOtp(): # or we can use the library pyotp
    otp = ""
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp

def send_code_to_user(email_data):
    email = email_data['to_email']
    user = User.objects.filter(email=email).first()

    if not user:
        logger.error(f"Utilisateur avec l'email {email} n'existe pas.")
        return False

    subject = email_data['email_subject']
    otp_code = generateOtp()
    current_site = settings.CURRENT_SITE  # Rendre configurable
    email_body = f"Hi {user.first_name}, thanks for signing up on {current_site}. Please verify your email with the one-time passcode: {otp_code}"
    from_email = settings.EMAIL_HOST_USER

    # Mettre à jour ou créer un OTP pour l'utilisateur
    OneTimePasscode.objects.update_or_create(
        user=user,
        defaults={'code': otp_code, 'expires_at': timezone.now() + timezone.timedelta(minutes=10)}
    )

    # Envoyer l'email
    try:
        d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
        d_email.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email : {e}")
        return False
    
def send_normal_email(data):
    try:
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']]
        )
        email.send()
        return True
    except Exception as e:
        # Log l'erreur pour le débogage
        logger.error(f"Erreur lors de l'envoi de l'email : {e}")
        return False
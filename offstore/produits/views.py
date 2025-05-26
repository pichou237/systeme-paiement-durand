from django.shortcuts import render
import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

@csrf_exempt
def stripe_webhook(request):
    if request.method != "POST":
        return HttpResponse("Méthode non autorisée", status=405)

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    if sig_header is None:
        return HttpResponse("Signature manquante", status=400)

    endpoint_secret = 'ton_webhook_secret'

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse("Payload invalide", status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse("Signature invalide", status=400)

    if event['type'] == 'payment_intent.succeeded':
        print("✅ Paiement réussi reçu")

    return HttpResponse(status=200)


# Create your views here.

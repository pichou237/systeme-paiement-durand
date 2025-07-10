import stripe
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment
import datetime
import json
from .serializers import PaymentSerializer
from .enums import PaymentStatus

stripe.api_key = settings.STRIPE_SECRET_KEY

@method_decorator(csrf_exempt, name='dispatch')
class CreateStripeCheckoutSession(APIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        try:
            amount = float(data.get("amount"))  # ex: 19.99
            currency = data.get("currency", "usd")

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': data.get("product_name", "Produit"),
                        },
                        'unit_amount': int(amount * 100),  # cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.SITE_URL + reverse('payment_success'),
                cancel_url=settings.SITE_URL + reverse('payment_cancel'),
                customer_email=user.email,
                metadata={
                    'user_id': user.id,
                }
            )

            return Response({"checkout_url": checkout_session.url})

        except Exception as e:
            return Response({"error": str(e)}, status=500)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        try:
            user_id = session['metadata']['user_id']
            amount_total = session['amount_total'] / 100
            currency = session['currency'].upper()
            payment_intent = session['payment_intent']

            Payment.objects.create(
                user_id=user_id,
                amount=amount_total,
                currency=currency,
                status=PaymentStatus.REUSSI,  # utilise l'enum
                transaction_id=payment_intent,
                date_time=datetime.datetime.now()
            )

        except KeyError as e:
            # En cas de champ manquant dans metadata ou session
            return HttpResponse(status=400)

    return HttpResponse(status=200)

# Pages de redirection
def payment_success(request):
    return HttpResponse("✅ Paiement réussi. Merci pour votre achat.")

def payment_cancel(request):
    return HttpResponse("❌ Paiement annulé. Vous pouvez réessayer.")

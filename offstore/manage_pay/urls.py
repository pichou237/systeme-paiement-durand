from django.urls import path
from .views import (
    CreateStripeCheckoutSession,
    stripe_webhook,
    payment_success,
    payment_cancel,
)

urlpatterns = [
    path('create-checkout-session/', CreateStripeCheckoutSession.as_view(), name='create_checkout_session'),
    path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
]

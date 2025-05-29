from django.db import models

# Create your models here.
from django.db import models 
from .enums import PaymentMethod, PaymentStatus, Currency
from Users.models import User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.EUR)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.EN_COURS)
    date_time = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-date_time']
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'

    def __str__(self):
        return f"{self.user.email} | {self.amount} {self.currency} | {self.payment_method} | {self.status}"

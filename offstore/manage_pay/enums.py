from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentMethod(models.TextChoices):
    STRIPE: Any = "STRIPE", _("Stripe")

    @classmethod
    def values(cls):
        return [choice.value for choice in cls]


class PaymentStatus(models.TextChoices):
    EN_COURS: Any = "EN COURS", _("En cours")
    REUSSI: Any = "REUSSI", _("Réussi")
    ECHOUE: Any = "ECHOUE", _("Échoué")

    @classmethod
    def values(cls):
        return [choice.value for choice in cls]


class Currency(models.TextChoices):
    EUR: Any = "EUR", _("Euro")
    USD: Any = "USD", _("Dollar")
    GBP: Any = "GBP", _("Livre")
    JPY: Any = "JPY", _("Yen")
    CNY: Any = "CNY", _("Yuan") 
    RUB: Any = "RUB", _("Rouble")
    INR: Any = "INR", _("Roupie")
    BRL: Any = "BRL", _("Real")
    AUD: Any = "AUD", _("Dollar australien")
    CAD: Any = "CAD", _("Dollar canadien")
    CHF: Any = "CHF", _("Franc suisse")
    NZD: Any = "NZD", _("Dollar néo-zélandais")
    MXN: Any = "MXN", _("Peso mexicain")
    AED: Any = "AED", _("Dirham des Émirats")
    ZAR: Any = "ZAR", _("Rand sud-africain")
    TRY: Any = "TRY", _("Lira turque")
    PKR: Any = "PKR", _("Roupie pakistanaise")
    XAF: Any = "XAF", _("Franc CFA (BEAC)")
    XCD: Any = "XCD", _("Dollar des Caraïbes orientales")
    XOF: Any = "XOF", _("Franc CFA (BCEAO)")
    XPF: Any = "XPF", _("Franc Pacifique")

    @classmethod
    def values(cls):
        return [choice.value for choice in cls]

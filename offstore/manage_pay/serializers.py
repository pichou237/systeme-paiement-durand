from rest_framework import serializers
from .models import Payment
from .enums import PaymentMethod, Currency, PaymentStatus

class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.ChoiceField(choices=PaymentMethod.choices)
    currency = serializers.ChoiceField(choices=Currency.choices)
    status = serializers.ChoiceField(choices=PaymentStatus.choices, read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'payment_method', 'currency', 'status', 'date_time', 'transaction_id']
        read_only_fields = ['id', 'user', 'status', 'date_time', 'transaction_id']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['status'] = PaymentStatus.en_cours  # exactement comme dans l'enum
        payment = super().create(validated_data)
        return payment


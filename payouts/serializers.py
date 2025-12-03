from rest_framework import serializers
from .models import Payout


class PayoutSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и чтения заявок на выплату."""

    class Meta:
        model = Payout
        fields = ['id', 'amount', 'currency', 'recipient_details', 'status', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def validate_amount(self, value):
        """Проверка что сумма положительная."""
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть положительной.")
        return value

    def validate_currency(self, value):
        """Проверка что валюта - 3-буквенный код."""
        if len(value) != 3 or not value.isalpha():
            raise serializers.ValidationError("Валюта должна быть 3-буквенным кодом (например: RUB, USD, EUR).")
        return value.upper()

    def validate_recipient_details(self, value):
        """Проверка что реквизиты получателя - непустой JSON объект."""
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Реквизиты получателя должны быть JSON объектом, например: "
                '{"account": "40817810099910004312", "bank": "Сбербанк"}'
            )
        if not value:
            raise serializers.ValidationError("Реквизиты получателя не могут быть пустыми.")
        return value


class PayoutUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления статуса заявки."""

    class Meta:
        model = Payout
        fields = ['status', 'updated_at']
        read_only_fields = ['updated_at']

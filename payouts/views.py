from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Payout
from .selectors import get_payout, list_payouts
from .serializers import PayoutSerializer, PayoutUpdateSerializer
from .services import PayoutService
from .tasks import process_payout


class PayoutViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для управления заявками на выплату."""

    service = PayoutService()
    queryset = Payout.objects.all()

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        if self.action in ["update", "partial_update"]:
            return PayoutUpdateSerializer
        return PayoutSerializer

    def get_queryset(self):
        """Получение списка заявок."""
        return list_payouts()

    def get_object(self):
        """Получение одной заявки по ID."""
        return get_payout(self.kwargs["pk"])

    def create(self, request, *args, **kwargs):
        """Создание новой заявки и запуск асинхронной обработки."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payout = self.service.create_payout(serializer.validated_data)
        process_payout.delay(str(payout.id))
        output = PayoutSerializer(payout)
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление заявки (обычно статуса)."""
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if "status" not in serializer.validated_data:
            return Response(
                {"status": ["Это поле обязательно для обновления."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        payout = self.service.set_status(kwargs["pk"], serializer.validated_data["status"])
        output = PayoutSerializer(payout)
        return Response(output.data)

    def destroy(self, request, *args, **kwargs):
        """Удаление заявки."""
        self.service.delete_payout(kwargs["pk"])
        return Response(status=status.HTTP_204_NO_CONTENT)

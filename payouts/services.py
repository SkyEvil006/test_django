from typing import Any, Dict

from django.shortcuts import get_object_or_404

from .models import Payout
from .repositories import PayoutRepository


class PayoutService:
    """Сервис для бизнес-логики работы с заявками на выплату."""

    def __init__(self, repository: PayoutRepository | None = None) -> None:
        self.repository = repository or PayoutRepository()

    def get(self, payout_id) -> Payout:
        """Получение заявки по ID."""
        return get_object_or_404(Payout, id=payout_id)

    def create_payout(self, data: Dict[str, Any]) -> Payout:
        """Создание новой заявки."""
        return self.repository.create(**data)

    def set_status(self, payout_id, status: str) -> Payout:
        """Изменение статуса заявки."""
        payout = get_object_or_404(Payout, id=payout_id)
        payout.status = status
        return self.repository.save(payout, update_fields=["status", "updated_at"])

    def delete_payout(self, payout_id) -> None:
        """Удаление заявки."""
        payout = get_object_or_404(Payout, id=payout_id)
        self.repository.delete(payout)

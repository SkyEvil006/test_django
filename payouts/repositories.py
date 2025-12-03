from typing import Iterable

from .models import Payout


class PayoutRepository:
    """Репозиторий для работы с базой данных заявок на выплату."""

    def create(self, **data) -> Payout:
        """Создание новой заявки в БД."""
        return Payout.objects.create(**data)

    def list_all(self) -> Iterable[Payout]:
        """Получение всех заявок."""
        return Payout.objects.all()

    def get(self, payout_id) -> Payout:
        """Получение заявки по ID."""
        return Payout.objects.get(id=payout_id)

    def save(self, payout: Payout, update_fields: list[str] | None = None) -> Payout:
        """Сохранение изменений заявки."""
        payout.save(update_fields=update_fields)
        return payout

    def delete(self, payout: Payout) -> None:
        """Удаление заявки из БД."""
        payout.delete()

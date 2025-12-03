from django.shortcuts import get_object_or_404

from .models import Payout
from .repositories import PayoutRepository

repository = PayoutRepository()


def list_payouts():
    """Получение списка всех заявок."""
    return repository.list_all()


def get_payout(payout_id):
    """Получение одной заявки по ID."""
    return get_object_or_404(Payout, id=payout_id)

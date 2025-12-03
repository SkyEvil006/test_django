from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Payout(models.Model):
    """Модель заявки на выплату средств."""

    class Status(models.TextChoices):
        """Статусы обработки заявки."""
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    currency = models.CharField(max_length=3, default='USD')
    recipient_details = models.JSONField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Строковое представление заявки."""
        return f"Payout {self.id} - {self.amount} {self.currency}"

    class Meta:
        ordering = ['-created_at']

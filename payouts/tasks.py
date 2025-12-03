import logging
import random
import time

from celery import shared_task

from .models import Payout
from .services import PayoutService

logger = logging.getLogger(__name__)


@shared_task
def process_payout(payout_id: str):
    """
    Process payout asynchronously.

    Args:
        payout_id: UUID of the payout to process

    Returns:
        dict: Processing result with status and payout_id
    """
    service = PayoutService()
    logger.info(f"Starting payout processing for payout_id={payout_id}")

    try:
        # Mark as processing
        payout = service.set_status(payout_id, Payout.Status.PROCESSING)
        logger.info(f"Payout {payout_id} marked as PROCESSING. Amount: {payout.amount} {payout.currency}")

        # Simulate processing delay
        time.sleep(2)
        logger.debug(f"Processing simulation completed for payout {payout_id}")

        # Randomly determine final status (simulate success/failure)
        final_status = Payout.Status.COMPLETED if random.choice([True, False]) else Payout.Status.FAILED

        # Update final status
        service.set_status(payout_id, final_status)
        logger.info(
            f"Payout {payout_id} processing finished with status: {final_status}. "
            f"Amount: {payout.amount} {payout.currency}"
        )

        return {"status": final_status, "payout_id": str(payout_id)}

    except Payout.DoesNotExist:
        logger.error(f"Payout {payout_id} not found. Cannot process.")
        return {"status": "error", "message": "Payout not found", "payout_id": str(payout_id)}
    except Exception as e:
        logger.exception(f"Unexpected error processing payout {payout_id}: {str(e)}")
        try:
            service.set_status(payout_id, Payout.Status.FAILED)
        except Exception:
            logger.exception(f"Failed to set FAILED status for payout {payout_id}")
        return {"status": "error", "message": str(e), "payout_id": str(payout_id)}

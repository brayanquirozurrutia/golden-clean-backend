from celery import shared_task
from service.utils import notify_employees_by_proximity
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def notify_employees_task(self, service_id, description, client_lat, client_lng, max_attempts=5, radius=5):
    """
    Task to notify employees within a certain radius of a client's location.
    :param self: The task instance.
    :param service_id: The ID of the service request.
    :param description: The description of the service request.
    :param client_lat: The latitude of the client's location.
    :param client_lng: The longitude of the client's location.
    :param max_attempts: The maximum number of attempts to find employees within the radius.
    :param radius: The initial radius in kilometers.
    :return: None
    """
    try:
        notify_employees_by_proximity(
            service_id, description, client_lat, client_lng, max_attempts, radius
        )
    except Exception as exc:
        logger.error(f"Error en notify_employees_task: {exc}")
        raise self.retry(exc=exc, countdown=10)

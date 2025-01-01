import logging
from math import radians, sin, cos, sqrt, atan2
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from golden_clean_backend.redis_pool import redis_client

logger = logging.getLogger(__name__)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points on Earth.
    :param lat1: Latitude of the first point.
    :param lon1: Longitude of the first point.
    :param lat2: Latitude of the second point.
    :param lon2: Longitude of the second point.
    :return:
    """

    R = 6371  # Earth radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def notify_employees_by_proximity(
        service_id: int,
        description: str,
        client_lat: float,
        client_lng: float,
        max_attempts: int = 5,
        radius: int = 5
) -> None:
    """
    Notify employees within a certain radius of a client's location.
    :param service_id: The ID of the service request.
    :param description: The description of the service request.
    :param client_lat: The latitude of the client's location.
    :param client_lng: The longitude of the client's location.
    :param max_attempts: The maximum number of attempts to find employees within the radius.
    :param radius: The initial radius in kilometers.
    :return: None
    """
    channel_layer = get_channel_layer()

    try:
        # Get all available employees
        employees = redis_client.keys("employee:*")

        for attempt in range(max_attempts):
            distances = []

            for employee in employees:
                data = redis_client.hgetall(employee)
                if data.get("status") == "available" and data.get("lat") != "0.0" and data.get("lng") != "0.0":
                    distance = calculate_distance(
                        client_lat, client_lng, float(data["lat"]), float(data["lng"])
                    )
                    if distance <= radius:
                        distances.append((employee, distance))

            distances.sort(key=lambda x: x[1])

            if distances:
                for employee, _ in distances:
                    employee_id = employee.split(":")[1]

                    # Notify the employee of the service request
                    async_to_sync(channel_layer.group_send)(
                        f"employee_{employee_id}",
                        {
                            "type": "service_notification",
                            "service_id": service_id,
                            "description": description,
                        }
                    )

                    # Set the service as pending for the employee
                    redis_client.set(f"service_pending:{service_id}", employee_id, ex=20)

                return

            radius += 5
            logger.debug(f"No se encontraron empleados dentro del radio. Aumentando el radio a {radius} km.")

        logger.warning(f"No se encontraron empleados después de {max_attempts} intentos para el servicio {service_id}.")

    except Exception as e:
        logger.error(f"Error al notificar empleados para el servicio {service_id}: {e}")

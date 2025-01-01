import logging
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from golden_clean_backend.redis_pool import redis_client

logger = logging.getLogger(__name__)

class EmployeeConsumer(AsyncWebsocketConsumer):
    """
    Consumer to handle WebSocket connections for employees.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.employee_id = None

    async def connect(self):
        """
        Connect to the WebSocket.
        :return: None
        """

        # Get the user from the scope
        user = self.scope.get("user")

        # Check if the user is authenticated and has an ID
        if user.is_authenticated and user.id:
            self.employee_id = user.id
            self.group_name = f"employee_{self.employee_id}"

            # Add the employee to the employees group and their own group
            await self.channel_layer.group_add("employees", self.channel_name)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

            # Set the employee's initial location and status
            redis_client.hset(
                f"employee:{self.employee_id}",
                mapping={"lat": "0.0", "lng": "0.0", "status": "available"}
            )

        else:
            logger.warning("Unauthorized WebSocket connection attempt.")
            await self.close()

    async def disconnect(self, close_code):
        """
        Disconnect from the WebSocket.
        :param close_code: The close code.
        :return: None
        """
        if hasattr(self, "employee_id"):
            await self.channel_layer.group_discard("employees", self.channel_name)
            redis_client.delete(f"employee:{self.employee_id}")
        else:
            logger.warning("Unauthorized WebSocket disconnection attempt.")

    async def receive(self, text_data=None, bytes_data=None):
        """
        Receive data from the WebSocket.
        :param text_data: The data received.
        :param bytes_data: The bytes data received.
        :return: None
        """

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON received: {text_data}. Error: {e}")
            return

        # Handle different types of messages
        if data["type"] == "update_location":
            if self.employee_id:
                try:
                    lat = float(data["lat"])
                    lng = float(data["lng"])
                    redis_client.hset(
                        f"employee:{self.employee_id}",
                        mapping={"lat": lat, "lng": lng, "status": "available"}
                    )
                except ValueError:
                    logger.error(f"Invalid latitude or longitude received: {data}.")
            else:
                logger.warning("Invalid employee ID; cannot update location.")

        if data["type"] == "accept_service":
            service_id = data["service_id"]

            # Set the service as assigned to the employee
            redis_client.set(f"service_assigned:{service_id}", self.employee_id, ex=30)
            await self.channel_layer.group_send(
                f"employees",
                {"type": "service_assigned", "employee_id": self.employee_id, "service_id": service_id},
            )

    async def service_notification(self, event):
        """
        Send a service notification to the employee.
        :param event: The event data.
        :return: None
        """
        try:
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.error(f"Error sending notification to employee {self.employee_id}: {str(e)}")

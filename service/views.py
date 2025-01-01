from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.serializers import ServiceSerializer
from service.tasks import notify_employees_task
import logging

logger = logging.getLogger("service_request_api")

class ServiceRequestAPIView(APIView):
    """
    API view to request a service.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "CLIENT":
            logger.warning(f"Unauthorized service request by user {request.user.id}.")
            return Response({"detail": "Only clients can request services."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ServiceSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            address = serializer.validated_data["address"]
            if address.user != request.user:
                logger.error(f"Address {address.id} does not belong to user {request.user.id}.")
                return Response(
                    {"detail": "You can only use your own addresses."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            service = serializer.save()

            notify_employees_task.delay(
                service_id=service.id,
                description=service.description,
                client_lat=address.latitude,
                client_lng=address.longitude
            )

            logger.info(f"Service {service.id} created by client {request.user.id}.")
            return Response(ServiceSerializer(service).data, status=status.HTTP_201_CREATED)

        logger.error(f"Invalid service request data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

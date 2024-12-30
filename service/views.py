from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.serializers import ServiceSerializer

class ServiceRequestAPIView(APIView):
    """
    API view to request a service.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "CLIENT":
            return Response({"detail": "Only clients can request services."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ServiceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Verify that the address belongs to the authenticated client
            address = serializer.validated_data['address']
            if address.user != request.user:
                return Response(
                    {"detail": "You can only use your own addresses."}, status=status.HTTP_400_BAD_REQUEST
                )

            service = serializer.save()
            return Response(ServiceSerializer(service).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

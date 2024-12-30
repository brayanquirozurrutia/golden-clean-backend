from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from user.models import User, Region, Comuna, Address
from faker import Faker

from user.serializers import AddressSerializer


class CreateTestUsersAPIView(APIView):
    """
    APIView to create test users.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create 5 clients and 5 employees.
        :return: Response with created users.
        """
        fake = Faker()
        users_created = []

        # Helper function to create users
        def create_users(role, count):
            for _ in range(count):
                email = fake.unique.email()
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password="password123",
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    role=role,
                )
                users_created.append({"username": user.username, "role": user.role, "email": user.email})

        # Create 5 clients and 5 employees
        create_users(User.Role.CLIENT, 5)
        create_users(User.Role.EMPLOYEE, 5)

        return Response({"users_created": users_created}, status=status.HTTP_201_CREATED)


class PopulateAddressDataAPIView(APIView):
    """
    APIView to populate regions, comunas, and addresses.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Populate regions, comunas, and addresses with random data.
        :return: Response with created data counts.
        """
        fake = Faker()

        # Create regions in bulk
        region_names = {fake.unique.state() for _ in range(5)}  # Use a set to ensure uniqueness
        regions = [Region(name=name) for name in region_names]
        Region.objects.bulk_create(regions, ignore_conflicts=True)

        # Fetch all created regions
        regions = list(Region.objects.all())

        # Create comunas in bulk
        comunas = [
            Comuna(name=fake.unique.city(), region=fake.random_element(regions))
            for _ in range(len(regions) * 5)  # 5 comunas per region
        ]
        Comuna.objects.bulk_create(comunas, ignore_conflicts=True)

        # Fetch all created comunas
        comunas = list(Comuna.objects.all())

        # Fetch first 10 clients
        clients = User.objects.filter(role=User.Role.CLIENT)[:10]

        # Create addresses in bulk
        addresses = [
            Address(
                street=fake.street_name(),
                number=fake.building_number(),
                comuna=fake.random_element(comunas),
                user=client,
            )
            for client in clients
            for _ in range(2)  # 2 addresses per user
        ]
        Address.objects.bulk_create(addresses, ignore_conflicts=True)

        return Response(
            {
                "regions_created": len(region_names),
                "comunas_created": len(comunas),
                "addresses_created": len(addresses),
            },
            status=status.HTTP_201_CREATED,
        )

class AddressListAPIView(APIView):
    """
    APIView to list addresses for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter addresses associated with the authenticated user
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
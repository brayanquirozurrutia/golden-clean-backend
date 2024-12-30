from rest_framework import serializers
from user.models import Address

class AddressSerializer(serializers.ModelSerializer):
    comuna_name = serializers.CharField(source='comuna.name', read_only=True)
    region_name = serializers.CharField(source='comuna.region.name', read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'street', 'number', 'comuna_name', 'region_name']

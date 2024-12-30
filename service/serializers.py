from rest_framework import serializers
from service.models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'client', 'description', 'address', 'status']
        read_only_fields = ['id', 'status', 'client']

    def create(self, validated_data):
        # Assign the client to the service
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)
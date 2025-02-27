from rest_framework import serializers
from .models import System, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'

class SystemSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True, read_only=True)

    class Meta:
        model = System
        fields = ['id', 'name', 'owner', 'created_at', 'measurements']
        read_only_fields = ['owner']

from rest_framework import serializers
from .models import HydroponicSystem, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'


class HydroponicSystemSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True, read_only=True)

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'owner', 'name', 'description', 'created_at', 'updated_at', 'measurements']
        read_only_fields = ['owner', 'created_at', 'updated_at']

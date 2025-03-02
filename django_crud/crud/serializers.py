from rest_framework import serializers
from .models import Measurement, Sensor, HydroponicSystem


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'value', 'timestamp']
        read_only_fields = ['timestamp']


class SensorSerializer(serializers.ModelSerializer):
    recent_measurements = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = ['id', 'hydroponic_system', 'sensor_type', 'recent_measurements']

    def get_recent_measurements(self, obj):
        measurements = obj.measurements.order_by('-timestamp')[:10]
        return MeasurementSerializer(measurements, many=True).data


class HydroponicSystemSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'description', 'created_at', 'sensors']
        read_only_fields = ['created_at']


class HydroponicSystemDetailSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'description', 'created_at', 'sensors']

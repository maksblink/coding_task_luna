from rest_framework import serializers
from .models import Measurement, Sensor, HydroponicSystem
from django.utils.timezone import now


class HydroponicSystemSerializer(serializers.ModelSerializer):
    sensors = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'owner', 'name', 'description', 'created_at', 'updated_at', 'sensors']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Nazwa systemu musi mieć co najmniej 3 znaki.")
        return value


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'value', 'timestamp']
        read_only_fields = ['timestamp']

    def validate(self, data):
        sensor = data.get('sensor')
        value = data.get('value')

        if sensor and sensor.sensor_type == 'pH':
            if not (0 <= value <= 14):
                raise serializers.ValidationError("pH musi być w zakresie 0-14.")

        return data


class SensorSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ['id', 'hydroponic_system', 'sensor_type', 'measurements']

    def validate_sensor_type(self, value):
        valid_types = [choice[0] for choice in Sensor.SYSTEM_SENSORS]
        if value not in valid_types:
            raise serializers.ValidationError("Niepoprawny typ czujnika.")
        return value

    def get_recent_measurements(self, obj):
        measurements = obj.measurements.order_by('-timestamp')[:10]
        return MeasurementSerializer(measurements, many=True).data

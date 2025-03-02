from rest_framework import serializers
from .models import HydroponicSystem, Measurement, Sensor


class MeasurementSerializer(serializers.ModelSerializer):


    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'value', 'timestamp']
        read_only_fields = ['timestamp']


class SensorSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True, read_only=True)


    class Meta:
        model = Sensor
        fields = ['id', 'hydroponic_system', 'sensor_type', 'measurements']


class HydroponicSystemSerializer(serializers.ModelSerializer):
    sensors = serializers.StringRelatedField(many=True, read_only=True)


    class Meta:
        model = HydroponicSystem
        fields = ['id', 'owner', 'name', 'description', 'created_at', 'updated_at', 'sensors']
        read_only_fields = ['owner', 'created_at', 'updated_at']


class HydroponicSystemDetailSerializer(serializers.ModelSerializer):
    sensors = serializers.StringRelatedField(many=True, read_only=True)
    recent_measurements = serializers.SerializerMethodField()


    class Meta:
        model = HydroponicSystem
        fields = ['id', 'owner', 'name', 'description', 'created_at', 'updated_at', 'sensors', 'recent_measurements']


    def get_recent_measurements(self, obj):
        measurements = Measurement.objects.filter(sensor__hydroponic_system=obj).order_by('-timestamp')[:10]
        return MeasurementSerializer(measurements, many=True).data

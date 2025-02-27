from rest_framework import serializers
from .models import System, Measurement

class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = '__all__'

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'

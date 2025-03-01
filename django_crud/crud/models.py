from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class HydroponicSystem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    SYSTEM_SENSORS = [
        ('pH', 'pH Sensor'),
        ('temperature', 'Temperature Sensor'),
        ('TDS', 'Total Dissolved Solids Sensor')
    ]

    hydroponic_system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, related_name='sensors', null=True, blank=True)
    sensor_type = models.CharField(max_length=20, choices=SYSTEM_SENSORS)

    def __str__(self):
        return f"{self.sensor_type} - {self.system.name}"


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    value = models.FloatField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.sensor.sensor_type}: {self.value} ({self.timestamp})"

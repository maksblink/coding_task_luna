from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class System(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='systems')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    SYSTEM_SENSORS = [
        ('pH', 'pH Sensor'),
        ('temperature', 'Temperature Sensor'),
        ('TDS', 'Total Dissolved Solids Sensor')
    ]

    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='sensors')
    sensor_type = models.CharField(max_length=20, choices=SYSTEM_SENSORS)

    def __str__(self):
        return f"{self.sensor_type} - {self.system.name}"


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    value = models.FloatField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.sensor.sensor_type}: {self.value} ({self.timestamp})"

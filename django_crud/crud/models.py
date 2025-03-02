from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver


class HydroponicSystem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hydroponic_systems")

    def __str__(self):
        return f"name = {self.name}, owner = ({self.owner.username})"


def get_default_system():
    return HydroponicSystem.objects.first().id


class Sensor(models.Model):
    SYSTEM_SENSORS = [
        ('pH', 'pH Sensor'),
        ('temperature', 'Temperature Sensor'),
        ('TDS', 'Total Dissolved Solids Sensor')
    ]

    hydroponic_system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, related_name='sensors', default=get_default_system)
    sensor_type = models.CharField(max_length=20, choices=SYSTEM_SENSORS)

    def __str__(self):
        return f"sensor_type = {self.sensor_type}, hydroponic_system = {self.hydroponic_system.name}"


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    value = models.FloatField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"sensor_type = {self.sensor.sensor_type}, hydroponic_system = {self.sensor.hydroponic_system.name}, value = {self.value}, timestamp = {self.timestamp}"


@receiver(post_save, sender=HydroponicSystem)
def create_sensors(sender, instance, created, **kwargs):
    if created:
        for sensor_type, _ in Sensor.SYSTEM_SENSORS:
            Sensor.objects.create(hydroponic_system=instance, sensor_type=sensor_type)

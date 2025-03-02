import pytest
from django.contrib.auth.models import User
from crud.models import HydroponicSystem, Sensor, Measurement
from django.utils.timezone import now


@pytest.mark.django_db
def test_create_hydroponic_system():
    user = User.objects.create_user(username="testuser", password="dupa12345")
    hydroponic_system = HydroponicSystem.objects.create(name="Test System", description="duuuuupa", owner=user)

    assert hydroponic_system.name == "Test System"
    assert hydroponic_system.owner == user
    assert hydroponic_system.sensors.count() == 3


@pytest.mark.django_db
def test_create_measurement():
    user = User.objects.create_user(username="testuser", password="dupa12345")
    system = HydroponicSystem.objects.create(name="Test System", description="duuuuupa", owner=user)
    sensor = system.sensors.first()

    measurement = Measurement.objects.create(sensor=sensor, value=7.5, timestamp=now())

    assert measurement.sensor == sensor
    assert measurement.value == 7.5

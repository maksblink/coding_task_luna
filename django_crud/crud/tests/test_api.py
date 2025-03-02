import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from crud.models import HydroponicSystem, Sensor, Measurement


@pytest.mark.django_db
def test_api_create_hydroponic_system():
    user = User.objects.create_user(username="testuser", password="dupa1235")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/api/hydroponic_system/", {"owner": user.id, "name": "API System", "description": "duuuuupa API"})
    assert response.status_code == 201
    assert HydroponicSystem.objects.count() == 1


@pytest.mark.django_db
def test_api_get_systems():
    user = User.objects.create_user(username="testuser", password="dupa1235")
    HydroponicSystem.objects.create(name="System 1", owner=user)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/hydroponic_system/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_api_create_measurement():
    user = User.objects.create_user(username="testuser", password="dupa1235")
    system = HydroponicSystem.objects.create(name="System 1", owner=user)
    sensor = system.sensors.first()

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/api/measurements/", {"sensor": sensor.id, "value": 7.2})
    assert response.status_code == 201
    assert Measurement.objects.count() == 1


@pytest.mark.django_db
def test_api_invalid_pH_value():
    user = User.objects.create_user(username="testuser", password="dupa12345")
    system = HydroponicSystem.objects.create(name="System 1", owner=user)
    sensor = system.sensors.first()

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/api/measurements/", {"sensor": sensor.id, "value": 15})
    assert response.status_code == 400
    assert "pH musi być w zakresie 0-14." in response.json()["non_field_errors"]

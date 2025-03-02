import pytest
from crud.forms import MeasurementForm
from crud.models import Sensor, HydroponicSystem
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_valid_measurement_form():
    user = User.objects.create_user(username="testuser", password="dupa12345")
    hydroponic_system = HydroponicSystem.objects.create(name="Test System", description="duuuuupa", owner=user)

    sensor = Sensor.objects.first()
    form_data = {"sensor": sensor.id, "value": 7.2}
    form = MeasurementForm(data=form_data)

    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_measurement_form():
    form_data = {"value": "nie liczba"}
    form = MeasurementForm(data=form_data)

    assert not form.is_valid()

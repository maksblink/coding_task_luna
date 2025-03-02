import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from crud.models import HydroponicSystem
from django.test import Client


@pytest.mark.django_db
def test_home_page():
    client = Client()

    user = User.objects.create_user(username="testuser", password="dupa12345")
    client.login(username="testuser", password="dupa12345")

    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_authenticated_home_page():
    user = User.objects.create_user(username="testuser", password="dupa12345")
    client = Client()
    client.login(username="testuser", password="dupa12345")

    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_hydroponic_system():
    user = User.objects.create_user(username="testuser", password="dupa12345")
    client = Client()
    client.login(username="testuser", password="dupa12345")

    response = client.post(reverse('add_hydroponic_system'), {"name": "Test System", "description": "duuuuupa"})
    assert response.status_code == 302
    assert HydroponicSystem.objects.count() == 1

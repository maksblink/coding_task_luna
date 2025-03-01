from rest_framework import viewsets, permissions
from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.systems.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Measurement.objects.filter(system__owner=self.request.user)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Konto dla {username} zostało utworzone! Możesz się teraz zalogować.")
            return redirect("login")  # Przekierowanie do logowania
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def home(request):
    systems = HydroponicSystem.objects.filter(owner=request.user) if request.user.is_authenticated else []
    return render(request, 'home.html', {'systems': systems})
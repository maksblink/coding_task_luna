from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import System, Measurement
from .serializers import SystemSerializer, MeasurementSerializer
from django.shortcuts import render
from .models import System
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages


class SystemViewSet(viewsets.ModelViewSet):
    serializer_class = SystemSerializer
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


def system_list(request):
    systems = System.objects.all()
    return render(request, 'systems/list.html', {'systems': systems})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Konto dla {username} zostało utworzone! Możesz się teraz zalogować.")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})
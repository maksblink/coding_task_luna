from rest_framework import viewsets, permissions, status, generics, filters
from .serializers import HydroponicSystemSerializer, MeasurementSerializer, SensorSerializer, HydroponicSystemDetailSerializer
from django.contrib import messages
from .forms import UserRegisterForm, HydroponicSystemForm
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from .models import Sensor, Measurement, HydroponicSystem
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import StandardResultsSetPagination
from .filters import MeasurementFilter


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Sensor.objects.filter(hydroponic_system__owner=self.request.user)

    def perform_create(self, serializer):
        hydroponic_system = serializer.validated_data.get('hydroponic_system')
        if hydroponic_system.owner != self.request.user:
            raise serializers.ValidationError("Nie masz dostępu do tego systemu.")
        serializer.save()


class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Measurement.objects.filter(sensor__hydroponic_system__owner=self.request.user)

    def perform_create(self, serializer):
        sensor = serializer.validated_data.get('sensor')

        if sensor.hydroponic_system.owner != self.request.user:
            raise serializers.ValidationError("Nie masz dostępu do tego sensora.")

        serializer.save()


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
    hydroponic_systems_form = HydroponicSystemForm()

    hydroponic_systems = None
    if request.user.is_authenticated:
        if request.method == "POST":
            hydroponic_systems_form = HydroponicSystemForm(request.POST)
            if hydroponic_systems_form.is_valid():
                hydroponic_system = hydroponic_systems_form.save(commit=False)
                hydroponic_system.owner = request.user
                hydroponic_system.save()
                return redirect('home')

        hydroponic_systems = HydroponicSystem.objects.filter(owner=request.user)

    return render(request, "home.html", {
        "hydroponic_systems_form": hydroponic_systems_form,
        "hydroponic_systems": hydroponic_systems
    })


def update_hydroponic_system(request, hydroponic_system_id):
    hydroponic_system = get_object_or_404(HydroponicSystem, id=hydroponic_system_id, owner=request.user)
    if request.method == "POST":
        hydroponic_systems_form = HydroponicSystemForm(request.POST, instance=hydroponic_system)
        if hydroponic_systems_form.is_valid():
            hydroponic_systems_form.save()
            return redirect('home')
    else:
        hydroponic_systems_form = HydroponicSystemForm(instance=hydroponic_system)

    return render(request, "update_hydroponic_system.html", {"hydroponic_systems_form": hydroponic_systems_form})


def delete_hydroponic_system(request, hydroponic_system_id):
    hydroponic_system = get_object_or_404(HydroponicSystem, id=hydroponic_system_id, owner=request.user)
    hydroponic_system.delete()
    return redirect('home')


class HydroponicSystemListView(generics.ListAPIView):
    serializer_class = HydroponicSystemSerializer

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)


class HydroponicSystemDetailView(generics.RetrieveAPIView):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemDetailSerializer


class MeasurementListView(generics.ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MeasurementFilter
    ordering_fields = ['timestamp', 'value']

from rest_framework import viewsets, permissions, generics, filters, serializers
from .serializers import HydroponicSystemSerializer, SensorSerializer, MeasurementSerializer
from django.contrib import messages
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import StandardResultsSetPagination
from .filters import MeasurementFilter
from .forms import HydroponicSystemForm, MeasurementForm, UserRegisterForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import HydroponicSystem, Measurement, Sensor
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return HydroponicSystem.objects.all()
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.owner != self.request.user:
            raise serializers.ValidationError({"error": "Nie masz uprawnień do edycji tego systemu."})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise serializers.ValidationError({"error": "Nie masz uprawnień do usunięcia tego systemu."})
        instance.delete()


class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Sensor.objects.filter(hydroponic_system__owner=self.request.user)

    def perform_create(self, serializer):
        hydroponic_system = serializer.validated_data['hydroponic_system']

        if hydroponic_system.owner != self.request.user:
            raise serializers.ValidationError({"error": "Nie masz dostępu do tego systemu."})

        serializer.save()


class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Measurement.objects.filter(sensor__hydroponic_system__owner=self.request.user)

    def perform_create(self, serializer):
        sensor = serializer.validated_data.get('sensor')

        if sensor.hydroponic_system.owner != self.request.user:
            raise serializers.ValidationError({"error": "Nie masz dostępu do tego sensora."})

        serializer.save()


@login_required
def home(request):
    hydroponic_systems = HydroponicSystem.objects.filter(owner=request.user)
    return render(request, "home.html", {"hydroponic_systems": hydroponic_systems})


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


class MeasurementListView(generics.ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MeasurementFilter
    ordering_fields = ['timestamp', 'value']


@login_required
def add_hydroponic_system(request):
    if request.method == "POST":
        hydroponic_systems_form = HydroponicSystemForm(request.POST)
        if hydroponic_systems_form.is_valid():
            hydroponic_system = hydroponic_systems_form.save(commit=False)
            hydroponic_system.owner = request.user
            hydroponic_system.save()
            return redirect('home')
    else:
        hydroponic_systems_form = HydroponicSystemForm()

    return render(request, "add_hydroponic_system.html", {"hydroponic_systems_form": hydroponic_systems_form})


def hydroponic_system_detail(request, hydroponic_system_id):
    hydroponic_system = get_object_or_404(HydroponicSystem, id=hydroponic_system_id, owner=request.user)
    measurements = Measurement.objects.filter(sensor__hydroponic_system=hydroponic_system)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        if start_date:
            start_date = parse_datetime(start_date)
            if start_date:
                measurements = measurements.filter(timestamp__gte=start_date)

        if end_date:
            end_date = parse_datetime(end_date)
            if end_date:
                measurements = measurements.filter(timestamp__lte=end_date)
    except ValidationError:
        messages.error(request, "Nieprawidłowy format daty.")

    try:
        min_value = float(request.GET.get('min_value')) if request.GET.get('min_value') else None
        max_value = float(request.GET.get('max_value')) if request.GET.get('max_value') else None

        if min_value is not None:
            measurements = measurements.filter(value__gte=min_value)
        if max_value is not None:
            measurements = measurements.filter(value__lte=max_value)
    except ValueError:
        messages.error(request, "Nieprawidłowa wartość dla filtra wartości.")

    sort_by = request.GET.get('sort_by', '-timestamp')
    if sort_by in ['value', '-value', 'timestamp', '-timestamp']:
        measurements = measurements.order_by(sort_by)

    paginator = Paginator(measurements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recent_measurements = measurements.order_by('-timestamp')[:10]

    return render(request, "hydroponic_system_detail.html", {
        "hydroponic_system": hydroponic_system,
        "sensors": hydroponic_system.sensors.all(),
        "measurements": page_obj,
        "recent_measurements": recent_measurements,
        "start_date": request.GET.get('start_date', ''),
        "end_date": request.GET.get('end_date', ''),
        "min_value": request.GET.get('min_value', ''),
        "max_value": request.GET.get('max_value', ''),
        "sort_by": request.GET.get('sort_by', '-timestamp'),
    })


@login_required
def add_measurement(request, hydroponic_system_id):
    hydroponic_system = get_object_or_404(HydroponicSystem, id=hydroponic_system_id, owner=request.user)
    sensors = hydroponic_system.sensors.all()

    if request.method == "POST":
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)

            if measurement.sensor.hydroponic_system != hydroponic_system:
                form.add_error('sensor', "Nie masz dostępu do tego czujnika.")
            else:
                measurement.save()
                messages.success(request, "Pomiar został dodany.")
                return redirect('hydroponic_system_detail', hydroponic_system_id=hydroponic_system.id)
    else:
        form = MeasurementForm()

    return render(request, "add_measurement.html", {
        "form": form,
        "hydroponic_system": hydroponic_system,
        "sensors": sensors
    })


@api_view(["GET", "POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def register(request):
    if request.content_type == "application/json":
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Nazwa użytkownika i hasło są wymagane."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Użytkownik już istnieje."}, status=400)

        user = User(username=username)
        user.set_password(password)
        user.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "message": "Rejestracja zakończona sukcesem"}, status=201)

    else:
        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("home")
        else:
            form = UserRegisterForm()

        return render(request, "users/register.html", {"form": form})

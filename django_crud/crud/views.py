from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import System, Measurement
from .serializers import SystemSerializer, MeasurementSerializer

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

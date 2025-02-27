from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crud.views import SystemViewSet, MeasurementViewSet

router = DefaultRouter()
router.register(r'systems', SystemViewSet)
router.register(r'measurements', MeasurementViewSet)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('crud/', include(router.urls)),
]

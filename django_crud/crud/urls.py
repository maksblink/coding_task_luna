from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HydroponicSystemViewSet, MeasurementViewSet, SensorViewSet, home, update_hydroponic_system, delete_hydroponic_system, HydroponicSystemListView, HydroponicSystemDetailView, MeasurementListView
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'hydroponic_system', HydroponicSystemViewSet, basename='hydroponic_system')
router.register(r'measurements', MeasurementViewSet, basename='measurement')
router.register(r'sensors', SensorViewSet, basename='sensor')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('', home, name='home'),
    path("systems/update/<int:hydroponic_system_id>/", update_hydroponic_system, name="update_hydroponic_system"),
    path("systems/delete/<int:hydroponic_system_id>/", delete_hydroponic_system, name="delete_hydroponic_system"),
    path('systems/', HydroponicSystemListView.as_view(), name='system-list'),
    path('systems/<int:pk>/', HydroponicSystemDetailView.as_view(), name='system-detail'),
    path('measurements/', MeasurementListView.as_view(), name='measurement-list'),
]

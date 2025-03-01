from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HydroponicSystemViewSet, MeasurementViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import home

router = DefaultRouter()
router.register(r'hydroponic_system', HydroponicSystemViewSet, basename='hydroponic_system')
router.register(r'measurements', MeasurementViewSet, basename='measurement')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    # path('systems/', system_list, name='system_list'),
    path('', home, name='home'),
]

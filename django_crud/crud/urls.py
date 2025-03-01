from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemViewSet, MeasurementViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import system_list, home

router = DefaultRouter()
router.register(r'systems', SystemViewSet, basename='system')
router.register(r'measurements', MeasurementViewSet, basename='measurement')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('systems/', system_list, name='system_list'),
    path('', home, name='home'),
]

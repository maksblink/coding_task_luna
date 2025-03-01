from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from crud.views import register


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crud.urls')),
    path("users/login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("users/logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("users/register/", register, name="register"),
]

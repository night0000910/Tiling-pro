from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import signupview, loginview, logoutview, tilingview, displayview


urlpatterns = [
    path("signup/", signupview, name="signup"),
    path("login/", loginview, name="login"),
    path("logout/", logoutview, name="logout"),
    path("tiling/<str:type>/", tilingview, name="tiling"),
    path("display/<str:type>/", displayview, name="display"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
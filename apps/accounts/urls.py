from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views.auth import (
    LoginView,
    LogoutView,
    MeView,
)


urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
]
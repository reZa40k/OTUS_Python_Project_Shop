from django.urls import path
from .views import (
    RegistrationView,
    CustomLogoutView,
    CustomLoginView,
    CustomProfileView,
)

app_name = "users"

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", CustomProfileView.as_view(), name="profile"),
]

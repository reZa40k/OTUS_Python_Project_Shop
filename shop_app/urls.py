from django.urls import path
from .views import index, about

app_name = "shop_app"

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
]

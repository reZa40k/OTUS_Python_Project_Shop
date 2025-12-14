from django.urls import path
from .views import create_order, order_list

app_name = "orders_app"
urlpatterns = [
    path("create/", create_order, name="create_order"),
    path("list/", order_list, name="order_list"),
]

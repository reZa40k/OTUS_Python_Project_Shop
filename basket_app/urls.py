from django.urls import path
from .views import detail_basket, add_basket, del_basket, edit_basket


app_name = "basket_app"

urlpatterns = [
    path("", detail_basket, name="detail_basket"),
    path("add/<int:product_pk>/", add_basket, name="add_basket"),
    path("del/<int:product_pk>/", del_basket, name="del_basket"),
    path("edit/<int:product_pk>/", edit_basket, name="edit_basket"),
]

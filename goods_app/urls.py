from django.urls import path
from .views import (
    catalog,
    product,
    ProductCreateView,
    ProductUpdateView,
    ProductListView,
    ProductDeleteView,
)

app_name = "catalog"

urlpatterns = [
    path("", catalog, name="index"),
    path("search/", catalog, name="search"),
    path("<slug:category_slug>/", catalog, name="index"),
    path("product/<slug:product_slug>/", product, name="product"),
    path("admin/products/", ProductListView.as_view(), name="product_list"),
    path("admin/products/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "admin/products/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "admin/products/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
]

from django.contrib import admin

from goods_app.models import Categories, Products


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """
    Автозаполнение slug
    """

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    """
    Регистрация товаров в админке
    """

    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "counts", "price"]
    search_fields = ["name", "description"]

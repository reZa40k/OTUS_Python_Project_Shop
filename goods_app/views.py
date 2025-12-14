from django.shortcuts import render
from django.db.models import Q
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from goods_app.models import Products


def catalog(request, category_slug=None):
    """
    Данная функция выводит перечень товров по категориям
    -все товары
    -товары по категориям
    -найденные товары через поиск
    """
    query = request.GET.get("query", None)

    if category_slug is None or category_slug == "all":
        if query:
            goods = Products.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(slug__icontains=query)
            )
        else:
            goods = Products.objects.all()
    elif query:
        goods = Products.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(slug__icontains=query)
        )
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    context = {
        "title": "Каталог товаров",
        "goods": goods,
        "query": query,
    }
    return render(request, "goods_app/catalog.html", context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    context = {
        "product": product,
        "title": product.name,
    }

    return render(request, "goods_app/product.html", context)


# ========= CBV. CRUD для обновления товаров =========


class StaffRequiredMixin(UserPassesTestMixin):
    """
    Доступ только для персонала/суперюзеров
    """

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class ProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """
    Просмотр товаров только для персонала
    """

    model = Products
    template_name = "goods_app/product_manage.html"
    context_object_name = "products"


class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """
    Добавление товара только для персонала
    """

    model = Products
    fields = ("name", "slug", "description", "image", "price", "counts", "category")
    template_name = "goods_app/product_edit.html"
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """
    Изменение товара только для персонала
    """

    model = Products
    fields = ("name", "slug", "description", "image", "price", "counts", "category")
    template_name = "goods_app/product_edit.html"
    success_url = reverse_lazy("catalog:product_list")


class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """
    Удаление товара только для персонала
    """

    model = Products
    template_name = "goods_app/product_del.html"
    success_url = reverse_lazy("catalog:index")

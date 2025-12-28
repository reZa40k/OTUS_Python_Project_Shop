from django.contrib import messages
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
from goods_app.tasks import info_add_poduct, info_edit_poduct, info_del_poduct


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
    test_product = Products.objects.get(slug=product_slug)
    context = {
        "product": test_product,
        "title": test_product.name,
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

    def form_valid(self, form):
        """
        Вывод сообщения в консоль
        """
        response = super().form_valid(form)
        messages.success(self.request, "Товар добавлен успешно")
        info_add_poduct.delay(self.object.name)
        return response


class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """
    Изменение товара только для персонала
    """

    model = Products
    fields = ("name", "slug", "description", "image", "price", "counts", "category")
    template_name = "goods_app/product_edit.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        """
        Вывод сообщения в консоль
        """
        response = super().form_valid(form)
        messages.success(self.request, "Товар изменен успешно")
        info_edit_poduct.delay(self.object.name)
        return response


class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """
    Удаление товара только для персонала
    """

    model = Products
    template_name = "goods_app/product_del.html"
    success_url = reverse_lazy("catalog:index")

    def post(self, request, *args, **kwargs):
        """
        Вывод сообщения в консоль
        """
        self.object = self.get_object()
        product_name = self.object.name
        info_del_poduct.delay(product_name)
        response = super().post(request, *args, **kwargs)
        messages.success(request, "Товар удален успешно")
        return response

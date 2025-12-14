from django.shortcuts import redirect, render
from django.contrib import messages

from basket_app.models import Basket
from goods_app.models import Products


def add_basket(request, product_pk):
    """
    Добавляет товар в корзину для авторизированных пользователей
    """
    product = Products.objects.get(pk=product_pk)

    if request.user.is_authenticated:
        basket = Basket.objects.filter(CustomUser=request.user, product=product)

        if basket.exists():
            basket = basket.first()
            if basket:
                basket.counts += 1
                basket.save()
                messages.success(request, f"{product.name} добавлен в корзину!")
        else:
            Basket.objects.create(CustomUser=request.user, product=product, counts=1)
            messages.success(request, f"{product.name} добавлен в корзину!")
    else:
        messages.warning(request, "Войдите в аккаунт для добавления в корзину")
    return redirect(request.META.get("HTTP_REFERER", "/"))


def del_basket(request, product_pk):
    """
    Удаляет товар из корзины для авторизованных пользователей
    """
    if request.user.is_authenticated:
        Basket.objects.filter(CustomUser=request.user, product_id=product_pk).delete()
    else:
        basket = request.session.get("basket", {})
        key = str(product_pk)
        basket.pop(key, None)
        request.session["basket"] = basket
        request.session.modified = True

    return redirect("basket:detail_basket")


def edit_basket(request, product_pk):
    """
    Позволяет изменять товары в корзине (количество)
    """
    if request.method == "POST":
        counts = int(request.POST.get("counts", 1))

        if request.user.is_authenticated:
            basket = Basket.objects.filter(
                CustomUser=request.user, product_id=product_pk
            ).first()

            if basket:
                if counts > 0:
                    basket.counts = counts
                    basket.save()
                else:
                    basket.delete()
    else:
        counts = request.POST.get("counts", 1)

    return redirect("basket:detail_basket")


def detail_basket(request):
    """
    Выводит информацию о корзине пользователя
    """
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(CustomUser=request.user).select_related(
            "product"
        )
        total_price = sum(item.price_order() for item in baskets) if baskets else 0
    else:
        baskets = []
        total_price = 0

    context = {"baskets": baskets, "total_price": total_price, "title": "Корзина"}
    return render(request, "basket_app/basket.html", context)

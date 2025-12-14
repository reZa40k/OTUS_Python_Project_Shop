from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from .models import Order, OrderItem
from basket_app.models import Basket


def create_order(request):
    """
    Оформление заказа из корзины
    """
    if not request.user.is_authenticated:
        messages.warning(request, "Войдите в аккаунт")
        return redirect("users:login")

    baskets = Basket.objects.filter(CustomUser=request.user).select_related("product")
    if not baskets.exists():
        messages.warning(request, "Корзина пуста!")
        return redirect("basket:detail_basket")

    total_price = sum(basket.price_order() for basket in baskets)

    if request.user.balance < total_price:
        messages.error(
            request,
            f"Недостаточно средств! Стоимость покупки: {total_price} руб., баланс: {request.user.balance} руб.",
        )
        return redirect("basket:detail_basket")

    with transaction.atomic():
        order = Order.objects.create(user=request.user, total_price=total_price)

        for basket in baskets:
            OrderItem.objects.create(
                order=order,
                product=basket.product,
                quantity=basket.counts,
                price=basket.product.price,
            )
            basket.delete()

        request.user.balance -= total_price
        request.user.save()
        order.status = "paid"
        order.paid_at = timezone.now()
        order.save()

    messages.success(
        request, f"Заказ #{order.pk} успешно оформлен! Сумма: {total_price} ₽"
    )
    return redirect("orders:order_list")


def order_success(request, order_id):
    """
    Подтвеждение заказа
    """
    messages.success(request, f"Заказ #{order_id} успешно оформлен!")
    return redirect("users:profile")


@login_required
def order_list(request):
    """
    Список заказов пользователя
    """
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )
    context = {"orders": orders, "title": "Заказы"}
    return render(request, "orders_app/orders.html", context)

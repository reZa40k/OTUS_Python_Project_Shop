from django.db import models
from users_app.models import CustomUser
from goods_app.models import Products


class Order(models.Model):
    """
    Модель заказов поьзователя
    """

    STATUS_CHOICES = [("new", "Новый"), ("paid", "Оплачен"), ("completed", "Выполнен")]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания заказа"
    )
    paid_at = models.DateTimeField(null=True, blank=True)

    def total_products(self):
        return sum(item.quantity for item in self.items.all())

    def total_sum(self):
        return sum(item.total_price() for item in self.items.all())

    total_products.short_description = "Количество"
    total_sum.short_description = "Сумма"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.pk} - {self.user.username}"


class OrderItem(models.Model):
    """
    Таблица заказ-товар
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость"
    )

    class Meta:
        verbose_name = "Купленные товары"
        verbose_name_plural = "Купленные товары"

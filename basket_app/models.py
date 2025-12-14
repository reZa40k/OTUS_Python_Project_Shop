from django.db import models

from goods_app.models import Products


class BasketQueryset(models.QuerySet):
    """
    Подсчитываем общую стоимость корзины
    """

    def total_price(self):
        return sum(basket.price_order() for basket in self)

    def total_counts(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Basket(models.Model):
    """
    Корзина для пользователя по 1 виду товаров
    """

    CustomUser = models.ForeignKey("users_app.CustomUser", on_delete=models.CASCADE)
    product = models.ForeignKey(
        to=Products, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    counts = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")

    class Meta:
        db_table = "basket"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    objects = BasketQueryset.as_manager()

    def price_order(self):
        """
        Вычесление стоимости по 1 типу товаров
        """
        return round(self.product.price * self.counts, 2)

    def __str__(self):
        """
        Для корректного отображения в панели администратора
        """
        return f"{self.CustomUser.email} - {self.product.name} x{self.counts}"

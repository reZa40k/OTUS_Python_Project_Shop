from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Таблица товаров внетри заказа
    """

    model = OrderItem
    extra = 0
    readonly_fields = ("price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Регистрация заказов в админке с позициями
    """

    list_display = ("id", "user", "created_at", "get_total_price", "total_products")
    list_filter = ("created_at", "user")
    search_fields = ("id", "user__username")
    inlines = [OrderItemInline]

    def get_total_price(self, obj):
        return f"{obj.total_price} руб."

    get_total_price.short_description = "Сумма"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Админка позиций заказов
    """

    list_display = "order", "product", "price", "quantity"
    search_fields = "order", "product", "name"

    def get_price(self, obj):
        return f"{obj.price} ₽"

    get_price.short_description = "Цена"

    def get_total(self, obj):
        return f"{obj.price * obj.quantity} ₽"

    get_total.short_description = "Итого"

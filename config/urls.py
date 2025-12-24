from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop_app.urls', namespace='shop_app')),
    path('catalog/', include('goods_app.urls', namespace='catalog')),
    path('user/', include('users_app.urls', namespace='users')),
    path('basket/', include('basket_app.urls', namespace='basket')),
    path('orders/', include('orders_app.urls', namespace='orders')),
]


# Импорт изображений
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
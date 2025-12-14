from django.shortcuts import render


def index(request):
    """
    Главная страница
    """
    context = {
        "title": "М.Аудио",
        "content": "Интернет магазин М.Аудио",
        "slogan": "Технологии на вашей волне!",
    }
    return render(request, "shop_app/index.html", context)


def about(request):
    """
    Страница Контактов
    """
    context = {
        "title": "Контакты",
        "top": "М.Аудио — онлайн-магазин электроники с быстрой доставкой, проверенными брендами и поддержкой 24/7.",
        "contacts": "Контакты:",
    }
    return render(request, "shop_app/about.html", context)

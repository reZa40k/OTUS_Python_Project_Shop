from django.views.generic import FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

from .forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    CustomUser,
    CustomUserChangeForm,
)


class RegistrationView(FormView):
    """
    Регистрация нового пользователя и вход в личный кабинет
    """

    template_name = "users_app/registration.html"
    form_class = CustomUserCreationForm
    success_url = "/user/profile/"
    title = "Регистрация"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context

    def get(self, request, *args, **kwargs):
        messages.info(self.request, "Заполните форму для регистрации")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(self.request, "Регистрация успешна!")
            user = form.save()
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Исправьте ошибки в форме")
            return super().form_invalid(form)


class CustomLoginView(LoginView):
    """
    Авторизация пользователя
    """

    template_name = "users_app/login.html"
    authentication_form = CustomAuthenticationForm
    title = "Вход"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class CustomLogoutView(LogoutView):
    """
    Выход пользователя
    """

    next_page = "/user/login/"

    def get(self, request, *args, **kwargs):
        print("LOGOUT GET request")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("LOGOUT POST request")
        return super().post(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class CustomProfileView(UpdateView):
    """
    Класс для редактирования профиля пользователя
    """

    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users_app/profile.html"
    success_url = "/user/profile/"
    title = "Профиль"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Форма создания нового пользователя при регистрации
    """

    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Имя",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите имя"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Фамилия",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите фамилию"}
        ),
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите Email"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.balance = 100000
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже занят")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    """
    Форма дла авторизации и валидации вводимых данных
    """

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите Email"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )

    def clean(self):
        email = self.cleaned_data.get("username").lower()
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Введите правильные email и пароль. Оба поля чувствительны к регистру."
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class CustomUserChangeForm(forms.ModelForm):
    """
    Форма редактирования профиля
    """

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "username", "email", "avatar", "balance")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "balance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "placeholder": "0.00",
                }
            ),
        }

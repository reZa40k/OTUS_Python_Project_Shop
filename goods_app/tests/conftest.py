import os
import django
from pytest import fixture

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

@fixture
def client():
    '''
    Имитация подключения
    '''
    from django.test import Client
    return Client()

@fixture
def staff_user(db):
    '''
    Фикстура создания CustomUser с правами персонала
    '''
    from users_app.models import CustomUser
    
    user = CustomUser.objects.create_user(
        email='stafftest@test.ru', 
        password='testpass123'
    )
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user

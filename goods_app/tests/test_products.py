import pytest
from django.urls import reverse
from goods_app.models import Products, Categories

@pytest.mark.django_db
class TestProductCRUD:
    '''
    Тесты по проверке модели Products
    '''

    @pytest.fixture
    def test_category(self):
        '''
        Добавляет тестовую категорию
        '''
        return Categories.objects.create(name="Тест", slug="test-cat")

    @pytest.fixture
    def test_product(self, test_category):
        '''
        Тестовый товар в созданной категории
        '''
        return Products.objects.create(
            name='Тестовый товар',
            slug='test-product',
            description='Тест',
            price='999.99',
            counts=5,
            category=test_category
        )

    def test_create_product(self, client, staff_user, test_category):
        '''
        Тест по добавлению товара персоналом
        '''
        client.login(username='stafftest@test.ru', password='testpass123')
        url = reverse('catalog:product_create')
        data = {
            'name': 'Новый товар',
            'slug': 'new-product',
            'description': 'Новое описание',
            'price': '1500.00',
            'counts': '10',
            'category': test_category.pk
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert Products.objects.filter(name='Новый товар').exists()

    def test_update_product(self, client, staff_user, test_product):
        '''
        Тест изменения товара персоналом
        '''
        client.login(username='stafftest@test.ru', password='testpass123')
        url = reverse('catalog:product_update', args=[test_product.pk])
        data = {
        'name': 'Обновленный товар',
        'slug': f'updated-product-{test_product.pk}',
        'description': 'Обновленное описание',
        'price': '2000.00',
        'counts': '20',
        'category': str(test_product.category.pk),
        'image': ''
    }
        response = client.post(url, data)        
        assert response.status_code == 302
        test_product.refresh_from_db()
        assert test_product.name == 'Обновленный товар'
        assert test_product.price == 2000.00
        assert test_product.counts == 20

    def test_delete_product(self, client, staff_user, test_product):
        '''
        Тест удаления товара персоналом
        '''
        client.login(username='stafftest@test.ru', password='testpass123')
        url = reverse('catalog:product_delete', args=[test_product.pk])
        response = client.post(url)
        assert response.status_code == 302
        assert not Products.objects.filter(pk=test_product.pk).exists()

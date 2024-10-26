import pytest
from rest_framework.test import APIClient

from apps.common.utils.text import generate_text
from apps.common.utils.uri import uri_text
from apps.product.selectors.product_selector import product_model
from apps.product.service.product_service import ProductService


class TestProductService:
    """Класс тестирования функций из пакета service"""

    _product_service = ProductService()

    @pytest.mark.parametrize(
        "fields, expectation",
        [
            ({'category': '', 'name': '', 'description': '', 'count': '', 'price': ''}, True),
            ({}, False),
            ({'cat': '', 'name': '', 'description': '', 'count': '', 'price': ''}, False),
            ({'category': '', 'nm': '', 'description': '', 'count': '', 'price': ''}, False),
            ({'category': '', 'name': '', 'descr': '', 'count': '', 'price': ''}, False),
            ({'category': '', 'name': '', 'description': '', 'cnt': '', 'price': ''}, False),
            ({'category': '', 'name': '', 'description': '', 'count': '', 'prc': ''}, False)
        ]
    )
    def test_validate_product(self, fields, expectation):
        """Тестирование функции валидациии полей модели"""
        assert self._product_service.validate_product(fields) == expectation


class TestProductAPI:
    """Класс тестирования эндпоинтов для работы с товарами"""

    api_client = APIClient()
    base_url = 'http://localhost:8000/backend/api/v1/product/product/'
    test_product_id = None

    @pytest.fixture
    def setup_test_data(self):
        """Добавление тестовых данных"""
        test_product = product_model(
            category='electronic',
            name='Товар',
            description='Описание',
            count=150,
            price=17500.50
        )
        test_product.save()
        self.test_product_id = test_product.id

    @pytest.mark.django_db
    def test_get(self, setup_test_data):
        """Проверка на получение товаров"""
        response = self.api_client.get(
            self.base_url,
            format="json"
        )
        assert response.status_code == 200
        assert len(response.data['success']) == 1

    @pytest.mark.django_db
    def test_get_filter(self, setup_test_data):
        """Проверка на получение товаров с фильтрами"""
        correct_name_response = self.api_client.get(
            f'{self.base_url}?name={uri_text("Тов")}',
            format="json"
        )
        assert len(correct_name_response.data['success']) == 1
        incorrect_name_response = self.api_client.get(
            f'{self.base_url}?name={uri_text("HONOR")}',
            format="json"
        )
        assert len(incorrect_name_response.data['success']) == 0

    @pytest.mark.django_db
    def test_create(self):
        """Проверка добавления товара"""
        assert product_model.objects.count() == 0
        create_response = self.api_client.post(
            self.base_url,
            data={
                'category': 'food',
                'name': generate_text(1, 299),
                'description': generate_text(1, 4999),
                'count': 150,
                'price': 17500.50
            },
            format='json'
        )
        assert create_response.status_code == 201
        assert product_model.objects.count() == 1

    @pytest.mark.django_db
    def test_update(self, setup_test_data):
        """Проверка обновления информации по товару"""
        update_response = self.api_client.patch(
            f'{self.base_url}{self.test_product_id}/',
            data={
                'category': 'food',
                'name': 'Молоко',
                'description': 'Один литр молока в картонной коробке',
                'count': 150,
                'price': 17500.50
            },
            format='json'
        )
        assert update_response.status_code == 200
        assert product_model.objects.get(id=self.test_product_id).name == 'Молоко'

    @pytest.mark.django_db
    def test_delete(self, setup_test_data):
        """Проверка удаления товара"""
        delete_response = self.api_client.delete(
            f'{self.base_url}{self.test_product_id}/'
        )
        assert delete_response.status_code == 200
        assert product_model.objects.count() == 0

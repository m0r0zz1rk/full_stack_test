import pytest
from faker import Faker

from apps.product.service.product_service import ProductService

faker = Faker('ru-RU')


def generate_text(min_length: int, max_length: int) -> str:
    """
    Генерация текста
    :param min_length: минимальная длина, кол-во символов
    :param max_length: максимальная длина, кол-во символов
    :return: строка
    """
    text = faker.text(max_nb_chars=max_length)
    if min_length != 0:
        while len(text) < min_length:
            text += faker.text(max_nb_chars=max_length)
    if len(text) > max_length:
        text = text[0:max_length - 1]
    return text


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

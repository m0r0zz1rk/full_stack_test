import uuid

from apps.common.logger.logger import app_logger
from apps.common.utils.django.exception import get_traceback
from apps.product.exceptions.product_exception import ProductNotExist, ProductInfoNotValid, ProductSaveError, \
    ProductDeleteError
from apps.product.selectors.product_selector import product_model, product_queryset


class ProductService:
    """Класс методов для работы с товарами"""

    @staticmethod
    def is_product_exists(search: dict):
        """
        Проверка на существующий товар в БД
        :param search: словарь, ключ - поле модели, значение - значение поля
        :return: ProductNotExists в случае отсутствия товара или товар - объект product
        """
        if not product_model.objects.filter(**search).exists():
            app_logger.error(f'Попытка получить несуществующий товар: {repr(search)}')
            raise ProductNotExist
        return product_queryset().filter(**search).first()

    def get_product(self, attribute_name: str, value: str) -> product_model:
        """
        Получение товара по атрибуту
        :param attribute_name: наименование атрибута (поля модели product)
        :param value: значение атрибута
        :return: объект product (или исключение ProductNotExist)
        """
        search = {attribute_name: value}
        return self.is_product_exists(search)

    @staticmethod
    def validate_product(product_info: dict) -> bool:
        """
        Валидация полученного объекта с полями модели product
        :param product_info: объект с информацией о товаре
        :return: True - данные валидны, False - данные не валидны
        """
        for field in product_model._meta.get_fields():
            if field.name not in ['id', 'created_at', 'updated_at', *product_info.keys()]:
                app_logger.error(f'Поле модели товара "{field.name}" не найдено в полученном объекте'
                                 f': {repr(product_info)}')
                return False
        return True

    def save_product(self, product_info: dict):
        """
        Сохранение информации по товару (создание, редактирование)
        :param product_info: словарь с информацией о товаре
        :return: ProductInfoNotValid - если полученные данные не валидны,
                 ProductSaveError - если произошла ошибка во время сохранения информации по товару
        """
        if not self.validate_product(product_info):
            raise ProductInfoNotValid
        new_prod = product_model()
        text = 'Добавлен новый товар'
        if 'id' in product_info:
            text = 'Товар обновлен'
            new_prod = product_model.objects.get(id=product_info['id'])
            del product_info['id']
        try:
            for key, value in product_info.items():
                setattr(new_prod, key, value)
            new_prod.save()
            info = new_prod.__dict__
            del info['_state']
            app_logger.info(f'{text}: {info}')
            return info
        except Exception:
            app_logger.error(f'Ошибка в процессе сохранения информации по товару: {get_traceback()}')
            raise ProductSaveError

    def delete_product(self, product_id: uuid.UUID):
        """
        Удаление товара
        :param product_id: id товара
        :return: ProductNotExists в случае отсутствия товара
        """
        product = self.is_product_exists({'id': product_id})
        try:
            log_obj = repr(product)
            product.delete()
            app_logger.info(f'Товар удален: {repr(log_obj)}')
            del log_obj
        except Exception:
            app_logger.error(f'Ошибка в процессе удаления товара: {get_traceback()}')
            raise ProductDeleteError

from django.core.validators import MinValueValidator
from django.db import models

from apps.common.base_model import BaseModel
from apps.product.consts.product_category import ProductCategory


class Product(BaseModel):
    """Модель товаров"""

    # Категория товара (можно реализовать через FK)
    category = models.CharField(
        choices=[(cat.value, cat.name) for cat in ProductCategory],
        max_length=12,
        default=ProductCategory.FOOD,
        verbose_name='Категория товаров'
    )

    # Наименование товара
    name = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        default='Новый товар',
        verbose_name='Наименование товара'
    )

    # Описание товара
    description = models.TextField(
        max_length=5000,
        blank=True,
        default='',
        verbose_name='Описание товара'
    )

    # Количество на складе (должна быть отдельной таблицей, в рамках тестового оставлю все в одном)
    count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество товара на складе'
    )

    # Стоимость
    price = models.FloatField(
        validators=[MinValueValidator(0.01), ],
        default=0.01,
        verbose_name='Стоимость товара'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

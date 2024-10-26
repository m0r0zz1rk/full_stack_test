import uuid

from django.db import models


class BaseModel(models.Model):
    """Базовая таблица приложения"""

    # Уникальный идентификатор объекта
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Идентификатор'
    )

    # Дата создания объекта
    created_at = models.DateField(
        auto_now_add=True,
        editable=False,
        verbose_name='Дата создания объекта'
    )

    # Дата обновления объекта
    updated_at = models.DateField(
        auto_now=True,
        verbose_name='Дата крайнего обновления объекта'
    )

    # Менеджер объектов
    objects = models.Manager()

    class Meta:
        abstract = True

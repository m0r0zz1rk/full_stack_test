from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

product_model = apps.get_model('product', 'Product')


def product_queryset() -> QuerySet:
    """Получение QuerySet со всеми товарами, отсортированными по дате добавления"""
    return product_model.objects.all().order_by('-created_at')


class ProductFilter(filters.FilterSet):
    """Класс для фильтрации товаров"""
    category = name = description = filters.CharFilter(
        lookup_expr='icontains'
    )
    count = price = filters.NumberFilter()
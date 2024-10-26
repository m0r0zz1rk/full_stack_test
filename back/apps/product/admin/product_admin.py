from django.contrib import admin

from apps.product.selectors.product_selector import product_model


@admin.register(product_model)
class ProductAdmin(admin.ModelAdmin):
    """Класс для отображения модели товаров в административной панели"""
    list_display = ('category', 'name', 'count', 'price')
    search_fields = ('category', 'name')

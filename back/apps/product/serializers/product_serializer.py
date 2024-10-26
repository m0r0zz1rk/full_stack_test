from rest_framework import serializers

from apps.product.consts.product_category import ProductCategory
from apps.product.selectors.product_selector import product_model


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для list, retrieve или update товара"""

    category = serializers.SerializerMethodField(
        label='Категория товара'
    )
    created_at = serializers.DateField(
        format='%d.%m.%Y',
        label='Дата добавления товара'
    )

    def get_category(self, obj):
        for category in ProductCategory:
            if category.name == obj.category:
                return category.value
        return obj.category

    class Meta:
        model = product_model
        exclude = ('updated_at', )


class ProductCreateUpdateSerializer(ProductSerializer):
    """Сериалиазатор для добавления/обновления товара"""

    created_at = None
    category = serializers.CharField(
        label='Категория товара'
    )

    def get_category(self, obj):
        for category in ProductCategory:
            if category.name == obj.category:
                return category.value
        return obj.category

    class Meta(ProductSerializer.Meta):
        exclude = ProductSerializer.Meta.exclude + ('id', 'created_at')

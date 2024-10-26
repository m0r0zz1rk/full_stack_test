from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.common.decorators.api_decorator import api_logging
from apps.common.exceptions.serializer_exceptions import SerializeDataError
from apps.common.utils.django.pagination import CustomPagination
from apps.common.utils.django.response import ResponseUtils
from apps.product.selectors.product_selector import product_queryset, ProductFilter, product_model
from apps.product.serializers.product_serializer import ProductSerializer, ProductCreateUpdateSerializer
from apps.product.service.product_service import ProductService


class ProductViewSet(viewsets.ModelViewSet):
    """Класс эндпоинтов для работы с товарами"""

    _response_utils = ResponseUtils()
    _product_service = ProductService()

    queryset = product_queryset()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = ProductFilter
    permission_classes = [AllowAny, ]
    lookup_field = 'id'

    @swagger_auto_schema(
        tags=['Товары', ],
        operation_description="Получение списка товаров",
        responses={
            '400': 'Ошибка при получении списка товаров',
            '200': ProductSerializer(many=True)
        }
    )
    @api_logging(product_model)
    def list(self, request, *args, **kwargs):
        """Получение списка товаров"""
        default_list = super(ProductViewSet, self).list(request, *args, **kwargs)
        return self._response_utils.ok_response(default_list.data)

    @swagger_auto_schema(
        tags=['Товары', ],
        operation_description="Добавление товара",
        request_body=ProductCreateUpdateSerializer,
        responses={
            '400': 'Ошибка при добавлении товара',
            '201': ProductCreateUpdateSerializer
        }
    )
    @api_logging(product_model)
    def create(self, request, *args, **kwargs):
        """Добавление товара"""
        serialize = ProductCreateUpdateSerializer(data=request.data)
        if serialize.is_valid():
            proc = self._product_service.save_product(serialize.validated_data)
            return self._response_utils.create_success_response(proc)
        else:
            serialize_exc = SerializeDataError
            serialize_exc.errors = serialize.errors
            raise serialize_exc

    @swagger_auto_schema(
        tags=['Товары', ],
        operation_description="Обновление товара",
        request_body=ProductCreateUpdateSerializer,
        responses={
            '400': 'Ошибка при обновлении товара',
            '200': ProductCreateUpdateSerializer
        }
    )
    @api_logging(product_model)
    def partial_update(self, request, *args, **kwargs):
        """Обновление товара"""
        serialize = ProductCreateUpdateSerializer(data=request.data)
        if serialize.is_valid():
            proc = self._product_service.save_product({
                'id': self.kwargs['id'],
                **serialize.validated_data
            })
            return self._response_utils.ok_dict_response(proc)
        else:
            serialize_ecx = SerializeDataError
            serialize_ecx.errors = serialize.errors
            raise serialize_ecx

    @swagger_auto_schema(
        tags=['Товары', ],
        operation_description="Удаление товара",
        responses={
            '400': 'Ошибка при удалении товара',
            '200': 'Сообщение "Товар успешно удален"'
        }
    )
    @api_logging(product_model)
    def destroy(self, request, *args, **kwargs):
        self._product_service.delete_product(self.kwargs['id'])
        return self._response_utils.ok_response('Товар успешно удален')

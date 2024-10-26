from apps.common.routers.crud_no_retrieve_router import CRUDNoRetrieveRouter
from apps.product.api.product_api import ProductViewSet

product_router = CRUDNoRetrieveRouter(trailing_slash=True)
product_router.register('product', ProductViewSet)

urlpatterns = product_router.urls

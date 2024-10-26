from apps.product.exceptions.product_exception import ProductNotExist, ProductInfoNotValid, ProductSaveError, \
    ProductDeleteError
from apps.product.selectors.product_selector import product_model

# Маппинг наименования модели БД к исключениям
api_exceptions_mapping = {
    product_model: {
        'exc_not_exist': ProductNotExist,
        'exc_info_not_valid': ProductInfoNotValid,
        'exc_save_error': ProductSaveError,
        'exc_delete_error': ProductDeleteError
    }
}

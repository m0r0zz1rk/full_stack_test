class ProductNotExist(Exception):
    """
    Исключение, вызываемое при попытке получения несуществующего товара в БД
    """
    pass


class ProductInfoNotValid(Exception):
    """
    Исключение, вызываемое при попытке сохранить информацию по товару с невалидными полями
    """
    pass


class ProductSaveError(Exception):
    """
    Исключение, вызываемое при возникновении ошибки в процессе сохранения информации по товару
    """
    pass


class ProductDeleteError(Exception):
    """
    Исключение, вызываемое при возникновении ошибки в процессе удаления товара
    """
    pass

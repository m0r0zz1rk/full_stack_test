class SerializeDataError(Exception):
    """
    Исключение, вызываемое в случае возникновения ошибки при сериализации полученных данных
    """
    errors = {}

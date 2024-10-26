class DjangoSettingsParameterNotExist(Exception):
    """
    Исключение, вызываемое при попытке получить несуществующий параметр
    из конфигурации Django
    """
    pass

from django.conf import settings

from apps.common.exceptions.django_settings import DjangoSettingsParameterNotExist


def get_settings_parameter(param_name: str):
    """
    Получение параметра из конфигурации приложения Django
    :param param_name: имя параметра
    :return: значение параметра или DjangoSettingsParameterNotExist если
    параметр не найден
    """
    if hasattr(settings, param_name):
        return getattr(settings, param_name)
    raise DjangoSettingsParameterNotExist

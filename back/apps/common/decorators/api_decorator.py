import datetime
import uuid
from functools import wraps

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.common.base_model import BaseModel
from apps.common.decorators.api_exceptions_mapping import api_exceptions_mapping
from apps.common.exceptions.serializer_exceptions import SerializeDataError
from apps.common.logger.logger import app_logger
from apps.common.utils.django.exception import get_traceback
from apps.common.utils.django.response import ResponseUtils

response_utils = ResponseUtils()


def api_logging(
        model: BaseModel
):
    """Декоратор для логирования обращений к эндпоинтам"""
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(request, *args, **kwargs):
            # Фиксация идентификатора сообщения
            log_id = uuid.uuid4()
            # Фиксация времени обращения
            time_appeal = datetime.datetime.now(datetime.UTC).strftime("%d.%m.%Y %H:%M:%S")

            # Логирование обращения
            app_logger.info(f'Обращение к эндпоинту {model._meta.verbose_name.title()} "{func.__name__}" № {log_id}  '
                            f'в {time_appeal}')

            # Формулировка текста ошибки (при исключении)
            error_text = (f'Обращение к эндпоинту {model._meta.verbose_name.title()} '
                          f'"{func.__name__}" № {log_id} '
                          f'от {time_appeal} завершено с ошибкой - ')

            # Получение исключений для модели
            try:
                exceptions = api_exceptions_mapping.get(model)
            except KeyError:
                exceptions = {
                    'exc_not_exist': model.DoesNotExist,
                    'exc_info_not_valid': ValidationError,
                    'exc_save_error': RuntimeError,
                    'exc_delete_error': RuntimeError
                }
            try:
                with transaction.atomic():
                    return func(request, *args, **kwargs)
            # Ошибка при сериализации (serialize.is_valid не прошел)
            except SerializeDataError as e:
                response_text = 'Ошибка сериализации данных'
                app_logger.error(f'{error_text}{response_text}: {repr(e.errors)}')
                return response_utils.bad_request_response(response_text)
            # Кастомные исключения для моделей приложения
            except exceptions['exc_not_exist']:
                response_text = 'Товар не найден'
                app_logger.warning(error_text + response_text)
                return response_utils.bad_request_response(response_text)
            except exceptions['exc_info_not_valid']:
                response_text = 'Получены не валидные данные'
                app_logger.warning(error_text + response_text)
                return response_utils.bad_request_response(response_text)
            except exceptions['exc_save_error']:
                response_text = 'Ошибка в процессе сохранения товара'
                app_logger.error(error_text + response_text)
                return response_utils.bad_request_response(response_text)
            except exceptions['exc_delete_error']:
                response_text = 'Ошибка в процессе удаления товара'
                app_logger.warning(error_text + response_text)
                return response_utils.bad_request_response(response_text)
            except Exception:
                response_text = 'Произошла системная ошибка'
                app_logger.warning(f'{error_text}{response_text}: {get_traceback()}')
                return response_utils.internal_server_error_response(response_text)
        return inner_wrapper
    return wrapper

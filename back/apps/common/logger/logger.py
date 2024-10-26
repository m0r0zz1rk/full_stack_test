import logging
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from apps.common.logger.log_level_mapping import log_level_mapping
from apps.common.utils.django.settings import get_settings_parameter


class Logger:
    """Класс создания объекта для логирования событий приложения"""

    logging_object = logging

    def __init__(self):
        """
        Настройка конфигурации логирования
        """

        # Получение минимального уровня события для записи в лог
        try:
            env_level = get_settings_parameter('LOGGER_LEVEL_START')
        except ImproperlyConfigured:
            env_level = 'info'

        # Получение имени файла
        try:
            env_filename = get_settings_parameter('LOG_FILENAME')
        except ImproperlyConfigured:
            env_filename = 'test-logs.txt'

        # Получение корневого пути
        try:
            base_dir = get_settings_parameter('BASE_DIR')
        except ImproperlyConfigured:
            base_dir = Path(__file__).resolve().parent.parent.parent.parent

        self.logging_object.basicConfig(
            level=log_level_mapping.get(env_level),
            filename=os.path.join(base_dir, str(env_filename)),
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s'
        )


app_logger = Logger().logging_object

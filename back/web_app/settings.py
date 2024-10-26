import os
import environ

from pathlib import Path

# Получаем путь до родительского каталога проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Переходим в каталог с файлом settings.py
SETTINGS_DIR = os.path.join(BASE_DIR, 'web_app')

# Считываем настройки из .env
env = environ.Env()
env.read_env(os.path.join(SETTINGS_DIR, 'env/.env'))

"""
    В зависимости от значения START в файле .env
    выбираем нужную конфигурацию проекта
"""

if env.str('START') == 'PROD':
    print('Сервер запущен в режиме PRODUCTION\n')
    from .vars.prod import * # noqa
else:
    print('Сервер запущен в режим DEVELOPMENT\n')
    from .vars.dev import * # noqa

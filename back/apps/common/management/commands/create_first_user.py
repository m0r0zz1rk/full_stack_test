from django.core.management import BaseCommand

from apps.common.service.user_service import UserService


class Command(BaseCommand):
    """Команда для создания первого пользователя администратора"""

    def handle(self, *args, **options):
        UserService.create_first_user()

from django.contrib.auth.models import User


class UserService:
    """Класс общих методов для работы с пользователями"""

    @staticmethod
    def create_first_user():
        """
        Создание нового пользователя Django с ролью администратора в случае, если нет других пользователей
        :return:
        """
        if User.objects.count() > 0:
            return
        new_user = User.objects.create_user(
            username='admin',
            email='admin@admin.ru',
            password='12345678',

        )
        new_user.is_staff = True
        new_user.is_superuser = True
        new_user.save()
        print('Создан новый пользователь: логин - admin, пароль - 12345678')

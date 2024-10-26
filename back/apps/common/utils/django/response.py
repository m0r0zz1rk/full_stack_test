from rest_framework import status
from rest_framework.response import Response


class ResponseUtils:
    """Класс для генерации ответов на запросы"""

    @staticmethod
    def bad_request_response(message) -> Response:
        """Генерация ответа с кодом 400 и ошибкой error"""
        return Response(
            {'error': message},
            status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def ok_response(message) -> Response:
        """Генерация ответа с кодом 200 и словарем с ключом success и сообщением"""
        return Response(
            {'success': message},
            status=status.HTTP_200_OK
        )

    @staticmethod
    def ok_dict_response(info: dict) -> Response:
        """Генерация ответа с кодом 200 и словарем с информацией"""
        return Response(
            info,
            status=status.HTTP_200_OK
        )

    @staticmethod
    def create_success_response(serializer_data) -> Response:
        """Генерация ответа с кодом 201 и данными по созданному объекту"""
        return Response(
            serializer_data,
            status=status.HTTP_201_CREATED
        )

    @staticmethod
    def internal_server_error_response(message: str) -> Response:
        """Генерация ответа с кодом 500 и сообщением"""
        return Response(
            {'error': message},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

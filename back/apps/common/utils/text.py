from faker import Faker

faker = Faker('ru-RU')


def generate_text(min_length: int, max_length: int) -> str:
    """
    Генерация текста
    :param min_length: минимальная длина, кол-во символов
    :param max_length: максимальная длина, кол-во символов
    :return: строка
    """
    text = faker.text(max_nb_chars=max_length)
    if min_length != 0:
        while len(text) < min_length:
            text += faker.text(max_nb_chars=max_length)
    if len(text) > max_length:
        text = text[0:max_length - 1]
    return text

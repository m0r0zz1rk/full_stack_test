import urllib.parse


def uri_text(source_text: str) -> str:
    """
    Конвертация русских символов для GET параметров
    :param source_text: исходный текст
    :return: текст urlencode
    """
    return urllib.parse.quote(source_text)

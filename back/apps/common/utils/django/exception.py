import sys
import traceback


def get_traceback() -> str:
    """Получение traceback исключения"""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    trb = repr(
        traceback.format_exception(
            exc_type, exc_value, exc_traceback
        )
    )
    return trb

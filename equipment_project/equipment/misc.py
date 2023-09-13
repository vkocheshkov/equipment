import re
from datetime import datetime
from rest_framework.views import exception_handler


def get_pattern(sn_mask):
    """
    Возвращает паттерн регулярного выражения в зависимости от символов N,A,a,X,Z, где
    • N - цифра от 0 до 9;
    • A - прописная буква латинского алфавита;
    • a - строчная буква латинского алфавита;
    • X - прописная буква латинского алфавита либо цифра от 0 до 9;
    • Z - символ из списка: -, _, @
    """
    mask = {
        "N": "\\d",
        "A": "[A-Z]",
        "a": "[a-z]",
        "X": "[A-Z,0-9]",
        "Z": "[-_@]"
    }
    pattern = "^"
    for item in sn_mask:
        mask_sign = mask.get(item, None)
        if mask_sign:
            pattern += mask.get(item)
        else:
            raise ValueError({"description": "В маске должны быть только символы N,A,a,X,Z"})
    return pattern + "$"


def validate_sn(sn_list, pattern):
    """
    Проверяет среди переданного списка серийных номеров на соответствие маске
    """
    errors = []
    for item in sn_list:
        if not re.match(pattern, item):
            errors.append(item)
    return errors


def present_datetime(date_obj):
    """
    Приводит дату к формату %Y-%m-%d %H:%M:%S
    """
    if isinstance(date_obj, datetime):
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def custom_exception_handler(exc, context):
    """
    Стандартизирует вывод ошибок API - в формат {"error":true, "description": "Описание ошибки"}
    """

    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        errors = []
        customized_response = {}
        customized_response["error"] = True
        customized_response["description"] = errors

        for key, value in response.data.items():
            errors.append(f"field {key}: {value}")

        customized_response["description"] = ", ".join(errors)
        response.data = customized_response

    return response
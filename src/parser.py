import re


class PhoneParser:
    """Класс для парсинга номера телефона."""

    class ParseError(Exception):
        """Ошибка парсинга."""

        pass

    @staticmethod
    def _remove_whitespaces(phone: str) -> str:
        """Убрать необязательные знаки из записи номера."""

        phone = phone.replace('-', '').replace("+", '')
        return "".join(phone.split())

    @staticmethod
    def _check_validity(phone: str) -> tuple[bool, str]:
        """Проверить правильность паттерна номера телефона."""

        rus_phone_pattern = re.compile(r"[78]\d{10}")
        if re.fullmatch(rus_phone_pattern, phone) is None:
            return False, f"Телефон '{phone}' не подходит под паттерн [78]XXXXXXXXXX"
        else:
            return True, ""

    @staticmethod
    def _normalize(phone: str) -> str:
        """Нормализовать номер телефона (8 => +7)."""

        if phone.startswith("7"):
            return "+" + phone
        else:
            return "+7" + phone[1:]

    @staticmethod
    def parse(phone: str) -> str:
        """
            Спарсить номер телефона.

            Выдает ошибку ParseError, если не удалось.
        """

        phone = PhoneParser._remove_whitespaces(phone)

        is_valid, error = PhoneParser._check_validity(phone)
        if not is_valid:
            raise PhoneParser.ParseError(error)

        return PhoneParser._normalize(phone)


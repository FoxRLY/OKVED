import requests
import json
from typing import Generator
from src.data import OkvedData


class OkvedDownloader:
    """Класс для скачивания списка ОКВЭД."""

    URL = "https://raw.githubusercontent.com/bergstar/testcase/refs/heads/master/okved.json"
    """Адрес для скачивания файла."""

    class DownloadFailed(Exception):
        """Ошибка скачивания."""

        pass

    @staticmethod
    def get_okveds() -> list[OkvedData]:
        """
            Получить список ОКВЭД.

            Выбрасывает исключение DownloadFailed, если загрузка завершилась с ошибкой.
        """

        response = requests.get(OkvedDownloader.URL)

        if response.status_code == 200:
            data = json.loads(response.content.decode())
            return list(OkvedDownloader._flatten([OkvedDownloader._parse_okveds(okved) for okved in data]))
        else:
            raise OkvedDownloader.DownloadFailed(response.status_code, response.content.decode())

    @staticmethod
    def _parse_okveds(json_data: dict) -> list[OkvedData]:
        """Спарсить ОКВЭД из JSON-строки."""

        result = [OkvedData(code=json_data["code"], name=json_data["name"])]

        if (child_list := json_data.get("items")) is not None:
            result += list(OkvedDownloader._flatten([OkvedDownloader._parse_okveds(child) for child in child_list]))

        return result

    @staticmethod
    def _flatten(items: list) -> Generator:
        """Уменьшить вложенность списка."""

        for x in items:
            if isinstance(x, list):
                yield from OkvedDownloader._flatten(x)
            else:
                yield x


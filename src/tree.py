from src.data import OkvedData


class SearchTreeNode:
    """Нода поискового древа."""

    def __init__(self):
        """Инициализация пустой ноды."""

        self.links: list[SearchTreeNode | None] = [None] * 10
        self.data: OkvedData | None = None

    def add(self, data: OkvedData, path: str):
        """Добавление данных в древо на основе пути."""

        # Если путь заканчивается - мы на нужной ноде, сохраняем данные в нее
        if path == "":
            self.data = data
            return

        # Индекс следующей ноды и остаток пути
        link_index = int(path[-1])
        path_remainder = path[:-1]

        # Если следующей ноды по индексу не существует - создаем
        next_node = self.links[link_index]
        next_node = next_node if next_node else SearchTreeNode()

        # Продвигаем операцию сохранения дальше по древу
        next_node.add(data, path_remainder)

        # Сохраняем/обновляем ноду в списке дочерних текущей ноды
        self.links[link_index] = next_node

    def find(self, path: str, last_found: OkvedData | None = None) -> OkvedData | None:
        """Поиск данных по пути ноды"""

        # Если на текущей ноде нашли данные, то запоминаем их
        if self.data is not None:
            last_found = self.data

        # Если путь закончился, то возвращаем последние найденные данные
        if path == "":
            return last_found

        # Индекс следующей ноды и остаток пути
        link_index = int(path[-1])
        path_remainder = path[:-1]

        # Пытаемся получить следующую ноду
        next_node = self.links[link_index]

        # Если ее нет, то возвращаем последние найденные данные
        if next_node is None:
            return last_found
        # Иначе проходим дальше по древу
        else:
            return next_node.find(path_remainder, last_found)


class OkvedSearchTree:
    """Древо поиска для ОКВЭД."""

    def __init__(self):
        """Инициализация древа поиска."""

        self.start_node: SearchTreeNode = SearchTreeNode()

    def add(self, data: OkvedData):
        """Добавить ОКВЭД в древо."""

        path = OkvedSearchTree._path_from_code(data.code)

        if path is None:
            return

        self.start_node.add(data, path)

    def find_by_phone(self, phone: str) -> tuple[OkvedData, int] | None:
        """Найти ОКВЭД по номеру телефона."""

        path = OkvedSearchTree._path_from_phone(phone)

        if path is None:
            return None

        found_okved = self.start_node.find(path)

        if found_okved is None:
            return None

        return found_okved, len(OkvedSearchTree._path_from_code(found_okved.code)) # type: ignore

    @staticmethod
    def _path_from_code(code: str) -> str | None:
        """Получить путь из кода ОКВЭД."""

        code = code.replace('.', '')
        if code.isnumeric():
            return code
        else:
            return None

    @staticmethod
    def _path_from_phone(phone: str) -> str | None:
        """Получить путь из номера телефона."""

        phone = phone.replace('+', '')
        if phone.isnumeric():
            return phone
        else:
            return None


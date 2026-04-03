from src.downloader import OkvedDownloader
from src.parser import PhoneParser
from src.tree import OkvedSearchTree
import argparse

parser = argparse.ArgumentParser(description="Игра 'Найди свой ОКВЭД по номеру телефона'.")
parser.add_argument("phone", help="Номер телефона в формате +7XXXXXXXXXX")
args = parser.parse_args()

try:
    phone = PhoneParser.parse(args.phone)
except PhoneParser.ParseError as e:
    print(f"Ошибка парсинга номера: {e}")
    exit()

print(f"Ищем ОКВЭД по номеру {phone}...")

try:
    okveds = OkvedDownloader.get_okveds()
except OkvedDownloader.DownloadFailed as e:
    print(f"Ошибка получения списка ОКВЭД: {e}")
    exit()

tree = OkvedSearchTree()

for data in okveds:
    tree.add(data)

found_okved = tree.find_by_phone(phone)

if found_okved:
    print("ОКВЭД найден!\n")
    print(f"Телефон: {phone}")
    print(f"ОКВЭД: {found_okved.code} | {found_okved.name}")
    print(f"Длина совпадения: {len(OkvedSearchTree._path_from_code(found_okved.code))}") # type: ignore
else:
    print("Не повезло!")


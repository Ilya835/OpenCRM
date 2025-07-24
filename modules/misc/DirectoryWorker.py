import os
import csv
from typing import Dict, List, Optional

name = "Менеджер папки"


class DirectoryWorker:
    def __init__(self, directory):
        """
        Класс для менеджмента папки.
        :param directory: Рабочая папка (передается при инициализации класса)
        :
        """
        self.directory = directory
        self.files = {}
        self.update()

    def update(self, filename_filter=None, data_filter=None):
        accepted_filename = ".DAT"
        required_filenames = ["HEADER", "TYPES"]

        for i in os.listdir(self.directory):
            if os.path.isfile(i):
                if i.find(accepted_filename) != -1:
                    with open(i, "r") as file:
                        reader = csv.reader(file, delimiter=";")
                        for row in reader:
                            self.files[i] = row
                else:
                    continue
        self.files = filter_and_sort_dict(self.files, filename_filter, data_filter)

        for i in os.listdir(self.directory):
            if os.path.isfile(i):
                for filename in required_filenames:
                    if i.find(filename) != -1:
                        with open(i, "r") as file:
                            reader = csv.reader(file, delimiter=";")
                            for row in reader:
                                self.files[i] = row

    def save_file(self, filename, array):
        with open(filename, "w") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(array)


def filter_and_sort_dict(
    data_dict: Dict[str, List],
    filename: Optional[str] = None,
    data: Optional[List] = None,
) -> List[tuple]:
    """
    Фильтрует и сортирует записи словаря по совпадению с filename и data.

    :param data_dict: Словарь, где ключи — строки, значения — списки.
    :param filename: Строка, которая должна содержаться в ключе (опционально).
    :param data: Список для частичного сравнения со значениями словаря (опционально).
    :return: Возвращает отсортированный список кортежей (ключ, значение) с учётом совпадений.
    """
    filtered_entries = []

    for key, value in data_dict.items():
        matches = {
            "key": False,
            "data": False,
            "score": 0,  # Общий "вес" совпадения (для сортировки)
        }

        # Проверяем совпадение filename в ключе
        if filename is not None and filename in key:
            matches["key"] = True
            matches["score"] += 2  # Больший вес, чем у data

        # Проверяем частичное совпадение data со значением
        if data is not None and any(item in value for item in data):
            matches["data"] = True
            matches["score"] += 1

        # Если хотя бы одно условие выполнено (или оба)
        if (filename is None or matches["key"]) or (data is None or matches["data"]):
            filtered_entries.append((key, value, matches["score"]))

    # Сортируем по убыванию "score" (лучшие совпадения — в начале)
    filtered_entries.sort(key=lambda x: x[2], reverse=True)

    # Возвращаем только ключи и значения (без score)
    return dict([(key, value) for key, value, _ in filtered_entries])

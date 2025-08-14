import os
import csv
from typing import Dict, List, Optional

name = "Менеджер папки"


class DirectoryWorker:
    def __init__(self, directory):
        """
        Класс для менеджмента папки.
        :param directory: Рабочая папка (передается при инициализации класса)
        :param filenames: Имена файлов которые будут использоваться в обработке.
        :param files: Словарь массивов где ключ это имя файла, а значение это его содержимое.
        """
        self.filenames = {
            "Data": ".DAT",
            "Required": ["TYPES"],
            "Optional": ["HEADER", "FORMAT"],
        }
        self.directory = directory
        self.files = {}
        self.check_path(directory)
        self.update()

    def update(self, filename_filter=None, data_filter=None):
        # Чтение разрешенных файлов
        for i in os.listdir(self.directory):
            if i.find(self.filenames["Data"]) != -1:
                self.files[i] = read_from_csv_stroke(self.directory + i)
        # Сортировка и фильтрация данных в словаре
        self.files = filter_and_sort_dict(self.files, filename_filter, data_filter)
        # Чтение обязательных функциональных файлов
        for i in os.listdir(self.directory):
            for filename in self.filenames["Required"]:
                if i.find(filename) != -1:
                    self.files[i] = read_from_csv_stroke(self.directory + i)
        # Чтение опциональных функциональных файлов
        for filename in self.filenames["Optional"]:
            for i in os.listdir(self.directory):
                if i.find(filename) != -1:
                    self.files[i] = read_from_csv_stroke(self.directory + i)

    def check_path(self, path):
        print(f"Проверяется следующий путь: {path}")
        count_of_data_files = 0
        count_of_required = {}
        count_of_optional = {}
        for i in os.listdir(self.directory):
            if i.find(self.filenames["Data"]) != -1:
                count_of_data_files += 1
            for filename in self.filenames["Required"]:
                if i.find(filename) != -1:
                    if filename not in count_of_required:
                        count_of_required[filename] = 1
                    else:
                        count_of_required[filename] += 1
            for filename in self.filenames["Optional"]:
                if i.find(filename) != -1:
                    if filename not in count_of_optional:
                        count_of_optional[filename] = 1
                    else:
                        count_of_optional[filename] += 1
        print(f"Количество файлов данных: {count_of_data_files} шт.")
        print(f"Обязательные функциональные файлы: {count_of_required}")
        for filename in self.filenames["Required"]:
            if filename not in count_of_required:
                print(
                    f"Не найден обязательный функциональный файл {filename}.\nСоздаю файл-заглушку {filename} в переданом пути: {path}."
                )
                save_file(path + "TYPES", ["Строка"])
        print(f"Опциональные функционнальные файлы: {count_of_optional}")


def save_file(filename, array):
    try:
        with open(filename, "w") as file:
            csv.writer(file, delimiter=";").writerow(array)
    except IOError as error:
        print(f"Что-то пошло не так при чтении файла. Вот ошибка: {error}")


def read_from_csv_stroke(path):
    try:
        with open(path, "r") as file:
            return list(csv.reader(file, delimiter=";"))[0]
    except IOError as error:
        print(f"Что-то пошло не так при чтении файла. Вот ошибка: {error}")


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

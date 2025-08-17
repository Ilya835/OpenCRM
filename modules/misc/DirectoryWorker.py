import os
import csv
import glob
import numpy as np
import multiprocessing
from functools import partial
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Union, Any

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
            "Data": "*.DAT",
            "Required": ["TYPES"],
            "Optional": ["HEADER", "FORMAT"],
        }
        self.directory = directory
        self.files = {}
        self.check_path(directory)
        self.update()

    ParsedValue = Union[str, int, float, bool, datetime, None]

    def parse_value(self, value: str) -> ParsedValue:
        value = value.strip()
        if not value:
            return None
        if value.lower() in ("true", "false", "yes", "no", "Ð´Ð°", "Ð½ÐµÑ"):
            return value.lower() in ("true", "yes", "Ð´Ð°", "1")
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value.replace(",", "."))
        except ValueError:
            pass
        date_formats = [
            "%Y-%m-%d",
            "%d.%m.%Y",
            "%Y/%m/%d",
            "%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ]
        for fmt in date_formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return value

    def vectorize_mixed_data(self, arr: List[ParsedValue]) -> np.ndarray:
        vector = []
        for item in arr:
            if isinstance(item, (int, float)):
                vector.append(float(item))
            elif isinstance(item, bool):
                vector.append(1.0 if item else 0.0)
            elif isinstance(item, datetime):
                vector.append(item.timestamp())
            elif item is None:
                vector.append(0.0)
            else:
                vector.append(float(hash(item) % 10000) / 10000)
        return np.array(vector)

    def mixed_similarity(self, a: List[ParsedValue], b: List[ParsedValue]) -> float:
        vec_a = self.vectorize_mixed_data(a)
        vec_b = self.vectorize_mixed_data(b)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        cosine = np.dot(vec_a, vec_b) / (norm_a * norm_b)
        return (cosine + 1) / 2

    def filter_worker(
        self,
        item: tuple[str, list[ParsedValue]],
        filter_array: list[ParsedValue],
        threshold: float,
    ) -> tuple[float, str, list[ParsedValue]] | None:
        key, array = item
        similarity = self.mixed_similarity(array, filter_array)
        return (similarity, key, array) if similarity >= threshold else None

    def parallel_filter_and_sort(
        self,
        data: dict[str, list[ParsedValue]],
        filter_array: list[ParsedValue],
        threshold: float = 0.3,
        processes: int | None = None,
    ) -> dict[str, list[ParsedValue]]:
        if not filter_array:
            return data
        if processes is None:
            processes = min(multiprocessing.cpu_count() - 1, 8)
        worker = partial(
            self.filter_worker, filter_array=filter_array, threshold=threshold
        )

        with multiprocessing.Pool(processes=processes) as pool:
            results = pool.imap_unordered(worker, data.items())
            filtered = [r for r in results if r is not None]
            filtered.sort(reverse=True, key=lambda x: x[0])

        return {key: array for _, key, array in filtered}

    def filter_and_sort(
        self,
        data: Dict[str, List[ParsedValue]],
        filter_array: Optional[List[ParsedValue]] = None,
        threshold: float = 0.3,
    ) -> Dict[str, List[ParsedValue]]:
        if filter_array is None:
            return data
        results = []
        for key, array in data.items():
            similarity = self.mixed_similarity(array, filter_array)
            if similarity >= threshold:
                results.append((similarity, key, array))
        results.sort(reverse=True, key=lambda x: x[0])
        return {key: array for _, key, array in results}

    def read_file(self, file_path: str) -> Dict[str, List[ParsedValue]]:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            data = next(reader)
            parsed = [self.parse_value(x) for x in data]
        return {file_path.split("/")[-1]: parsed}

    def read_files(self, path: str = ".\*"):
        file_paths = glob.glob(path)
        result_dict = {}
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(self.read_file, fp) for fp in file_paths]
            for future in futures:
                try:
                    result_dict.update(future.result())
                except Exception as e:
                    print(f"Произошла ошибка при чтении данных из файлов: {e}")
        return result_dict

    def update(self, data_filter=None, simlarity_threshold=None):
        self.files = self.read_files(self.directory + self.filenames["Data"])
        # Сортировка и фильтрация данных в словаре
        if data_filter:
            self.files = self.filter_and_sort(
                self.files, data_filter, simlarity_threshold
            )
        for i in self.filenames["Required"]:
            try:
                self.files[i] = self.read_files(self.directory + i)[i]
            except Exception as e:
                print(f"Не найден файл {i}. Ошибка {e}")
        for i in self.filenames["Optional"]:
            try:
                self.files[i] = self.read_files(self.directory + i)[i]
            except Exception as e:
                print(f"Не найден файл {i}. Ошибка {e}")

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
                save_stroke_to_csv(path + "TYPES", ["Строка"])
        print(f"Опциональные функционнальные файлы: {count_of_optional}")


def save_stroke_to_csv(filename, array):
    try:
        with open(filename, "w") as file:
            csv.writer(file, delimiter=";").writerow(array)
    except IOError as error:
        print(f"Что-то пошло не так при чтении файла. Вот ошибка: {error}")

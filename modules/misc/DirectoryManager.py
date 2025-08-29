import glob
import csv
import importlib.util
import multiprocessing
from . import PickablePixmap
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Any
from PyQt6 import QtCore

module_name = "Менеджер папки"

FORMATTED_TYPES = {
    "Строка": str,
    "Целое число": int,
    "Дробное число": float,
    "Время": QtCore.QDateTime().fromString,
}
UNFORMATTED_TYPES = {
    "Флажок": bool,
    "Фото": PickablePixmap.PickablePixmap,
}
TYPE_MAPPING = {**FORMATTED_TYPES, **UNFORMATTED_TYPES}


class DirectoryManager:
    """Высокопроизводительный менеджер директории"""

    def __init__(self, directory: str, max_workers: int = multiprocessing.cpu_count()):
        self.directory = Path(directory)
        self.max_workers = max_workers

        # Основной словарь всех файлов
        self.config_files: dict[str, list[Any]] = {}
        self.types: list[Any] = []
        # Отдельный словарь только для .DAT файлов с преобразованными данными
        self.data_files: dict[str, list[Any]] = {}
        self.custom_code = None

        self.update_files()

    def update_files(self) -> None:
        """Обновление словарей файлов"""
        # Очищаем словари перед обновлением
        self.config_files.clear()
        self.data_files.clear()

        file_loader = ParallelFileLoader(self.max_workers)

        # Находим все необходимые файлы
        all_files = []
        for pattern in ["TYPES", "HEADER", "FORMAT"]:
            all_files.extend(glob.glob(str(self.directory / pattern)))
        # Параллельная загрузка всех файлов
        self.config_files = file_loader.load_files_parallel(all_files)
        self.prepare_types()
        for pattern in ["HEADER", "FORMAT"]:
            if pattern not in self.config_files:
                self.config_files[pattern] = list(
                    str(" ") * len(self.config_files["TYPES"])
                )

        self.data_files = file_loader.load_files_parallel(
            glob.glob(str(self.directory / "*.DAT"))
        )
        # Загрузка пользовательского кода
        self._load_custom_code()

        # Преобразование .DAT файлов и заполнение data_files
        self._process_dat_files_parallel()

    def _load_custom_code(self) -> None:
        """Загрузка пользовательского кода"""
        dir_code_path = self.directory / "DirCode.py"
        if dir_code_path.exists():
            try:
                spec = importlib.util.spec_from_file_location("DirCode", dir_code_path)
                self.custom_code = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(self.custom_code)
                print("Пользовательский код загружен из DirCode.py")
            except Exception as e:
                print(f"Ошибка загрузки DirCode.py: {e}")

    def _process_dat_files_parallel(self) -> None:
        """Параллельная обработка .DAT файлов и заполнение data_files"""
        # Получаем сырые .DAT данные из основного словаря
        raw_dat_files = {**self.data_files}

        if not raw_dat_files:
            print("Не найдено .DAT файлов для обработки")
            return
        self.data_files.clear()
        print(f"Обработка {len(raw_dat_files)} .DAT файлов...")

        # Параллельное преобразование .DAT файлов
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for filename, raw_data in raw_dat_files.items():
                future = executor.submit(
                    self._convert_dat_file_data,
                    raw_data,
                    self.types,
                    self.config_files["FORMAT"],
                )
                futures[future] = filename

            # Собираем преобразованные данные в data_files
            for future in as_completed(futures):
                filename = futures[future]
                try:
                    converted_data = future.result()
                    # Сохраняем в словарь
                    self.data_files[filename] = converted_data
                except Exception as e:
                    print(f"Ошибка преобразования {filename}: {e}")
                    # В случае ошибки оставляем сырые данные
                    self.data_files[filename] = raw_dat_files[filename]

    def _convert_dat_file_data(
        self, data: List[str], types_config: List[Any], fmt_config: List[str]
    ) -> List[Any]:
        """Преобразование данных .DAT файла"""
        converted = []
        for i in range(len(data)):
            converted.append(
                self.parse_value(
                    data[i],
                    types_config[i],
                    fmt_config[i],
                )
            )
        return converted

    def prepare_types(self) -> None:
        for i in self.config_files["TYPES"]:
            self.types.append(TYPE_MAPPING[i])

    def parse_value(self, value: str, target_type: Any, fmt: str = " ") -> Any:
        self._cache: dict[str, Any] = {}
        self._cache_size = 100000
        if not value.strip():
            return None

        cache_key = f"{value}|{target_type}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        try:
            result = target_type(value)
            if len(self._cache) >= self._cache_size:
                self._cache.clear()
            self._cache[cache_key] = result

            return result

        except Exception as e:
            print(e)
            return value


class ParallelFileLoader:
    def __init__(self, max_workers: int = multiprocessing.cpu_count()):
        self.max_workers = max_workers

    def load_file(self, file_path: str) -> tuple[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=";")
                return Path(file_path).name, next(reader)
        except Exception as e:
            print(f"Ошибка загрузки {file_path}: {e}")
            return Path(file_path).name, None

    def load_files_parallel(self, file_paths: List[str]) -> Dict[str, Any]:
        results = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.load_file, fp): fp for fp in file_paths}

            for future in as_completed(futures):
                filename, content = future.result()
                if content is not None:
                    results[filename] = content

        return results

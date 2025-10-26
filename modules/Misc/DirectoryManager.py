import os
import sys
import glob
import pickle
import multiprocessing
from typing import Any, TypedDict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

inProjectRoot: bool = False
projectRoot: str = str(Path(__file__).resolve())
upToFolders: int = 0
while not inProjectRoot:
    projectRoot = str(Path(__file__).resolve().parents[upToFolders])
    if projectRoot.endswith("OpenCRM"):
        inProjectRoot = True
    upToFolders += 1
sys.path.append(projectRoot)
from modules.ModularUI.Units import UNITS_NAMING, UNITS_MAP


class DirectoryManager:
    """Высокопроизводительный менеджер директории"""

    class ColumnConfig(TypedDict):
        unit: str
        formating: str
        header: str
        hidden: bool

    default_config: list[ColumnConfig] = [
        {
            "unit": "Строка",
            "formating": None,
            "header": "Это автоматически сгенерированный файл заголовка.",
            "hidden": False,
        },
        {
            "unit": "Целое число",
            "formating": None,
            "header": "Это автоматически сгенерированный файл заголовка.",
            "hidden": False,
        },
        {
            "unit": "Дробное число",
            "formating": None,
            "header": "Это автоматически сгенерированный файл заголовка.",
            "hidden": False,
        },
        {
            "unit": "Дата и время",
            "formating": None,
            "header": "Это автоматически сгенерированный файл заголовка.",
            "hidden": False,
        },
    ]

    def __init__(self, directory: str, max_workers: int = multiprocessing.cpu_count()):
        self.directory = Path(directory)
        self.max_workers = max_workers  # Максимальное количество потоков
        self.directory_data: dict[Any] = {}  # Хранилище файлов

        def readFile():
            try:
                with open(self.directory.joinpath("SETTINGS.BIN"), "rb") as file:
                    return pickle.load(file)
            except Exception as error:
                print(
                    f"Ошибка при чтении файла SETTINGS.BIN: {error} \nПересоздаю файл."
                )
                with open(self.directory.joinpath("SETTINGS.BIN"), "wb") as file:
                    pickle.dump(self.default_config, file)
                with open(self.directory.joinpath("SETTINGS.BIN"), "rb") as file:
                    return pickle.load(file)

        self.config_file = readFile()
        self.data_suffix = "*.DAT"
        self.file_loader = self.ParallelFileLoader(self.max_workers)  # Загрузчик файлов
        self.update_files()

    def update_files(self) -> None:
        """Обновление словарей файлов."""
        self.directory_data.clear()  # Очищаем словари перед обновлением
        self.paths_list = glob.glob(
            str(self.directory / self.data_suffix)
        )  # Обновление путей до файлов в папке
        self.directory_data.update(
            self.file_loader.load_files_parallel(self.paths_list)
        )  # Параллельная загрузка всех файлов

    class ParallelFileLoader:
        """Загрузчик файлов использующий мультипроцессинг."""

        def __init__(self, max_workers: int = multiprocessing.cpu_count()):
            self.max_workers = max_workers

        def load_file(self, path: str) -> tuple[str, Any]:
            """Загружает бинарные данные из файла."""
            with open(path, "rb") as file:
                return Path(path).name, pickle.load(file)

        def save_file(self, path: str, data: list[Any]) -> None:
            """Сохраняет файл в биннарный файл по переданному пути."""
            with open(path, "wb") as file:
                pickle.dump(data, file)

        def load_files_parallel(self, file_paths: list[str]) -> dict[str, Any]:
            results = {}

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(self.load_file, fp): fp for fp in file_paths}

                for future in as_completed(futures):
                    filename, content = future.result()
                    if content is not None:
                        results[filename] = content

            return results


MainClass = DirectoryManager

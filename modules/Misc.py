import glob
import csv
import importlib.util
import multiprocessing
import pickle
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from pathlib import Path
from PyQt6 import QtWidgets, QtGui, QtCore
from typing import Any, Dict, List, Union, Callable

inProjectRoot: bool = False
projectRoot: str = str(Path(__file__).resolve())
upToFolders: int = 0
while not inProjectRoot:
    projectRoot = str(Path(__file__).resolve().parents[upToFolders])
    if projectRoot.endswith("OpenCRM"):
        inProjectRoot = True
    upToFolders += 1
sys.path.append(projectRoot)
from modules.Units import UNITS_NAMING, UNITS_MAP

module_name = "Дополнительные утилиты для QMenuBar"


class MenuUtils:
    """
    Набор утилит для работы с QMenuBar и QMenu.
    """

    class MenuItem(QtGui.QAction):
        def __init__(
            self,
            title: str,
            method: Callable[[Any], Any],
            checkable: bool = False,
            icon: Union[QtGui.QIcon, None] = None,
            objName: Union[str, None] = None,
        ):
            """
            Создает объект типа QAction из переданных при инициализации переменных.
            """
            super().__init__()
            self.setText(title)
            self.triggered.connect(method)
            self.setCheckable(checkable)
            if icon is not None:
                self.setIcon(icon)
            if objName is not None:
                self.setObjectName(objName)

    def setupMenuBar(
        self,
        menubar: QtWidgets.QMenuBar,
        content: Dict[str, List[Union[MenuItem, None]]],
        parent: QtWidgets.QGroupBox,
    ) -> None:
        """
        Создает ManuBar у переданного parent.
        """
        for i in list(content.keys()):
            menu = QtWidgets.QMenu(i, menubar)
            for j in content[i]:
                if j is None:
                    menu.addSeparator()
                else:
                    j.setParent(menu)
                    menu.addAction(j)
            menubar.addMenu(menu)
            menu.show()
        parent.layout().setMenuBar(menubar)

    def prepareContextMenu(
        self, context_menu: QtWidgets.QMenu, content: List[Union[MenuItem, None]]
    ) -> None:
        for action in content:
            if action is not None:
                context_menu.addAction(action)
            else:
                context_menu.addSeparator()


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
        self.raw_data_files: dict[str, list[str]] = {}
        self.custom_code = None
        self.update_files()

    def update_files(self) -> None:
        """Обновление словарей файлов"""
        # Очищаем словари перед обновлением
        self.config_files.clear()
        self.data_files.clear()
        self.raw_data_files.clear()
        file_loader = ParallelFileLoader(self.max_workers)

        # Находим все необходимые файлы
        all_files = []
        for pattern in ["TYPES", "HEADER", "FORMAT"]:
            all_files.extend(glob.glob(str(self.directory / pattern)))
        # Параллельная загрузка всех файлов
        self.config_files = file_loader.load_files_parallel(all_files)
        self.types = list(map(lambda x: UNITS_NAMING[x], self.config_files["TYPES"]))
        # self.prepare_types()
        for pattern in ["HEADER", "FORMAT"]:
            if pattern not in self.config_files:
                self.config_files[pattern] = list(
                    str(" ") * len(self.config_files["TYPES"])
                )

        self.raw_data_files = file_loader.load_files_parallel(
            glob.glob(str(self.directory / "*.DAT"))
        )
        # Загрузка пользовательского кода
        self._load_custom_code()

        # Преобразование .DAT файлов и заполнение data_files
        self._process_dat_files_parallel()
        print(self.data_files)

    def load_file(self, path: str) -> tuple[str, Any]:
        with open(path, "rb") as file:
            return Path(path).name, pickle.load(file)

    def save_file(self, path: str, data: List[Any]) -> None:
        with open(path, "wb") as file:
            pickle.dump(data, file)

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
        if not self.raw_data_files:
            print("Не найдено .DAT файлов для обработки")
            return
        self.data_files.clear()
        print(f"Обработка {len(self.raw_data_files)} .DAT файлов...")

        # Параллельное преобразование .DAT файлов
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for filename, raw_data in self.raw_data_files.items():
                future = executor.submit(
                    self._convert_dat_file_data, raw_data, self.types
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
                    self.data_files[filename] = self.raw_data_files[filename]

    def _convert_dat_file_data(
        self, data: List[str], types_config: List[Any]
    ) -> List[Any]:
        """Преобразование данных .DAT файла"""
        return list(
            map(
                lambda x, y: UNITS_MAP[y]["fromStrConverter"](x),
                data,
                types_config,
            )
        )


class ParallelFileLoader:
    """
    Загрузчик файлов использующий мультипроцессинг.
    """

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


class PickablePixmap(QtGui.QPixmap):
    """
    Класс для полноценной работы с QPixmap (избегает ошибки QPixmap object is not pickable)
    """

    def __reduce__(self) -> Any:
        return type(self), (), self.__getstate__()

    def __getstate__(self) -> QtCore.QByteArray:
        ba = QtCore.QByteArray()
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.OpenModeFlag.WriteOnly)
        stream << self
        return ba

    def __setstate__(self, ba: QtCore.QByteArray) -> None:
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.OpenModeFlag.ReadOnly)
        stream >> self

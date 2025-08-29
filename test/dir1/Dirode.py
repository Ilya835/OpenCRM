import glob, os, csv, time, multiprocessing, datetime
from pathlib import Path
from typing import Dict, List, Union, Any
from concurrent.futures import ThreadPoolExecutor


class BackgroundWorker:
    def __init__(self, path: str):
        self.folder_path = path
        self.stop_event = multiprocessing.Event()

        self.shared_data = multiprocessing.Manager().dict()
        self.lock = multiprocessing.Lock()

        self.process = None

    def work(self, stop_event, shared_data, lock):
        while not stop_event.is_set():
            try:
                folder = Path(self.folder_path)
                if not folder.exists():
                    time.sleep(1)
                    continue
                print(folder)
                read_files
                files = list(folder.glob("*"))
                time.sleep(1)
            except Exception as e:
                with lock:
                    shared_data.update({"error": str(e), "status": "error"})
                time.sleep(5)

    ParsedValue = Union[str, int, float, bool, datetime, None]

    def read_file(self, file_path: str) -> Dict[str, List[ParsedValue]]:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            data = next(reader)
            parsed = [self.parse_value(x) for x in data]
        return {file_path.split("/")[-1]: parsed}

    def read_files(self, path: str = "*.DAT"):
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

    def save_file(self, filename, array):
        try:
            with open(filename, "w") as file:
                csv.writer(file, delimiter=";").writerow(array)
        except IOError as error:
            print(f"Что-то пошло не так при чтении файла. Вот ошибка: {error}")

    def save_files(self, files: dict[str, list[ParsedValue]]):
        file_paths = files.keys()
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(self.read_file, fp) for fp in file_paths]
            for future in futures:
                try:
                    result_dict.update(future.result())
                except Exception as e:
                    print(f"Произошла ошибка при чтении данных из файлов: {e}")

    def start(self):
        if self.process and self.process.is_alive():
            return False
        self.stop_event.clear()
        self.process = multiprocessing.Process(
            target=self.work,
            args=(self.stop_event, self.shared_data, self.lock),
            daemon=True,
        )
        self.process.start()
        return True

    def stop(self):
        if self.process:
            self.stop_event.set()
            self.process.join(timeout=5)
            self.process.terminate()

    def get_data(self) -> Dict[str, Any]:
        with self.lock:
            return dict(self.shared_data)

    def __del__(self):
        self.stop()


worker = BackgroundWorker(os.path.dirname(__file__))
worker.start()

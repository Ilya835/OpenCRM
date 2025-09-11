import multiprocessing
import pickle
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, List
lenght = 1000
int_list = [x + 1 for x in range(lenght)]
str_list = ["TEST" + str(x) for x in range(lenght)]
test_list = []
for i in range(lenght):
    test_list.append([int_list[i], str_list[i]])

with open("test.bin", "wb") as file:
    pickle.dump(test_list, file)
class ParallelFileLoader:
    def __init__(self, max_workers: int = multiprocessing.cpu_count()):
        self.max_workers = max_workers

    def load_file(self, path: str,element:int) -> Any:
        with open(path, "rb") as file:
            return pickle.load(file)[element]

    def load_files_parallel(self, file_path: str) -> List[Any]:
        results: List[Any]= []
        list_length: int = 0
        with open(file_path, "rb") as file:
            list_length = len(pickle.load(file))
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.load_file, file_path, fp): fp for fp in range(list_length)}
            for future in as_completed(futures):
                results.append(future.result())
        return results


start_time = time.time()
loader = ParallelFileLoader()
loader.load_files_parallel("test.bin")
result_mp = time.time() - start_time

start_time = time.time()
test = []
with open("test.bin", "rb") as file:
    test = pickle.load(file)

result = time.time() - start_time
print(f"Время загрузки в несколько потоков: {result_mp}")
print(f"Время загрузки в 1 поток: {result}")
print(f"Разница во времени{result_mp - result}")

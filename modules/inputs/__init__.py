import os
import glob
import importlib
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(f"./logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
content = {}

for module_file in modules:
    module_name = os.path.basename(module_file)[:-3]
    if module_name == "__init__":
        continue
    try:
        module = importlib.import_module(f".{module_name}", package=__name__)
        globals()[module_name] = module
        content[module.name] = getattr(module, module_name)
        logger.info(f"Импортировано поле ввода данных {module_name}")
    except Exception as err:
        logger.exception(f"Ошибка импорта поля ввода данных {module_name}: {err}")

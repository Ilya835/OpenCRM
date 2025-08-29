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
UiFiles = {}

ui_skelets = glob.glob(os.path.join(os.path.dirname(__file__), "*.ui"))
for file in ui_skelets:
    os.system(f"pyuic6 {file} -o {file.replace('.ui', '.py')}")
ui_modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
for module_file in ui_modules:
    module_name = os.path.basename(module_file)[:-3]
    if module_name == "__init__":
        continue
    try:
        module = importlib.import_module(f".{module_name}", package=__name__)
        globals()[module_name] = module
        UiFiles[module.name] = getattr(module, module_name)
        logger.info(f"Импортирован виджет {module_name}")
    except Exception as error:
        logger.error(f"Ошибка импорта виджета {module_name}: {error}")

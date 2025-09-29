import os
import glob
import importlib
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
    except Exception as error:
        print(f"Ошибка импорта виджета {module_name}: {error}")

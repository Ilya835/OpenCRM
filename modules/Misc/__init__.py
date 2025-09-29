import os
import glob
import importlib

modules_files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
for module_file in modules_files:
    module_name = os.path.basename(module_file)[:-3]
    if module_name == "__init__":
        continue
    try:
        module = importlib.import_module(f".{module_name}", package=__name__)
        globals()[module_name] = module.MainClass
    except Exception as error:
        print(error)
        pass

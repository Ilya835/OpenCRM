import os
import glob
import importlib

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
Misc = {}

for module_file in modules:
    module_name = os.path.basename(module_file)[:-3]
    if module_name == "__init__":
        continue
    try:
        module = importlib.import_module(f".{module_name}", package=__name__)
        globals()[module_name] = module
        Misc[module.module_name] = getattr(module, module_name)
    except:
        pass

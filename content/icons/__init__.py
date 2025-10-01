import os
import glob
from PyQt6 import QtGui

Icons = {}
files_list = glob.glob(os.path.join(os.path.dirname(__file__), "*.svg"))
for file in files_list:
    Icons[os.path.basename(file)] = QtGui.QIcon(file)

""" Reload dynamically freecad workbench without needance toward restart entire application """

import sys
import importlib

# Add the module path
sys.path.append('C:/Users/micha/AppData/Roaming/FreeCAD/Mod')

# Import and reload the module
import TwoByTwo
importlib.reload(TwoByTwo)
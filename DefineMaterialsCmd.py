import os
import FreeCADGui;
import FreeCAD as FCad
from utils.ModelTableView import MyTableModel
from PySide2.QtCore import QFile
from PySide2 import QtCore, QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDockWidget, QWidget, QTableView
# from PySide2 import QtWidgets, QtCore, QtGui

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(__dir__, "icons")
path_ui = os.path.join(__dir__, "ui", "definematerials.ui")

class DefineMaterials:
    """ Define materials sheet for construction """

    def GetResources(self):
        return {
            'Pixmap': os.path.join(iconPath, "gold_bar.svg"),  # Path to your icon
            'MenuText': 'Define Materials',
            'ToolTip': 'Define materials for your construction',
        }

    def Activated(self):
        # Load UI content from .ui file
        loader = QUiLoader()
        ui_file = QFile(path_ui)

        # Produce sepearate window
        global WIDGET_w # prevent shinny window from garbage collecting=
        WIDGET_w = loader.load(ui_file, None)
        WIDGET_w.show()
        
        # Modify a table view -> Add headers and make columns not editable by user
        table_view: QTableView = WIDGET_w.findChild(QTableView, "MaterialsList")
        my_model = MyTableModel([], ["Material Name", "Dimension", "Weight"])
        table_view.setModel(my_model)
        table_view.setEditTriggers(QTableView.NoEditTriggers)  # Disable editing

        # TODO: FreeCad read base documentation on a Github to understand how is, delegate button to table column



    def IsActive(self):
        # Return True if the command can be executed
        return True

# QtCore.Qt.LeftDockWidgetArea
FreeCADGui.addCommand('2by2_DefMaterials', DefineMaterials())

if __name__ == "main":
    print(path_ui)

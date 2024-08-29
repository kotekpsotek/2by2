import os
import re
import json
import FreeCADGui;
import FreeCAD as FCad
from pathlib import Path
from dataclasses import dataclass, asdict
from utils.API import Materials
from utils.API.ModelTableView import MyTableModel
from PySide2.QtCore import QFile
from PySide2 import QtCore, QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDockWidget, QWidget, QTableView, QPushButton, QTextEdit, QDialog, QLabel, QVBoxLayout, QComboBox, QStyledItemDelegate
from dataclasses import dataclass
from utils.GUI import MakeNewMaterialWindow

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(__dir__, "icons")
path_ui = os.path.join(__dir__, "ui", "definematerials.ui")
path_define_nmat_ui = os.path.join(__dir__, "ui", "define_new_materialui.ui")

@dataclass
class Material:
    materialName: str
    weight: float = 0

weightUnit = "g/mm3"
defaultMaterialsList = [Material("steel", 12)]

def format_material(mat: Material):
    """ Format material to string appear in form """
    return f"{mat.materialName} | {mat.weight}{weightUnit}"


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
        my_model = MyTableModel([], ["Material Name", "Weight|g/mm3"])
        table_view.setModel(my_model)
        table_view.setEditTriggers(QTableView.NoEditTriggers)  # Disable editing
        # TODO: FreeCad read base documentation on a Github to understand how is, delegate button to table column
        WIDGET_w.update()

        new_mat_class = MakeNewMaterialWindow(my_model)
        def_new_but: QPushButton = WIDGET_w.findChild(QPushButton, "DefineName")

        """ Load old materials """
        listMaterials = Materials().to_list()
        my_model.insertRows(0, len(listMaterials), listMaterials)

        """ Add remove button """
        my_model.insertColumns(my_model.columnCount(), 1)
        # TODO: Add button to last column for each row
        """ for row in range(my_model.rowCount()):
            button_w = QPushButton("Remove")
            table_view.setIndexWidget(my_model.index(row, my_model.columnCount() - 1), button_w) """

        """ Clicked on ready to use """
        def_new_but.clicked.connect(new_mat_class.display())

        # Combobox
        combobox: QComboBox = WIDGET_w.findChild(QComboBox, "SelectFromExistsing")
        for default_mat in defaultMaterialsList:
            """ Fullfill Combobox """
            combobox.addItem(format_material(default_mat), default_mat)

        """ Pass selected in combobox items to project materials list """
        def handle_add_comb():
            c_d: Material = combobox.currentData()
            my_model.insertRows(my_model.rowCount(), 1, [[c_d.materialName, c_d.weight]])
            # TODO: Save this material on list
            
        add_comb_b = WIDGET_w.findChild(QPushButton, "AddAccept")
        add_comb_b.clicked.connect(handle_add_comb)

        # Manage button handle
        def handle_manage():
            """ Display Manage Window """
        
        m_button = WIDGET_w.findChild(QPushButton, "manageList")
        m_button.clicked.connect(handle_manage)

        # TODO: Make list of ready to use materials
        # TODO: Remove existsing material from table via button and update QTableView model
        finish_but: QPushButton = WIDGET_w.findChild(QPushButton, "Accept")
        finish_but.clicked.connect(lambda: WIDGET_w.hide())


    def IsActive(self):
        # Return True if the command can be executed
        return True

# QtCore.Qt.LeftDockWidgetArea
FreeCADGui.addCommand('2by2_DefMaterials', DefineMaterials())

if __name__ == "main":
    print(path_ui)

import os
import json
import FreeCADGui;
import FreeCAD as FCad
from pathlib import Path
from dataclasses import dataclass, asdict
from utils.ModelTableView import MyTableModel
from PySide2.QtCore import QFile
from PySide2 import QtCore, QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDockWidget, QWidget, QTableView, QPushButton, QTextEdit, QDialog, QLabel, QVBoxLayout
# from PySide2 import QtWidgets, QtCore, QtGui
from dataclasses import dataclass

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(__dir__, "icons")
path_ui = os.path.join(__dir__, "ui", "definematerials.ui")
path_define_nmat_ui = os.path.join(__dir__, "ui", "define_new_materialui.ui")

@dataclass
class Material:
    materialName: str
    weight: int = 0

weightUnit = "g/mm3"

class Materials:
    def __init__(self, material: Material):
        self.material = material

    def save(self):
        """ Add new material to materials file """
        # Prepare data to save
        dict_material = asdict(self.material)

        # Save within file
        path_file = Path(__dir__, "data", "materials.json")
        
        def doesntexists():
            # define it
            dict_mat = { "materials": [dict_material] }

            # json it
            json_content = json.dumps(dict_mat)

            # save it
            file.write(json_content)

        # Operation on data file
        with path_file.open("r+") as file:
            
            if path_file.is_file(): # File exists
                # read it
                content = path_file.read_text()
                print(len(content))

                if len(content) > 0:
                    # decode it
                    json_decoder = json.JSONDecoder()
                    json_content = json_decoder.decode(content) # { "materials": [{ "materialName": "name", weight: 12 }] }

                    # Add to materials it
                    json_content["materials"].append(dict_material)

                    # save in file it
                    file.write(json.dumps(json_content))
                else:
                    doesntexists()
            else: # File doesn't exists
                doesntexists()

class MakeNewMaterialWindow:
    """Handle, user click on **"Define new"** button"""
    def __init__(self) -> None:
        new_mat = QUiLoader()
        def_mat_ui_file = QFile(path_define_nmat_ui)
        
        global DEF_MATERIAL
        DEF_MATERIAL = new_mat.load(def_mat_ui_file, None)
        DEF_MATERIAL.show()

        # Handle "define new material window logic"
        def addNewHandle():
            """ Add new material to list. Only when is fully correct """
            matname: str = DEF_MATERIAL.findChild(QTextEdit, "matSrcName").toPlainText().strip()
            weight: str = DEF_MATERIAL.findChild(QTextEdit, "weightSrc").toPlainText().strip()

            # Make checks
            if len(weight) != 0 and len(matname) != 0:
                # TODO: Check matname field has not same numbers
                if weight.isdigit():
                    mat = Material(materialName=matname, weight=weight)

                    # Save it to file with materials
                    Materials(material=mat).save()

                    DEF_MATERIAL.hide()
                else:
                    FCad.Console.PrintError("\"Weight\" field should contain just same number string")
            else:
                FCad.Console.PrintError("\"Weight\" and \"Material name\" fields cannot be empty!. Leave there your desired value")


        def cancelHandle():
            """ Omit new material without any save for current state within textFields """
            DEF_MATERIAL.hide()

        cancelButton = DEF_MATERIAL.findChild(QPushButton, "cancelButton")
        cancelButton.clicked.connect(cancelHandle)
        
        addButton = DEF_MATERIAL.findChild(QPushButton, "addButton")
        addButton.clicked.connect(addNewHandle)

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

        def_new_but: QPushButton = WIDGET_w.findChild(QPushButton, "DefineName")
        def_new_but.clicked.connect(MakeNewMaterialWindow())


    def IsActive(self):
        # Return True if the command can be executed
        return True

# QtCore.Qt.LeftDockWidgetArea
FreeCADGui.addCommand('2by2_DefMaterials', DefineMaterials())

if __name__ == "main":
    print(path_ui)

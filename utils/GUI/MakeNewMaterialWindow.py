import re
import FreeCAD as FCad
from utils.API import Materials
from utils.API.ModelTableView import MyTableModel
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from DefineMaterialsCmd import Material, path_define_nmat_ui
from PySide2.QtWidgets import QDockWidget, QWidget, QTableView, QPushButton, QTextEdit, QDialog, QLabel, QVBoxLayout, QComboBox, QStyledItemDelegate

class MakeNewMaterialWindow:
    """Handle, user click on **"Define new"** button"""
    def __init__(self, table_model: MyTableModel) -> None:
        self.table_view = table_model

    def display(self):
        def src():
            new_mat = QUiLoader()
            def_mat_ui_file = QFile(path_define_nmat_ui)
            
            global DEF_MATERIAL
            DEF_MATERIAL = new_mat.load(def_mat_ui_file, None)
            DEF_MATERIAL.show()
            
            def addNewHandle():
                """ Add new material to list. Only when is fully correct """
                matname: str = DEF_MATERIAL.findChild(QTextEdit, "matSrcName").toPlainText().strip()
                weight: str = DEF_MATERIAL.findChild(QTextEdit, "weightSrc").toPlainText().strip()

                # Make checks
                if len(weight) != 0 and len(matname) != 0:
                    if weight.isdigit() and re.search(r'[a-zA-Z]', matname):
                        mat = Material(materialName=matname, weight=weight)

                        # Save it to file with materials
                        materials = Materials(material=mat)
                        materials.save()

                        # Update material list table
                        self.table_view.insertRows(self.table_view.rowCount(), 1, [[matname, weight]])

                        # Hide view when everything succeed
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

        return src
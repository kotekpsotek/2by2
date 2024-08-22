import os
import FreeCAD as App
import FreeCADGui as Gui

icon_dir = os.path.join(".", "icons", "workbench.svg")

class TwoByTwoWb(Workbench):

    MenuText = "2by2"
    ToolTip = "Get on paper how much specific material you need to create real world thing"
    Icon = """paste here the contents of a 16x16 xpm icon"""

    def Initialize(self):
        """This function is executed when the workbench is first activated.
        It is executed once in a FreeCAD session followed by the Activated function.
        """

        # import here all the needed files that create your FreeCAD commands
        import DefineMaterialsCmd;

        self.list = [
            "2by2_DefMaterials"
        ] # a list of command names created in the line above
        self.appendToolbar("2by2", self.list) # creates a new toolbar with your commands
        self.appendMenu("2by2", self.list) # creates a new menu
        self.appendMenu(["2by2"], self.list) # appends a submenu to an existing menu

    def Activated(self):
        """This function is executed whenever the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed whenever the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands", self.list) # add commands to the context menu

    def GetClassName(self): 
        # This function is mandatory if this is a full Python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(TwoByTwoWb())

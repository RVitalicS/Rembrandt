


from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as PyMELcore

import UI











class LightLibrary (UI.DockableWindow):



    def __init__ (self, renderer):
        
        super(LightLibrary, self).__init__(renderer)



    def rigClicked (self, userData):
 
        if userData["wanted"]:
 
            pass
 
        elif PyMELcore.selected():
 
            pass
 
        else:
            self.mayaEcho("select any object")



    def mayaEcho (self, message):

        PyMELcore.inViewMessage(
            assistMessage = message,
            position      = 'botCenter',
            fade          = True)

        print( "REMBRAND ECHO: {}".format(message) )










def show (renderer="renderman"):

    RembrandtWindow = LightLibrary(renderer)
    RembrandtWindow.show(dockable=True)





shelf_command = '''
import LightLibrary
# reload(LightLibrary)
LightLibrary.show()
'''




import os
import re

from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin



import RigIcon
import TreeItem
import Settings


UIsettings = Settings.UIsettings










class InfoComment (QtWidgets.QWidget):


    def __init__ (self):
        super(InfoComment, self).__init__()

        self.width         = UIsettings["info"]["commentWidth"]
        self.strokeHeight  = UIsettings["info"]["strokeHeight"]
        self.strokeSpacing = UIsettings["info"]["strokeSpacing"]


        self.setMaximumWidth(self.width)
        self.setMinimumWidth(self.width)


        self.fontLabel = Settings.makeFont(
            UIsettings["info"]["fontLabel"] )

        self.fontInfo = Settings.makeFont(
            UIsettings["info"]["fontInfo"] )


        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(self.strokeSpacing )


        strokeLayout = QtWidgets.QHBoxLayout()
        strokeLayout.setContentsMargins(0, 0, 0, 0)
        strokeLayout.setSpacing(0)

        labelItem = QtWidgets.QLabel("Comment:")
        labelItem.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        labelItem.setFixedHeight(self.strokeHeight)
        labelItem.setIndent(0)
        labelItem.setFont(self.fontLabel)


        strokeLayout.addWidget(labelItem)


        self.infoItem = QtWidgets.QLabel()
        self.infoItem.setWordWrap(True)
        self.infoItem.setFont(self.fontInfo)


        infoSpacer = QtWidgets.QSpacerItem(
            10, 10,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)


        mainLayout.addItem(strokeLayout)
        mainLayout.addWidget(self.infoItem)
        mainLayout.addItem(infoSpacer)

        self.setLayout(mainLayout)



    def setData (self, info):

        self.infoItem.setText(info)










class InfoBase (QtWidgets.QWidget):


    def __init__ (self):
        super(InfoBase, self).__init__()


        self.width         = UIsettings["info"]["baseWidth"]
        self.strokeHeight  = UIsettings["info"]["strokeHeight"]
        self.strokeSpacing = UIsettings["info"]["strokeSpacing"]

        self.labelWidth    = UIsettings["info"]["labelWidth"]
        self.colonWidth    = UIsettings["info"]["colonWidth"]


        self.ID   = QtWidgets.QLabel()
        self.Date = QtWidgets.QLabel()


        self.setMaximumWidth(self.width)
        self.setMinimumWidth(self.width)


        self.fontLabel = Settings.makeFont(
            UIsettings["info"]["fontLabel"] )

        self.fontInfo = Settings.makeFont(
            UIsettings["info"]["fontInfo"] )


        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(30)


        infoIcon = QtWidgets.QPushButton("")
        infoIcon.setObjectName("infoIcon")
        infoIcon.setFlat(True)
        infoIcon.setCheckable(False)
        infoIcon.setFixedSize(
            UIsettings["info"]["iconSize"],
            UIsettings["info"]["iconSize"])

        iconSpacer = QtWidgets.QSpacerItem(
            0, 0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)

        infoLayout = QtWidgets.QVBoxLayout()
        infoLayout.setContentsMargins(0, 0, 0, 0)
        
        infoLayout.addWidget(infoIcon)
        infoLayout.addItem(iconSpacer)
        

        mainLayout.setStretch(1, 1)
        mainLayout.addItem(infoLayout)
        mainLayout.addItem(self.createInfoBlock())


        self.setLayout(mainLayout)



    def createInfoBlock (self, number=None, date=None):

        ID   = number if number else "-"
        Date = date if date else "-"

        strokeID   = self.createStroke("ID", ID)
        strokeDate = self.createStroke("Date", Date)

        dataLayout = QtWidgets.QVBoxLayout()
        dataLayout.setContentsMargins(0, 0, 0, 0)
        dataLayout.setSpacing(self.strokeSpacing)

        dataSpacer = QtWidgets.QSpacerItem(
            0, 0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)

        dataLayout.addItem(strokeID)
        dataLayout.addItem(strokeDate)
        dataLayout.addItem(dataSpacer)

        return dataLayout



    def createStroke (self, label, info):

        strokeLayout = QtWidgets.QHBoxLayout()
        strokeLayout.setContentsMargins(0, 0, 0, 0)
        strokeLayout.setSpacing(0)

        labelItem = QtWidgets.QLabel(label)
        labelItem.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        labelItem.setFixedSize(self.labelWidth, self.strokeHeight)
        labelItem.setIndent(0)
        labelItem.setFont(self.fontLabel)

        colonItem = QtWidgets.QLabel(":")
        colonItem.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        colonItem.setFixedSize(self.colonWidth, self.strokeHeight)
        colonItem.setIndent(0)
        colonItem.setFont(self.fontLabel)

        infoItem = QtWidgets.QLabel(info)
        infoItem.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        infoItem.setFixedHeight(self.strokeHeight)
        infoItem.setIndent(0)
        infoItem.setFont(self.fontInfo)

        strokeLayout.addWidget(labelItem)
        strokeLayout.addWidget(colonItem)
        strokeLayout.addWidget(infoItem)

        if label == "ID":
            self.ID   = infoItem
        else:
            self.Date = infoItem

        return strokeLayout



    def setData (self, ID, date):

        self.ID.setText(ID)
        self.Date.setText(date)










class OptionsWidget (QtWidgets.QWidget):


    def __init__ (self):
        super(OptionsWidget, self).__init__()


        self.setMaximumHeight( UIsettings["options"]["height"] )
        self.setMinimumHeight( UIsettings["options"]["height"] )


        self.setAutoFillBackground(True)

        palette = QtGui.QPalette()
        palette.setColor(
            QtGui.QPalette.Background,
            QtGui.QColor(UIsettings["options"]["colorBackground"]) )
        self.setPalette(palette)


        fontLabel = Settings.makeFont(
            UIsettings["options"]["fontLabel"] )

        fontButton = Settings.makeFont(
            UIsettings["options"]["fontButton"] )


        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setContentsMargins(
            UIsettings["options"]["margin"],
            UIsettings["options"]["margin"],
            UIsettings["options"]["margin"],
            UIsettings["options"]["margin"] )
        self.mainLayout.setSpacing(0)


        self.infoBase = InfoBase()
        self.infoBase.hide()

        self.infoComment = InfoComment()
        self.infoComment.hide()



        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.setContentsMargins(0, 0, 30, 0)
        self.rightLayout.setSpacing( UIsettings["options"]["spacing"] )


        self.constraintLabel = QtWidgets.QLabel("CONSTRAINT")
        self.constraintLabel.setObjectName("constraintLabel")
        self.constraintLabel.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.constraintLabel.setIndent(0)

        self.constraintLabel.setFont(fontLabel)


        self.constraintGroup = QtWidgets.QButtonGroup()

        self.radioPoint = QtWidgets.QRadioButton("point")
        self.radioPoint.setObjectName("radioPoint")
        self.radioPoint.setProperty("option", "radio")
        self.radioPoint.setFont(fontButton)
        self.constraintGroup.addButton(self.radioPoint)

        self.radioParent = QtWidgets.QRadioButton("parent")
        self.radioParent.setObjectName("radioParent")
        self.radioParent.setProperty("option", "radio")
        self.radioParent.setFont(fontButton)
        self.constraintGroup.addButton(self.radioParent)


        self.leftLayout = QtWidgets.QVBoxLayout()
        self.leftLayout.setContentsMargins(50, 0, 50, 0)
        self.leftLayout.setSpacing( UIsettings["options"]["spacing"] )


        self.upGroup = QtWidgets.QButtonGroup()

        self.radioObject = QtWidgets.QRadioButton("object")
        self.radioObject.setObjectName("radioObject")
        self.radioObject.setProperty("option", "radio")
        self.radioObject.setFont(fontButton)
        self.upGroup.addButton(self.radioObject)

        self.radioWorld = QtWidgets.QRadioButton("world")
        self.radioWorld.setObjectName("radioWorld")
        self.radioWorld.setProperty("option", "radio")
        self.radioWorld.setFont(fontButton)
        self.upGroup.addButton(self.radioWorld)


        self.vectorLabel = QtWidgets.QLabel("UP VECTOR")
        self.vectorLabel.setObjectName("vectorLabel")
        self.vectorLabel.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.vectorLabel.setIndent(0)

        self.vectorLabel.setFont(fontLabel)


        self.rightSpacer = QtWidgets.QSpacerItem(
            0, 0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)

        self.leftSpacer = QtWidgets.QSpacerItem(
            0, 0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)

        self.bottomSpacer = QtWidgets.QSpacerItem(
            0, 0,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)


        self.rightLayout.addWidget(self.constraintLabel)
        self.rightLayout.addWidget(self.radioPoint)
        self.rightLayout.addWidget(self.radioParent)
        self.rightLayout.addItem(self.rightSpacer)


        self.leftLayout.addWidget(self.vectorLabel)
        self.leftLayout.addWidget(self.radioObject)
        self.leftLayout.addWidget(self.radioWorld)
        self.leftLayout.addItem(self.leftSpacer)


        self.mainLayout.addWidget(self.infoBase)
        self.mainLayout.addWidget(self.infoComment)

        self.mainLayout.addItem(self.bottomSpacer)
        self.mainLayout.addItem(self.leftLayout)
        self.mainLayout.addItem(self.rightLayout)


        self.setLayout(self.mainLayout)
        self.applySettings()



    def applySettings (self):

        with Settings.UIManager(update=False) as uiSettings:


            if self.radioObject.text() == uiSettings["upVector"]:

                self.radioObject.setChecked(True)

            else:
                self.radioWorld.setChecked(True)


            constraintSettings = uiSettings["constraint"]

            if constraintSettings:

                if self.radioPoint.text() == constraintSettings:

                    self.radioPoint.setChecked(True)

                else:
                    self.radioParent.setChecked(True)
                
                self.constraintLabel.setProperty("off", "False")
                self.radioPoint.setProperty("off", "False")
                self.radioParent.setProperty("off", "False")


            else:
                self.radioPoint.setChecked(False)
                self.radioParent.setChecked(False)

                self.constraintLabel.setProperty("off", "True")
                self.radioPoint.setProperty("off", "True")
                self.radioParent.setProperty("off", "True")

            self.setStyleSheet("")



    def constraintWrap (self, function):

        self.radioPoint.clicked.connect(
            lambda: function(self.radioPoint) )

        self.radioParent.clicked.connect(
            lambda: function(self.radioParent) )



    def upWrap (self, function):

        self.radioObject.clicked.connect(
            lambda: function(self.radioObject) )

        self.radioWorld.clicked.connect(
            lambda: function(self.radioWorld) )



    def infoManager (self, userData):

        spaceTrigger = 350


        if self.width() > spaceTrigger:

            ID = userData["ID"]
            date = userData["info"]["date"]

            self.infoBase.setData(ID, date)
            self.infoBase.show()


            spaceTrigger +=self.infoComment.width

            if self.width() > spaceTrigger:

                info = userData["info"]["text"]

                self.infoComment.setData(info)
                self.infoComment.show()



    def infoClose (self):

        self.infoBase.hide()
        self.infoComment.hide()










class LibraryWidget (QtWidgets.QWidget):


    def __init__ (self):
        super(LibraryWidget, self).__init__()


        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.topLayout = QtWidgets.QHBoxLayout()
        self.topLayout.setContentsMargins(0, 0, 0, 10)
        self.topLayout.setSpacing(0)

        self.previewLabel = QtWidgets.QLabel("ICON SIZE")
        self.previewLabel.setObjectName("previewLabel")
        self.previewLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.previewLabel.setIndent(10)

        font = Settings.makeFont( UIsettings["info"]["fontInfo"] )
        self.previewLabel.setFont(font)

        self.previewSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.previewSlider.setObjectName("previewSlider")
        self.previewSlider.setFixedWidth(35)
        self.previewSlider.setRange(1, 3)
        self.previewSlider.setTickInterval(1)

        with Settings.UIManager(update=False) as uiSettings:
            self.previewSlider.setValue(uiSettings["iconSize"])


        self.topSpacer = QtWidgets.QSpacerItem(
            10, 10,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)

        self.favoriteLabel = QtWidgets.QLabel("favotires")
        self.favoriteLabel.setObjectName("favoriteLabel")
        self.favoriteLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.favoriteLabel.setIndent(10)

        font = Settings.makeFont( UIsettings["info"]["fontInfo"] )
        self.favoriteLabel.setFont(font)

        self.favoriteButton = QtWidgets.QPushButton("")
        self.favoriteButton.setObjectName("favoriteButton")
        self.favoriteButton.setFlat(True)
        self.favoriteButton.setCheckable(True)
        self.favoriteButton.setFixedSize(16, 16)


        with Settings.UIManager(update=False) as uiSettings:
            if uiSettings["lovefilter"] == True:
                self.favoriteButton.setChecked(True)


        self.tab_vew = QtWidgets.QTabWidget()
        self.tab_vew.tabBarClicked.connect(self.tabAction)

        font = Settings.makeFont( UIsettings["info"]["fontInfo"] )
        self.tab_vew.setFont(font)


        self.options = OptionsWidget()
        self.options.constraintWrap(self.constraintOption)
        self.options.upWrap(self.upOption)


        self.topLayout.addWidget(self.previewLabel)
        self.topLayout.addWidget(self.previewSlider)
        self.topLayout.addItem(self.topSpacer)
        self.topLayout.addWidget(self.favoriteLabel)
        self.topLayout.addWidget(self.favoriteButton)

        self.mainLayout.addItem(self.topLayout)
        self.mainLayout.addWidget(self.tab_vew)
        self.mainLayout.addWidget(self.options)

        self.setLayout(self.mainLayout)


        self.previewSize = UIsettings["preview"]



    def tabAction (self, tabIndex):

        with Settings.UIManager() as uiSettings:
            uiSettings["itemTab"] = tabIndex



    def sliderWrap (self, function):

        self.previewSlider.valueChanged.connect(
            lambda value: function(value) )



    def constraintOption (self, radioItem):

        with Settings.UIManager() as uiSettings:

            lastChoice    = uiSettings["constraint"]
            currentChoice = radioItem.text()

            if lastChoice == currentChoice:
                radioItem.setCheckable(False)
                radioItem.setCheckable(True)
                currentChoice = ""

            else:
                radioItem.setCheckable(True)
                radioItem.setChecked(True)

            uiSettings["constraint"] = currentChoice

        self.options.applySettings()



    def upOption (self, radioItem):

        with Settings.UIManager() as uiSettings:
            uiSettings["upVector"] = radioItem.text()










class IconGrid (QtWidgets.QListView):

    rigClicked  = QtCore.Signal(dict)
    treeRequest = QtCore.Signal()
    applyFilter = QtCore.Signal()
    passInfo    = QtCore.Signal(dict)
    killInfo    = QtCore.Signal()


    def __init__(self):
        super(IconGrid, self).__init__()


        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setResizeMode(QtWidgets.QListView.Adjust)

        self.setLayoutMode(QtWidgets.QListView.Batched)
        self.setBatchSize(20)

        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setMovement(QtWidgets.QListView.Static)


        self.setDragEnabled(False)
        self.setAcceptDrops(False)

        self.setViewportMargins(QtCore.QMargins(2, 5, 3, 3))


        self.setMouseTracking(True)


        self.previewSize = {}
        self.hateMode = False



    def enterEvent (self, event):

        super(IconGrid, self).enterEvent(event)
        self.setFocus(QtCore.Qt.MouseFocusReason)



    def keyPressEvent (self, key_event):

        if key_event.key() == QtCore.Qt.Key_Control:
            self.hateMode = True
            self.update()



    def keyReleaseEvent (self, key_event):
        
        if key_event.key() == QtCore.Qt.Key_Control:
            self.hateMode = False
            self.update()



    def reloadTreeRequest (self):

        self.treeRequest.emit()



    def applyFilterSignal (self):

        self.applyFilter.emit()



    def rigClickedSignal (self, rigData):

        self.rigClicked.emit(rigData)



    def passInfoSignal (self, rigData):

        self.passInfo.emit(rigData)



    def killInfoSignal (self):

        self.killInfo.emit()










class ProjectWidget (QtWidgets.QWidget):


    def __init__ (self):
        super(ProjectWidget, self).__init__()


        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.wrapLayout = QtWidgets.QWidget()
        self.wrapLayout.setObjectName("parent")
        self.wrapLayout.setStyleSheet('''
            background-color: #636363;
            border-radius: 5px;''')


        self.projectLayout = QtWidgets.QHBoxLayout(self.wrapLayout)


        self.labelLayout = QtWidgets.QVBoxLayout(self.wrapLayout)
        self.labelLayout.setContentsMargins(10, 10, 30, 0)
        self.labelLayout.setSpacing(0)

        self.projectLabel = QtWidgets.QLabel("PLACE")
        self.projectLabel.setParent(self.wrapLayout)
        font = Settings.makeFont( UIsettings["project"]["fontLabel"] )
        self.projectLabel.setFont(font)

        self.extraInfo = QtWidgets.QLabel("info")
        self.extraInfo.setParent(self.wrapLayout)
        font = Settings.makeFont( UIsettings["project"]["fontInfo"] )
        self.extraInfo.setFont(font)


        self.projectPreview = QtWidgets.QPushButton(self.wrapLayout)
        self.projectPreview.setObjectName("projectPreview")
        self.projectPreview.setFlat(True)
        self.projectPreview.setFixedSize(
            UIsettings["project"]["previewWidth"],
            UIsettings["project"]["previewHeight"] )


        self.labelSpacer = QtWidgets.QSpacerItem(
            0, 0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)

        self.rightSpacer = QtWidgets.QSpacerItem(
            50, 00,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)

        self.bottomSpacer = QtWidgets.QSpacerItem(
            0,0,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)


        self.labelLayout.addWidget(self.projectLabel)
        self.labelLayout.addWidget(self.extraInfo)
        self.labelLayout.addItem(self.labelSpacer)

        self.projectLayout.addWidget(self.projectPreview)
        self.projectLayout.addItem(self.rightSpacer)
        self.projectLayout.addItem(self.labelLayout)

        self.mainLayout.addWidget(self.wrapLayout)
        self.mainLayout.addItem(self.bottomSpacer)
        self.setLayout(self.mainLayout)



    def changePoster (self, path):

        self.projectPreview.setStyleSheet('''
            QPushButton[objectName~="projectPreview"] {
                border: none;
                background-image: url(%s);
                background-repeat: repeat-n;
                background-position: center;
            } ''' % path)










class DockableWindow (MayaQWidgetDockableMixin, QtWidgets.QWidget):


    def __init__(self, renderer):
        super(DockableWindow, self).__init__()

        self.renderer = renderer


        self.setWindowTitle("Rembrandt")
        self.mainLayout = QtWidgets.QHBoxLayout()


        self.treeStructure = QtWidgets.QTreeWidget()
        self.treeStructure.setIndentation(0)
        self.treeStructure.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.treeStructure.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.treeStructure.setObjectName("tree")
        self.treeStructure.setFixedWidth( UIsettings["tree"]["width"] )
        self.treeStructure.header().setVisible(False)
        self.treeStructure.setItemsExpandable(True)
        self.treeStructure.itemClicked.connect(self.updateUI)
        self.treeStructure.setRootIsDecorated(False)
        self.focusTree = None


        self.projectMode = ProjectWidget()
        self.projectMode.hide()

        self.libraryMode = LibraryWidget()
        self.libraryMode.hide()
        self.libraryMode.favoriteButton.clicked.connect(self.favoriteAction)
        self.libraryMode.sliderWrap(self.sliderAction)

        
        self.mainLayout.addWidget(self.treeStructure)
        self.mainLayout.addWidget(self.libraryMode)
        self.mainLayout.addWidget(self.projectMode)
        self.mainLayout.setStretch(1, 0)
        self.mainLayout.setSpacing(5)



        self.setLayout(self.mainLayout)
        self.buildTree()


        stylesheet = os.path.join( os.path.dirname(__file__), "stylesheet.css" )
        self.setStyleSheet( open(stylesheet).read() )



    def buildTree (self):

        self.treeStructure.clear()


        library = Settings.LIB().load()["lights"]
        sortedLibrary = sorted(library.items(), key=lambda x: x[0])

        for projectItem in sortedLibrary:
            project = projectItem[0]

            projectData = self.createProjectData(library, project)

            projectRoot = self.buildTreeItem(
                projectData["representation"],
                projectData,
                self.treeStructure.invisibleRootItem())


            characters = library[project]["items"]
            sortedCharacters = sorted(characters.items(), key=lambda x: x[0])

            for characterItem in sortedCharacters:
                character = characterItem[0]

                projectItemData = self.createProjectItemData(library, project, character)

                self.buildTreeItem(
                    projectItemData["representation"],
                    projectItemData,
                    projectRoot)


        self.treeStructure.setItemDelegate(
            TreeItem.Delegate(self.treeStructure) )


        with Settings.UIManager(update=False) as uiSettings:
            itemTree = uiSettings["itemTree"]

            focusItem = None

            root = self.treeStructure.invisibleRootItem()

            for project_index in range(root.childCount()):
                project = root.child(project_index)

                project_name = project.data(0, QtCore.Qt.UserRole)["category"]

                if project_name == itemTree["project"]:
                    focusItem = project

                    if itemTree["character"]:
                        self.treeStructure.expandItem(project)

                        for character_index in range(project.childCount()):
                            character = project.child(character_index)

                            character_name = character.data(0, QtCore.Qt.UserRole)["category"]

                            if character_name == itemTree["character"]:
                                focusItem = character

            if not focusItem:
                focusItem = root.child(0)


            self.treeStructure.setCurrentItem(focusItem, QtCore.QItemSelectionModel.Select)
            self.updateUI(focusItem)



    def createProjectData (self, library, projectName):

        representationName = library[projectName]["name"]
        itemData           = library[projectName]["info"]

        return {
            "type": "project",
            "category": projectName,
            "representation": representationName,
            "data": itemData }



    def createProjectItemData (self, library, projectName, itemName):

        representationName = library[projectName]["items"][itemName]["name"]
        itemData           = library[projectName]["items"][itemName]["tabs"]

        wanted = library[projectName]["items"][itemName]["wanted"]


        dataIterator = library[projectName]["items"][itemName]["tabs"]
        for tab in dataIterator:
            tabData = dataIterator[tab]

            for lightIndex in range(len(tabData)):

                itemData[tab][lightIndex]["project"]   = projectName
                itemData[tab][lightIndex]["character"] = itemName
                itemData[tab][lightIndex]["tab"]       = tab

                itemData[tab][lightIndex]["wanted"]    = wanted

                itemData[tab][lightIndex]["renderer"]  = self.renderer


        return {
            "type": "character",
            "category": itemName,
            "representation": representationName,
            "data": itemData }



    def buildTreeItem (self, name, data, root):

        item = QtWidgets.QTreeWidgetItem()

        itemSize = QtCore.QSize()
        itemSize.setHeight( UIsettings["tree"]["height"] )
        item.setSizeHint(0, itemSize)

        item.setText(0, name)

        item.setFlags(
            QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsSelectable)

        item.setData(0, QtCore.Qt.UserRole, data)


        root.addChild(item)

        return item



    def reloadTreeItem (self):

        if not self.focusTree.childCount():

            library = Settings.LIB().load()["lights"]

            projectData = self.focusTree.parent().data(0, QtCore.Qt.UserRole)
            projectItemData = self.focusTree.data(0, QtCore.Qt.UserRole)

            projectName = projectData["category"]
            itemName = projectItemData["category"]

            projectItemData = self.createProjectItemData(library, projectName, itemName)

            self.focusTree.setData(0, QtCore.Qt.UserRole, projectItemData)



    def updateUI (self, tree_item):


        tree_selection_changed = False

        with Settings.UIManager() as uiSettings:

            itemTree = {}


            if tree_item.parent():
                itemTree["project"] = tree_item.parent().data(0, QtCore.Qt.UserRole)["category"]
                itemTree["character"] = tree_item.data(0, QtCore.Qt.UserRole)["category"]

            else:
                itemTree["project"] = tree_item.data(0, QtCore.Qt.UserRole)["category"]
                itemTree["character"] = ""


            if uiSettings["itemTree"]["project"] != itemTree["project"]:
                tree_selection_changed = True
            if uiSettings["itemTree"]["character"] != itemTree["character"]:
                tree_selection_changed = True


            uiSettings["itemTree"] = itemTree


        self.focusTree = tree_item


        if tree_item.childCount():
            self.treeStructure.collapseAll()
            self.treeStructure.setItemExpanded(tree_item, True)


        tree_item_data = tree_item.data(0, QtCore.Qt.UserRole)

        if tree_item_data["type"] == "project":

            self.libraryMode.hide()
            self.projectMode.show()
            self.posterUpdate(tree_item)
            
        elif tree_item_data["type"] == "character":

            self.projectMode.hide()
            self.libraryMode.show()
            self.libraryUpdate(tree_item_data)


            with Settings.UIManager() as uiSettings:

                if tree_selection_changed:
                    uiSettings["itemTab"] = 0

                else:
                    self.libraryMode.tab_vew.setCurrentIndex(uiSettings["itemTab"])



    def posterUpdate (self, tree_item):

        tree_item_name = tree_item.data(0, QtCore.Qt.UserRole)["category"]

        icon_path = os.path.join(os.path.dirname(__file__), "icons", "project")
        icon_path = os.path.join(icon_path, "{}_300x450.jpg".format(tree_item_name))
        icon_path = re.sub(r"\\", "/", icon_path)

        self.projectMode.changePoster(icon_path)

        self.projectMode.projectLabel.setText(tree_item.text(0).upper())
        self.projectMode.extraInfo.setText("")



    def libraryUpdate (self, tree_item_data):

        self.libraryMode.tab_vew.clear()


        with Settings.UIManager(update=False) as uiSettings:
            index = uiSettings["iconSize"]

            previewSize = self.libraryMode.previewSize[index-1]

            self.previewSizeX = previewSize["previewSizeX"]
            self.previewSizeY = previewSize["previewSizeY"]
            self.labelSize    = previewSize["labelSize"]
            self.gridSpace    = previewSize["gridSpace"]


        tree_item_data = tree_item_data["data"]
        for tab in tree_item_data:


            rigList = IconGrid()
            rigList.previewSize = previewSize

            rigList.treeRequest.connect(self.reloadTreeItem)
            rigList.applyFilter.connect(self.favoriteAction)

            rigList.passInfo.connect(self.libraryMode.options.infoManager)
            rigList.killInfo.connect(self.libraryMode.options.infoClose)

            rigList.rigClicked.connect(self.rigClicked)

            rigModel = QtGui.QStandardItemModel(rigList)


            rigList.setMinimumWidth(self.previewSizeX +self.gridSpace*2)
            rigList.setMinimumHeight(self.previewSizeY +self.gridSpace*2 +self.labelSize)


            rigList.setIconSize(QtCore.QSize(
                self.previewSizeX,
                self.previewSizeY +self.labelSize))

            rigList.setGridSize(QtCore.QSize(
                self.previewSizeX +self.gridSpace,
                self.previewSizeY +self.gridSpace +self.labelSize))


            for rigData in tree_item_data[tab]:

                RigID = rigData["ID"]

                with Settings.UIManager(update=False) as uiSettings:

                    if RigID not in uiSettings["hatelist"]:
                        if self.renderer in rigData:

                            if uiSettings["lovefilter"] == True:
                                if RigID in uiSettings["lovelist"]:
                                    self.buildIcon(rigModel, rigData)
                            else:
                                self.buildIcon(rigModel, rigData)


            rigList.setModel(rigModel)
            rigList.setItemDelegate( RigIcon.Delegate(rigList) )

            self.libraryMode.tab_vew.addTab(rigList, tab)



    def buildIcon (self, rigModel, rigData):

        iconItem = QtGui.QStandardItem()

        iconItem.setData(rigData, QtCore.Qt.EditRole)
        iconItem.setSizeHint(
            QtCore.QSize(
                self.previewSizeX,
                self.previewSizeY +self.labelSize))

        iconItem.setCheckable(False)
        iconItem.setEditable(True)

        rigModel.appendRow(iconItem)



    def favoriteAction (self):

        with Settings.UIManager() as uiSettings:
            uiSettings["lovefilter"] = self.libraryMode.favoriteButton.isChecked()

        self.updateUI(self.focusTree)



    def sliderAction (self, value):

        with Settings.UIManager() as uiSettings:
            uiSettings["iconSize"] = value

        self.updateUI(self.focusTree)



    def rigClicked (self, userData):

        pass

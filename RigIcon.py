


import os
import re
import tempfile

from PySide2 import QtWidgets, QtCore, QtGui



import Settings
import icons.resources



UIsettings = Settings.UIsettings










class Icon (object):


    def __init__ (self):


        self.rigData     = None
        self.previewSize = None


        self.pointer      = QtCore.QPoint(-1, -1)


        self.previewArea  = QtCore.QRect()

        self.favotireArea = QtCore.QRect()
        self.nameArea     = QtCore.QRect()
        self.setArea      = QtCore.QRect()

        self.infoArea     = QtCore.QRect()


        self.showName = True

        self.infoMode = False
        self.hateMode = False



    def paint (self, painter, iconArea, palette, isEditable=False):

        previewWidth  = self.previewSize["previewSizeX"]
        previewHeight = self.previewSize["previewSizeY"]
        labelHeight   = self.previewSize["labelSize"]

        nameWidth     = previewWidth



        # painter
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)


        clipPath = QtGui.QPainterPath()
        clipPath.addRoundedRect(
            iconArea,
            UIsettings["icon"]["cornerRadius"], 
            UIsettings["icon"]["cornerRadius"])

        painter.setClipPath(clipPath)
        painter.setPen(QtGui.Qt.NoPen)



        # info
        commentOffset = UIsettings["icon"]["infoCommentOffset"]
        borderOffset  = UIsettings["icon"]["infoBorderOffset"]

        self.infoArea.setX(iconArea.x() +commentOffset)
        self.infoArea.setY(iconArea.y() +borderOffset)
        self.infoArea.setWidth(iconArea.width() -commentOffset -borderOffset)
        self.infoArea.setHeight(iconArea.height() -borderOffset*2)


        if self.infoMode:
            painter.fillRect(iconArea, UIsettings["icon"]["colorBackground"])

            infoPosition = QtCore.QPoint(
                iconArea.x() +borderOffset,
                iconArea.y() +borderOffset)

            infoImage = QtGui.QImage(":/Rembrandt/info.png")
            painter.drawImage(infoPosition, infoImage)

            return



        # hover
        if iconArea.contains(self.pointer):
            painter.fillRect(iconArea, UIsettings["icon"]["colorHover"])
        else:
            painter.fillRect(iconArea, UIsettings["icon"]["colorBackground"])



        # rig preview
        previewPosition = QtCore.QPoint(
            iconArea.x(),
            iconArea.y())

        previewImage = QtGui.QImage(self.iconPath())

        painter.drawImage(previewPosition, previewImage)

        self.previewArea = QtCore.QRect(
            iconArea.x(),
            iconArea.y(),
            previewWidth,
            previewHeight )



        # favorite button
        nameBase = "favorites"
        if self.hateMode:
            nameBase = "skull"

        favotireImage = QtGui.QImage(":/Rembrandt/{}_disabled.png".format(nameBase))
        
        favotireHeight = favotireImage.height()
        favotireWidth  = favotireImage.width()

        x = iconArea.x() +(labelHeight -favotireHeight)/2
        y = iconArea.y() +previewHeight +(labelHeight -favotireHeight)/2

        self.favotireArea = QtCore.QRect(x, y, favotireWidth, favotireHeight)


        with Settings.UIManager(update=False) as uiSettings:

            if self.rigData["ID"] in uiSettings["lovelist"]:
                favotireImage = QtGui.QImage(":/Rembrandt/{}_enabled.png".format(nameBase))

            elif self.favotireArea.contains(self.pointer):
                favotireImage = QtGui.QImage(":/Rembrandt/{}_enabled.png".format(nameBase))


            painter.drawImage(QtCore.QPoint(x, y), favotireImage)



        # set button
        with Settings.LIBManager(update=False) as libSettings:

            RigID     = self.rigData["ID"]
            project   = self.rigData["project"]
            character = self.rigData["character"]

            set_data = libSettings["lights"][project]["items"][character]["sets"]


            for set_group in set_data:

                if RigID in set_group:


                    setImage = QtGui.QImage(":/Rembrandt/set_disabled.png")
                    
                    setHeight = setImage.height()
                    setWidth  = setImage.width()

                    x = iconArea.x() +iconArea.width() -setWidth -(labelHeight -setHeight)/2
                    y = iconArea.y() +previewHeight +(labelHeight -setHeight)/2

                    nameWidth -= setWidth + (labelHeight -setHeight)

                    self.setArea = QtCore.QRect(x, y, setWidth, setHeight)


                    with Settings.UIManager(update=False) as uiSettings:

                        if self.rigData["ID"] in uiSettings["setIDs"]:
                            setImage = QtGui.QImage(":/Rembrandt/set_enabled.png")

                        elif self.setArea.contains(self.pointer):
                            setImage = QtGui.QImage(":/Rembrandt/set_hover.png")


                        painter.drawImage(QtCore.QPoint(x,y), setImage)



        # name label
        if self.showName:

            nameHeight = favotireHeight

            nameOffset = labelHeight -favotireHeight + favotireHeight +4

            x = iconArea.x() +nameOffset
            y = iconArea.y() +previewHeight +(labelHeight -favotireHeight)/2

            nameWidth -= nameOffset

            self.nameArea = QtCore.QRect(x, y, nameWidth, nameHeight)


            painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)

            painter.setPen(
                QtGui.QPen(
                    QtGui.QBrush(QtGui.QColor( UIsettings["icon"]["colorLabel"] )),
                    0,
                    QtGui.Qt.SolidLine,
                    QtGui.Qt.RoundCap,
                    QtGui.Qt.RoundJoin) )

            font = Settings.makeFont( UIsettings["icon"]["fontLabel"] )
            painter.setFont(font)

            textOption = QtGui.QTextOption()
            textOption.setWrapMode(QtGui.QTextOption.NoWrap)
            textOption.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)

            painter.drawText(
                QtCore.QRectF(self.nameArea),
                self.rigData["name"],
                textOption)



    def sizeHint (self):

        return QtCore.QSize(
            self.previewSize["previewSizeX"],
            self.previewSize["previewSizeY"] + self.previewSize["labelSize"])



    def iconPath (self):

        name = "_".join([
            self.rigData["project"],
            self.rigData["character"],
            self.rigData["tab"],
            self.rigData["ID"],
            "{}x{}".format(
                self.previewSize["previewSizeX"],
                self.previewSize["previewSizeY"])
            ])

        path = os.path.join(os.path.dirname(__file__), "icons", self.rigData["renderer"])
        path = os.path.join(path, "{}{}".format(name, ".jpg"))
        path = re.sub(r"\\", "/", os.path.normpath(path))

        return path










class IconDrag (Icon):


    def __init__ (self, rigData, previewSize):

        self.rigData     = rigData
        self.previewSize = previewSize


        self.rigImage = self.paint()
        self.rigImage.setAlphaChannel(
            self.makeAlpha(self.rigImage.rect()) )



    def paint (self):

        previewWidth  = self.previewSize["previewSizeX"]
        previewHeight = self.previewSize["previewSizeY"]
        labelHeight   = self.previewSize["labelSize"]


        infoBorderOffset = UIsettings["icon"]["infoBorderOffset"]
        infoBlockOffset = UIsettings["icon"]["infoBlockOffset"]

        strokeHeight = UIsettings["info"]["strokeHeight"]
        strokeSpacing = UIsettings["info"]["strokeSpacing"]

        labelWidth = UIsettings["info"]["labelWidth"]
        colonWidth = UIsettings["info"]["colonWidth"]

        commentWidth = previewWidth-infoBlockOffset-infoBorderOffset
        commentHeight = self.calculateCommentHeight(commentWidth)

        infoHeight = strokeHeight*2 +strokeSpacing +infoBorderOffset*3 +commentHeight


        nameWidth     = previewWidth



        # device init.
        paintDevice = QtGui.QImage(
            QtCore.QSize(
                previewWidth,
                previewHeight +labelHeight +infoHeight ),
            QtGui.QImage().Format_RGBA8888 )

        paintDevice.fill( UIsettings["icon"]["colorBackground"] )



        # area init.
        paintArea = paintDevice.rect()



        # painter init.
        painter = QtGui.QPainter(paintDevice)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtGui.Qt.NoPen)



        # info area
        infoArea = QtCore.QRect(
            paintArea.x(),
            paintArea.y() +previewHeight +labelHeight,
            previewWidth,
            infoHeight)

        painter.fillRect(infoArea, UIsettings["icon"]["colorInfo"] )


        infoImage = QtGui.QImage(":/Rembrandt/info.png")

        x = paintArea.x() +infoBorderOffset
        y = paintArea.y() +previewHeight +labelHeight +infoBorderOffset

        painter.drawImage(QtCore.QPoint(x, y), infoImage)



        # preview
        previewPosition = QtCore.QPoint(
            paintArea.x(),
            paintArea.y())

        previewImage = QtGui.QImage(self.iconPath())

        painter.drawImage(previewPosition, previewImage)



        # favorite button
        favotireImage = QtGui.QImage(":/Rembrandt/favorites_disabled.png")
        
        favotireHeight = favotireImage.height()
        favotireWidth  = favotireImage.width()

        x = paintArea.x() +(labelHeight -favotireHeight)/2
        y = paintArea.y() +previewHeight +(labelHeight -favotireHeight)/2

        with Settings.UIManager(update=False) as uiSettings:

            if self.rigData["ID"] in uiSettings["lovelist"]:
                favotireImage = QtGui.QImage(":/Rembrandt/favorites_enabled.png")

        painter.drawImage(QtCore.QPoint(x, y), favotireImage)



        # set button
        with Settings.LIBManager(update=False) as libSettings:

            RigID     = self.rigData["ID"]
            project   = self.rigData["project"]
            character = self.rigData["character"]

            set_data = libSettings["lights"][project]["items"][character]["sets"]


            for set_group in set_data:

                if RigID in set_group:


                    setImage = QtGui.QImage(":/Rembrandt/set_disabled.png")
                    
                    setHeight = setImage.height()
                    setWidth  = setImage.width()

                    x = paintArea.x() +paintArea.width() -setWidth -(labelHeight -setHeight)/2
                    y = paintArea.y() +previewHeight +(labelHeight -setHeight)/2

                    nameWidth -= setWidth + (labelHeight -setHeight)


                    with Settings.UIManager(update=False) as uiSettings:

                        if self.rigData["ID"] in uiSettings["setIDs"]:
                            setImage = QtGui.QImage(":/Rembrandt/set_enabled.png")


                    painter.drawImage(QtCore.QPoint(x,y), setImage)



        # name label
        nameHeight = favotireHeight

        nameOffset = labelHeight -favotireHeight + favotireHeight +4

        x = paintArea.x() +nameOffset
        y = paintArea.y() +previewHeight +(labelHeight -favotireHeight)/2

        nameWidth -= nameOffset

        nameArea = QtCore.QRect(x, y, nameWidth, nameHeight)


        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)

        painter.setPen(
            QtGui.QPen(
                QtGui.QBrush(QtGui.QColor( UIsettings["icon"]["colorLabel"] )),
                0,
                QtGui.Qt.SolidLine,
                QtGui.Qt.RoundCap,
                QtGui.Qt.RoundJoin) )


        font = Settings.makeFont( UIsettings["icon"]["fontLabel"] )
        painter.setFont(font)

        textOption = QtGui.QTextOption()
        textOption.setWrapMode(QtGui.QTextOption.NoWrap)
        textOption.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)

        painter.drawText(
            QtCore.QRectF(nameArea),
            self.rigData["name"],
            textOption)



        # info label
        fontLabel = Settings.makeFont( UIsettings["info"]["fontLabel"] )
        painter.setFont(fontLabel)

        textOption = QtGui.QTextOption()
        textOption.setWrapMode(QtGui.QTextOption.NoWrap)
        textOption.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)

        painter.drawText(
            QtCore.QRectF(
                infoArea.x() +infoBlockOffset,
                infoArea.y() +infoBorderOffset,
                labelWidth, strokeHeight),
            "ID",
            textOption)

        painter.drawText(
            QtCore.QRectF(
                infoArea.x() +infoBlockOffset +labelWidth,
                infoArea.y() +infoBorderOffset,
                colonWidth, strokeHeight),
            ":",
            textOption)
        
        painter.drawText(
            QtCore.QRectF(
                infoArea.x() +infoBlockOffset,
                infoArea.y() +infoBorderOffset +strokeHeight +strokeSpacing,
                labelWidth, strokeHeight),
            "Date",
            textOption)

        painter.drawText(
            QtCore.QRectF(
                infoArea.x() +infoBlockOffset +labelWidth,
                infoArea.y() +infoBorderOffset +strokeHeight +strokeSpacing,
                colonWidth, strokeHeight),
            ":",
            textOption)


        fontInfo = Settings.makeFont( UIsettings["info"]["fontInfo"] )
        painter.setFont(fontInfo)

        painter.drawText(
            QtCore.QRectF(
                infoArea.x() +infoBlockOffset +labelWidth +colonWidth,
                infoArea.y() +infoBorderOffset,
                previewWidth -infoBlockOffset -labelWidth -colonWidth -infoBorderOffset, strokeHeight),
            self.rigData["ID"],
            textOption)

        painter.drawText(
            QtCore.QRectF(
                infoArea.x() +infoBlockOffset +labelWidth +colonWidth,
                infoArea.y() +infoBorderOffset +strokeHeight +strokeSpacing,
                previewWidth -infoBlockOffset -labelWidth -colonWidth -infoBorderOffset, strokeHeight),
            self.rigData["info"]["date"],
            textOption)

        textOption = QtGui.QTextOption()
        textOption.setWrapMode(QtGui.QTextOption.WordWrap)
        textOption.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        painter.drawText(
            QtCore.QRectF(
                infoArea.x() +infoBlockOffset,
                infoArea.y() +infoBorderOffset*2 +strokeHeight*2 +strokeSpacing,
                previewWidth -infoBlockOffset -infoBorderOffset, commentHeight),
            self.rigData["info"]["text"],
            textOption)



        # device output
        return painter.device()



    def calculateCommentHeight (self, commentWidth):

        comment = QtWidgets.QLabel()
        comment.setFixedWidth(commentWidth)
        comment.setWordWrap(True)

        font = Settings.makeFont( UIsettings["info"]["fontInfo"] )
        comment.setFont(font)

        comment.setText(self.rigData["info"]["text"])
        comment.adjustSize()

        commentHeight = comment.height()

        del(comment)
        return commentHeight



    def makeAlpha (self, paintArea):

        paintDevice = QtGui.QImage(
            QtCore.QSize(
                paintArea.width(),
                paintArea.height() ),
            QtGui.QImage().Format_Alpha8 )

        paintDevice.fill( QtGui.QColor(0, 0, 0, a=0) )


        painter = QtGui.QPainter(paintDevice)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtGui.Qt.NoPen)


        alphaPath = QtGui.QPainterPath()
        alphaPath.addRoundedRect(
            paintArea,
            UIsettings["icon"]["cornerRadius"], 
            UIsettings["icon"]["cornerRadius"])

        painter.fillPath(
            alphaPath,
            QtGui.QBrush( QtGui.QColor(255, 255, 255, a=255) ) )

        return painter.device()










class Editor (QtWidgets.QWidget):

    clicked = QtCore.Signal(dict)
    showInfo = QtCore.Signal(dict)
    leaveEditor  = QtCore.Signal()
    reloadTreeItem  = QtCore.Signal()
    applyFilter = QtCore.Signal()
    startDrag = QtCore.Signal()


    def __init__ (self, parent=None):
        super(Editor, self).__init__(parent)

        self.index   = None
        self.option  = None

        self.rigIcon = Icon()

        self.setMouseTracking(True)

        self.dragAccept = False
        self.dragStartPosition = QtCore.QPoint(0, 0)


        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)


        self.info = QtWidgets.QPlainTextEdit()
        self.info.setObjectName("info")
        self.info.setContentsMargins( 0, 0, 0, 0)

        self.info.setVisible(False)

        font = Settings.makeFont( UIsettings["info"]["fontInfo"] )
        self.info.setFont(font)


        self.rigName = QtWidgets.QLineEdit()
        self.rigName.setObjectName("rigName")
        self.rigName.setFrame(False)
        self.rigName.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.rigName.setContentsMargins( 0, 0, 0, 0)
        self.rigName.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.rigName.setVisible(False)

        self.rigName.mousePressEvent = self.renameStart
        self.rigName.editingFinished.connect(self.renameFinish)

        font = Settings.makeFont( UIsettings["info"]["fontEdit"] )
        self.rigName.setFont(font)



        self.mainLayout.addWidget(self.info)
        self.mainLayout.addWidget(self.rigName)
        self.setLayout(self.mainLayout)



    def mouseMoveEvent (self, event):

        self.rigIcon.pointer = QtCore.QPoint(
            event.x(),
            event.y())

        self.update()

        if self.dragAccept:
            dragDistance  = (event.pos() -self.dragStartPosition).manhattanLength()
            dragThreshold = QtWidgets.QApplication.startDragDistance()

            if dragDistance >= dragThreshold:
                self.startDrag.emit()



    def mousePressEvent (self, event):

        if event.button() == QtCore.Qt.MouseButton.RightButton:

            if not self.rigName.text():

                self.rigIcon.infoMode = True

                self.rigName.setVisible(False)

                self.info.setVisible(True)
                self.info.setGeometry(self.rigIcon.infoArea)
                self.info.setPlainText(self.rigIcon.rigData["info"]["text"])

                self.update()


        if event.button() == QtCore.Qt.MouseButton.LeftButton:

            self.dragAccept = True
            self.dragStartPosition = event.pos()



    def mouseReleaseEvent (self, event):

        self.dragAccept = False

        if event.button() == QtCore.Qt.MouseButton.LeftButton:

            pointer = QtCore.QPoint(
                event.x(),
                event.y())


            RigID = self.rigIcon.rigData["ID"]


            if self.rigIcon.favotireArea.contains(pointer):

                updateGrid = False

                with Settings.UIManager() as uiSettings:


                    if self.rigIcon.hateMode == False:

                        if RigID not in uiSettings["lovelist"]:
                            uiSettings["lovelist"].append(RigID)

                        else:
                            uiSettings["lovelist"].remove(RigID)

                        if uiSettings["lovefilter"]:
                            updateGrid = True

                    else:

                        if RigID not in uiSettings["hatelist"]:
                            uiSettings["hatelist"].append(RigID)

                        updateGrid = True


                if updateGrid:
                    self.applyFilter.emit()



            project   = self.rigIcon.rigData["project"]
            character = self.rigIcon.rigData["character"]

            if self.rigIcon.setArea.contains(pointer):

                 with Settings.LIBManager(update=False) as libSettings:


                    character_data = libSettings["lights"][project]["items"][character]

                    for set_group in character_data["sets"]:

                        if RigID in set_group:

                            with Settings.UIManager() as uiSettings:

                                for set_group_ID in set_group:

                                    if set_group_ID not in uiSettings["setIDs"]:
                                        uiSettings["setIDs"].append(set_group_ID)

                                    else:
                                        uiSettings["setIDs"].remove(set_group_ID)



            if self.rigIcon.previewArea.contains(pointer):
                if not self.info.isVisible():

                    self.clicked.emit(self.rigIcon.rigData)
            

            self.update()



    def leaveEvent (self, event):

        if self.rigName.text():
            self.renameFinish()

        if self.info.isVisible():
            self.saveInfo()

        self.leaveEditor.emit()



    def enterEvent (self, event):

        self.rigName.setVisible(True)
        self.rigName.setGeometry(self.rigIcon.nameArea)

        self.showInfo.emit(self.rigIcon.rigData)



    def keyPressEvent (self, event):
        super(Editor, self).keyPressEvent(event)

        if not self.rigName.text():


            if event.key() == QtCore.Qt.Key_Control:
                self.rigIcon.hateMode = True
                self.update()



    def keyReleaseEvent (self, event):
        super(Editor, self).keyReleaseEvent(event)
        
        if event.key() == QtCore.Qt.Key_Control:
            self.rigIcon.hateMode = False
            self.update()



    def paintEvent (self, event):

        self.rigIcon.paint(
            QtGui.QPainter(self),
            self.rect(),
            self.palette(),
            isEditable=True )



    def renameStart (self, event):

        QtWidgets.QLineEdit.mousePressEvent(self.rigName, event) 

        if self.rigName.cursorPosition() < 1:
            self.rigName.setText(self.rigIcon.rigData["name"])

        self.rigIcon.showName = False
        self.update()



    def renameFinish (self):

        newText = self.rigName.text()
        if newText:

            self.rigIcon.rigData["name"] = newText


            ID        = self.rigIcon.rigData["ID"]

            new_name  = self.rigIcon.rigData["name"]

            project   = self.rigIcon.rigData["project"]
            character = self.rigIcon.rigData["character"]
            tab       = self.rigIcon.rigData["tab"]


            with Settings.LIBManager() as libSettings:

                character_data = libSettings["lights"][project]["items"][character]


                ID_group = None
                for set_group in character_data["sets"]:

                    if ID in set_group:
                        ID_group = set_group


                if ID_group:
                    for tab_name in character_data["tabs"]:
                        for rig in character_data["tabs"][tab_name]:

                            if rig["ID"] in ID_group:
                                rig["name"] = new_name

                else:
                    for rig in character_data["tabs"][tab]:

                            if ID == rig["ID"]:
                                rig["name"] = new_name


                libSettings["lights"][project]["items"][character] = character_data


            self.rigName.clear()
            self.rigName.close()
            self.rigName.setCursorPosition(-1)

            self.reloadTreeItem.emit()

            self.rigIcon.showName = True
            self.update()



    def saveInfo (self):

        infoText = self.info.toPlainText()
        if infoText:

            self.rigIcon.rigData["info"]["text"] = infoText


            ID        = self.rigIcon.rigData["ID"]

            project   = self.rigIcon.rigData["project"]
            character = self.rigIcon.rigData["character"]
            tab       = self.rigIcon.rigData["tab"]


            with Settings.LIBManager() as libSettings:

                character_data = libSettings["lights"][project]["items"][character]

                for rig in character_data["tabs"][tab]:

                        if ID == rig["ID"]:
                            rig["info"]["text"] = infoText


                libSettings["lights"][project]["items"][character] = character_data


            self.info.clear()
            self.info.close()
            self.info.setVisible(False)

            self.reloadTreeItem.emit()

            self.rigIcon.infoMode = False
            self.update()



    def sizeHint (self):

        return self.rigIcon.sizeHint()










class Delegate (QtWidgets.QStyledItemDelegate):


    def __init__ (self, parent):

        super(Delegate, self).__init__(parent)



    def paint (self, painter, option, index):

        rigIcon = Icon()
        rigIcon = self.setIconData(rigIcon, index)

        rigIcon.paint(painter, option.rect, option.palette)



    def sizeHint (self, option, index):

        rigIcon = Icon()
        rigIcon = self.setIconData(rigIcon, index)

        return rigIcon.sizeHint()



    def createEditor (self, parent, option, index):

        editor = Editor(parent)

        editor.index   = index
        editor.option  = option
        editor.rigIcon = self.setIconData(editor.rigIcon, index)

        editor.reloadTreeItem.connect(self.reloadAcion)
        editor.applyFilter.connect(self.filterAcion)

        editor.startDrag.connect(self.dragAcion)
        editor.leaveEditor.connect(self.leaveAcion)

        editor.showInfo.connect(self.infoAction)
        editor.clicked.connect(self.clickAction)

        return editor



    def setModelData (self, editor, model, index):

        model.setData(index, editor.rigIcon.rigData)



    def setIconData (self, icon, index):

        icon.rigData     = index.data()
        icon.previewSize = self.parent().previewSize
        icon.hateMode    = self.parent().hateMode

        return icon



    def editorEvent (self, event, model, option, index):

        if event.type() == QtCore.QEvent.MouseMove:
            if not self.parent().isPersistentEditorOpen(index):
                self.parent().edit(index)

        return True



    def dragAcion (self):

        self.leaveAcion()

        dataBuffer = QtGui.QDrag(self.parent())

        rigData = self.sender().index.data()
        ID = rigData["ID"]

        previewSize = self.parent().previewSize
        rigImage = IconDrag(rigData, previewSize).rigImage

        dragFile = os.path.join( tempfile.gettempdir(), "{}.png".format(ID) )
        rigImage.save(dragFile, "png")

        dragURL = QtCore.QUrl()
        dragURL = dragURL.fromLocalFile(dragFile)

        mimeData = QtCore.QMimeData()
        mimeData.setText(ID)
        mimeData.setImageData(rigImage)
        mimeData.setUrls([dragURL])
        dataBuffer.setMimeData(mimeData)

        dragPreview = QtGui.QPixmap().fromImage(rigImage)
        dataBuffer.setPixmap(dragPreview)
        dataBuffer.setHotSpot(dragPreview.rect().center())

        dataBuffer.exec_(QtCore.Qt.CopyAction)

        os.remove(dragFile)



    def leaveAcion (self):

        self.setModelData(
            self.sender(),
            self.parent().model(),
            self.sender().index )

        self.closeEditor.emit(
            self.sender(),
            QtWidgets.QAbstractItemDelegate.NoHint )

        self.parent().killInfoSignal()



    def reloadAcion (self):

        self.parent().reloadTreeRequest()



    def filterAcion (self):

        self.parent().applyFilterSignal()



    def clickAction (self, rigData):

        self.parent().rigClickedSignal(rigData)



    def infoAction (self, userData):

        self.parent().passInfoSignal(userData)

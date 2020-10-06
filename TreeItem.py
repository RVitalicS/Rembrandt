


from PySide2 import QtWidgets, QtCore, QtGui



import Settings
import icons.resources



UIsettings = Settings.UIsettings









class Delegate (QtWidgets.QStyledItemDelegate):


    def __init__ (self, parent):
        super(Delegate, self).__init__(parent)



    def paint (self, painter, option, index):

        treegData = index.data(QtCore.Qt.UserRole)

        treeType = treegData["type"]
        treeName = treegData["representation"]


        itemArea = option.rect


        offset = UIsettings["tree"]["offsetGroup"]

        opened    = option.state & QtWidgets.QStyle.State_Open
        selected  = option.state & QtWidgets.QStyle.State_Selected
        character = treeType == "character"

        highlightImage = QtGui.QImage(":/Rembrandt/highlight.png")
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if opened or selected and not character:
            painter.fillRect(itemArea, UIsettings["tree"]["colorOpened"])

            transform = QtGui.QTransform()
            transform.rotate(180)
            
            painter.drawImage(
                itemArea,
                highlightImage.transformed(transform),
                highlightImage.rect())


        elif character:
            painter.fillRect(itemArea, UIsettings["tree"]["colorItem"])

            if selected:
                painter.drawImage(
                    itemArea,
                    highlightImage,
                    highlightImage.rect())

            offset = UIsettings["tree"]["offsetItem"]

        else:
            painter.fillRect(itemArea, UIsettings["tree"]["colorGroup"])



        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)

        painter.setPen(
            QtGui.QPen(
                QtGui.QBrush(QtGui.QColor(UIsettings["tree"]["colorText"])),
                0,
                QtGui.Qt.SolidLine,
                QtGui.Qt.RoundCap,
                QtGui.Qt.RoundJoin) )

        font = Settings.makeFont( UIsettings["tree"]["font"] )
        painter.setFont(font)

        textOption = QtGui.QTextOption()
        textOption.setWrapMode(QtGui.QTextOption.NoWrap)
        textOption.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)


        nameArea = QtCore.QRectF(
            itemArea.x() +offset,
            itemArea.y(),
            itemArea.width() -offset,
            itemArea.height())

        painter.drawText(
            nameArea,
            treeName,
            textOption)



        if option.state & QtWidgets.QStyle.State_Selected:

            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

            pointerImage = QtGui.QImage(":/Rembrandt/pointer.png")
            
            pointerHeight = pointerImage.height()
            pointerWidth  = pointerImage.width()

            x = itemArea.width() -pointerImage.width() +itemArea.x() -5
            y = (itemArea.height() -pointerImage.height())/2 +itemArea.y()

            painter.drawImage(QtCore.QPoint(x, y), pointerImage)


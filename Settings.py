

import shutil
import time
import json
import os


from PySide2 import QtGui





this_dir = os.path.dirname(__file__)
user_dir = os.path.expanduser("~")

backup_dir = os.path.join(this_dir, "backup")










class LIB (object):


    def __init__ (self):

        self.path = os.path.join(this_dir, "library.json")



    def load (self):

        with open(self.path, "r") as file:
            return json.load(file)



    def save (self, data):

        self.backup()

        with open(self.path, "w") as file:
            json.dump( data, file, indent=4 )



    def backup (self):

        time_format = "%d%b%I%p%M"
        time_tag = time.strftime(time_format, time.localtime())

        base_name = os.path.basename(self.path)
        name = os.path.splitext(base_name)[0]

        backup_name = "{}.{}.backup".format(name, time_tag)
        backup_path = os.path.join(backup_dir, backup_name)

        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)

        shutil.copy(self.path, backup_path)










class LIBManager (object):


    def __init__ (self, update=True):

        self.update = update


    def __enter__ (self):

        self.data = LIB().load()
        return self.data



    def __exit__ (self, exc_type, exc_val, exc_tb):

        if self.update:
            LIB().save(self.data)










class UI (object):


    def __init__ (self):

        self.default_data = dict(
            itemTree=dict(
                project="",
                character=""),
            iconSize=1,
            lovefilter=False,
            itemTab=0,
            hatelist=[],
            lovelist=[],
            setIDs=[],
            upVector="",
            constraint="")


        self.path = os.path.join(user_dir, "Rembrandt.json")

        if not os.path.exists(self.path):
            self.default_settings(self.path)



    def default_settings (self, path):

        with open(path, "w") as file:
            json.dump( self.default_data, file, indent=4 )



    def load (self):

        with open(self.path, "r") as file:
            return json.load(file)



    def save (self, data):

        with open(self.path, "w") as file:
            json.dump( data, file, indent=4 )









class UIManager (object):


    def __init__ (self, update=True):

        self.update = update


    def __enter__(self):

        self.data = UI().load()
        return self.data



    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.update:
            UI().save(self.data)






fontFamily = ""

UIsettings = dict(

    tree = dict(
        width = 150,
        height = 26,
        offsetGroup=5,
        offsetItem=20,
        colorOpened="#444444",
        colorGroup="#363636",
        colorItem="#2b2b2b",
        colorText="#c8c8c8",
        font = dict(
            size   = 9,
            bold   = False,
            weight = 50,
            family = fontFamily
            )
        ),

    project = dict(
        previewWidth  = 300,
        previewHeight = 450,
        fontLabel = dict(
            size   = 14,
            bold   = True,
            weight = 80,
            family = fontFamily
            ),
        fontInfo = dict(
            size   = 10,
            bold   = False,
            weight = 50,
            family = fontFamily
            )
        ),

    options = dict(
        height  = 70,
        margin  = 8,
        spacing = 3,
        colorBackground = "#141414",
        fontLabel = dict(
            size   = 8,
            bold   = True,
            weight = 90,
            family = fontFamily
            ),
        fontButton = dict(
            size   = 8,
            bold   = False,
            weight = 50,
            family = fontFamily
            )
        ),

    info = dict(
        iconSize      = 12,
        strokeHeight  = 14,
        strokeSpacing = 4,
        labelWidth    = 30,
        colonWidth    = 10,
        baseWidth     = 180,
        commentWidth  = 350,
        fontLabel = dict(
            size   = 8,
            bold   = True,
            weight = 90,
            family = fontFamily
            ),
        fontInfo = dict(
            size   = 8,
            bold   = False,
            weight = 50,
            family = fontFamily
            ),
        fontEdit = dict(
            size   = 8,
            bold   = True,
            weight = 80,
            family = fontFamily
            )
        ),

    icon = dict(
        colorBackground = "#3a3a3a",
        colorHover      = "#505050",
        colorLabel      = "#c8c8c8",
        colorInfo       = "#303030",
        cornerRadius=5,
        infoCommentOffset = 60,
        infoBorderOffset  = 10,
        infoBlockOffset   = 40,
        fontLabel = dict(
            size   = 8,
            bold   = False,
            weight = 50,
            family = fontFamily
            )
        ),

    preview = [
        dict(
            previewSizeX = 256,
            previewSizeY = 128,
            labelSize    = 26,
            gridSpace    = 6),
        dict(
            previewSizeX = 512,
            previewSizeY = 256,
            labelSize    = 26,
            gridSpace    = 6),
        dict(
            previewSizeX = 1024,
            previewSizeY = 512,
            labelSize    = 26,
            gridSpace    = 6),
        ],

    store = dict(
        colorOutlinerSelection = "#5285a6",
        colorTreeWidget        = "#3b3b3b",
        colorListView          = "#2b2b2b",
        colorSliderGroove      = "#373737",
        colorSliderHandle      = "#808080",
        colorRadioButton       = "#505050"
        )

    )









def makeFont (fontSettings):

    font = QtGui.QFont()

    font.setPointSize( fontSettings["size"] )
    font.setBold( fontSettings["bold"] )
    font.setWeight( fontSettings["weight"] )

    if fontSettings["family"]:
        font.setFamily( fontSettings["family"] )

    return font

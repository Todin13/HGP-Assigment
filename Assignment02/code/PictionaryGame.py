# Inspired by PyQt5 Creating Paint Application In 40 Minutes
#  https://www.youtube.com/watch?v=qEgyGyVA1ZQ

# NB If the menus do not work then click on another application and then click back
# and they will work https://python-forum.io/Thread-Tkinter-macOS-Catalina-and-Python-menu-issue

# PyQt documentation links are prefixed with the word 'documentation' in the code below and can be accessed automatically
#  in PyCharm using the following technique https://www.jetbrains.com/help/pycharm/inline-documentation.html

import csv
import random
import sys

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction, QIcon, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QDockWidget,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QColorDialog,
)


class PictionaryGame(QMainWindow):  # documentation https://doc.qt.io/qt-6/qwidget.html
    """
    Painting Application class
    """

    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("Pictionary Game - A2 Template")

        # set the windows dimensions
        top = 400
        left = 400
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        # set the icon
        # windows version
        self.setWindowIcon(
            QIcon("./icons/paint-brush.png")
        )  # documentation: https://doc.qt.io/qt-6/qwidget.html#windowIcon-prop
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))

        # image settings (default)
        self.image = QPixmap(
            "./icons/canvas.png"
        )  # documentation: https://doc.qt.io/qt-6/qpixmap.html
        self.image.fill(
            Qt.GlobalColor.white
        )  # documentation: https://doc.qt.io/qt-6/qpixmap.html#fill
        mainWidget = QWidget()
        mainWidget.setMaximumWidth(300)

        # draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = (
            Qt.GlobalColor.black
        )  # documentation: https://doc.qt.io/qt-6/qt.html#GlobalColor-enum

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()  # documentation: https://doc.qt.io/qt-6/qpoint.html

        # set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(
            " File"
        )  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        brushSizeMenu = mainMenu.addMenu(
            " Brush Size"
        )  # add the "Brush Size" menu to the menu bar
        brushColorMenu = mainMenu.addMenu(
            " Brush Colour"
        )  # add the "Brush Colour" menu to the menu bar

        helpButton = mainMenu.addAction(" ? ")  # adding help button to menu bar adding space as it's the style of the bar

        # help button action
        self.helpMessage = (
            f"<b>Welcome to Pictionary Game!</b><br><br>"
            f"<b>Instructions:</b><br>"
            f"- Use the left mouse button to draw on the canvas.<br>"
            f"- Select brush size and color from the menu.<br>"
            f"- Save your drawing by selecting 'Save' (Ctrl+S).<br>"
            f"- Clear the canvas by selecting 'Clear' (Ctrl+C).<br><br>"
            f"<b>Shortcuts:</b><br>"
            f"- Change brush size: 3px (Ctrl+3), 5px (Ctrl+5), 7px (Ctrl+7), 9px (Ctrl+9).<br>"
            f"- Change color: Black (Ctrl+B), Red (Ctrl+R), Green (Ctrl+G), Yellow (Ctrl+Y) or use the Palette to choose another one (Ctrl+P).<br>"
            f"- Clear the canvas: (Ctrl+C) <br>"
            f"- Save the canvas: (Ctrl+S) <br><br>"
            f"<b>Game Information:</b><br>"
            f"- Each player takes turns drawing a word.<br>"
            f"- Words are randomly selected from an external file based on difficulty.<br>"
            f"- Check the left sidebar for current turn and player scores.<br>"
            f"<br><i>Enjoy playing!</i>"
        )# Define help text
        helpButton.triggered.connect(self.helpMessageBox) # Connecting to the help message pop up window when click on " help" button

        # save menu item
        saveAction = QAction(
            QIcon("./icons/save.png"), "Save", self
        )  # create a save action with a png as an icon, documentation: https://doc.qt.io/qt-6/qaction.html
        saveAction.setShortcut(
            "Ctrl+S"
        )  # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-6/qaction.html#shortcut-prop
        fileMenu.addAction(
            saveAction
        )  # add the save action to the file menu, documentation: https://doc.qt.io/qt-6/qwidget.html#addAction
        saveAction.triggered.connect(
            self.save
        )  # when the menu option is selected or the shortcut is used the save slot is triggered, documentation: https://doc.qt.io/qt-6/qaction.html#triggered

        # clear
        clearAction = QAction(
            QIcon("./icons/clear.png"), "Clear", self
        )  # create a clear action with a png as an icon
        clearAction.setShortcut(
            "Ctrl+C"
        )  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(
            self.clear
        )  # when the menu option is selected or the shortcut is used the clear slot is triggered

        # brush thickness
        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")
        brushSizeMenu.addAction(
            threepxAction
        )  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        blackAction = QAction(QIcon("./icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColorMenu.addAction(blackAction)
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("./icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColorMenu.addAction(redAction)
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("./icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColorMenu.addAction(greenAction)
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColorMenu.addAction(yellowAction)
        yellowAction.triggered.connect(self.yellow)

        # Action for the color picker to the Brush Colour menu
        colorPickerAction = QAction(QIcon("./icons/color-picker.png"), "Choose Color", self)
        colorPickerAction.setShortcut("Ctrl+P")
        brushColorMenu.addAction(colorPickerAction)
        colorPickerAction.triggered.connect(self.openColorPicker)

        # Side Dock
        self.dockInfo = QDockWidget()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockInfo)

        # widget inside the Dock
        playerInfo = QWidget()
        self.vbdock = QVBoxLayout()
        playerInfo.setLayout(self.vbdock)
        playerInfo.setMaximumSize(100, self.height())
        # add controls to custom widget
        self.vbdock.addWidget(QLabel("Current Turn: -"))
        self.vbdock.addSpacing(20)
        self.vbdock.addWidget(QLabel("Scores:"))
        self.vbdock.addWidget(QLabel("Player 1: -"))
        self.vbdock.addWidget(QLabel("Player 2: -"))
        self.vbdock.addStretch(1)
        self.vbdock.addWidget(QPushButton("Button"))

        # Setting colour of dock to gray
        playerInfo.setAutoFillBackground(True)
        p = playerInfo.palette()
        p.setColor(playerInfo.backgroundRole(), Qt.GlobalColor.gray)
        playerInfo.setPalette(p)

        # set widget for dock
        self.dockInfo.setWidget(playerInfo)

        self.getList("easy")
        self.currentWord = self.getWord()

    # event handlers
    def mousePressEvent(
        self, event
    ):  # when the mouse is pressed, documentation: https://doc.qt.io/qt-6/qwidget.html#mousePressEvent
        if (
            event.button() == Qt.MouseButton.LeftButton
        ):  # if the pressed button is the left button
            self.drawing = True  # enter drawing mode
            self.lastPoint = (
                event.pos()
            )  # save the location of the mouse press as the lastPoint
            print(self.lastPoint)  # print the lastPoint for debugging purposes

    def mouseMoveEvent(
        self, event
    ):  # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-6/qwidget.html#mouseMoveEvent
        if self.drawing:
            painter = QPainter(
                self.image
            )  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-6/qpen.html
            painter.setPen(
                QPen(
                    self.brushColor,
                    self.brushSize,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
                )
            )
            painter.drawLine(
                self.lastPoint, event.pos()
            )  # draw a line from the point of the orginal press to the point to where the mouse was dragged to
            self.lastPoint = (
                event.pos()
            )  # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()  # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(
        self, event
    ):  # when the mouse is released, documentation: https://doc.qt.io/qt-6/qwidget.html#mouseReleaseEvent
        if (
            event.button() == Qt.MouseButton.LeftButton
        ):  # if the released button is the left button, documentation: https://doc.qt.io/qt-6/qt.html#MouseButton-enum ,
            self.drawing = False  # exit drawing mode

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(
            self
        )  # create a new QPainter object, documentation: https://doc.qt.io/qt-6/qpainter.html
        canvasPainter.drawPixmap(
            QPoint(), self.image
        )  # draw the image , documentation: https://doc.qt.io/qt-6/qpainter.html#drawImage-1

    # resize event - this function is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())


    def helpMessageBox(self):
        """
        Creating the Help message pop up window
        """
        QMessageBox.information(self, " Help", self.helpMessage) 

    def openColorPicker(self):
        """
        Open a color dialog and get the selected color
        """
        color = QColorDialog.getColor()  # Open a color dialog to choose a color
        
        if color.isValid():  # if the color is valid, set it 
            self.changeBrushColor(color)

    def changeBrushColor(self, color):
        """
        Change the brush color to the selected color from QColorDialog.
        """
        self.brushColor = color

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)"
        )
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.image.save(filePath)  # save file image to the file path

    def clear(self):
        self.image.fill(
            Qt.GlobalColor.white
        )  # fill the image with white, documentation: https://doc.qt.io/qt-6/qimage.html#fill-2
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    def threepx(self):  # the brush size is set to 3
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):  # the brush color is set to black
        self.brushColor = Qt.GlobalColor.black

    def red(self):
        self.brushColor = Qt.GlobalColor.red

    def green(self):
        self.brushColor = Qt.GlobalColor.green

    def yellow(self):
        self.brushColor = Qt.GlobalColor.yellow

    # Get a random word from the list read from file
    def getWord(self):
        randomWord = random.choice(self.wordList)
        print(randomWord)
        return randomWord

    # read word list from file
    def getList(self, mode):
        with open(mode + "mode.txt") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                # print(row)
                self.wordList = row
                line_count += 1
            # print(f'Processed {line_count} lines.')

    # open a file
    def open(self):
        """
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file dialog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        """
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)"
        )
        if filePath == "":  # if not file is selected exit
            return
        with open(filePath, "rb") as f:  # open the file in binary mode for reading
            content = f.read()  # read the file
        self.image.loadFromData(content)  # load the data into the file
        width = self.width()  # get the width of the current QImage in your application
        height = (
            self.height()
        )  # get the height of the current QImage in your application
        self.image = self.image.scaled(
            width, height
        )  # scale the image from file and put it in your QImage
        self.update()  # call the update method of the widget which calls the paintEvent of this class


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PictionaryGame()
    window.show()
    app.exec()  # start the event loop running

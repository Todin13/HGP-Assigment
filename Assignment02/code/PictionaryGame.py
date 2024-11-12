# Inspired by PyQt5 Creating Paint Application In 40 Minutes
#  https://www.youtube.com/watch?v=qEgyGyVA1ZQ

# NB If the menus do not work then click on another application and then click back
# and they will work https://python-forum.io/Thread-Tkinter-macOS-Catalina-and-Python-menu-issue

# PyQt documentation links are prefixed with the word 'documentation' in the code below and can be accessed automatically
#  in PyCharm using the following technique https://www.jetbrains.com/help/pycharm/inline-documentation.html

import csv
import random
import sys

from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtGui import QAction, QIcon, QPainter, QPen, QPixmap, QPalette, QColor
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
    QSpinBox,
    QDialog,
    QComboBox,
    QFormLayout,
    QDialogButtonBox,
    QGridLayout,
    QLineEdit,
    QHBoxLayout
)


class PictionaryGame(QMainWindow):  # documentation https://doc.qt.io/qt-6/qwidget.html
    """
    Painting Application class
    """

    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("Pictionary Game")

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

        # image settings (default)
        self.image = QPixmap(
            "./icons/canvas.png"
        )  # documentation: https://doc.qt.io/qt-6/qpixmap.html
        self.image.fill(
            Qt.GlobalColor.white
        )  # documentation: https://doc.qt.io/qt-6/qpixmap.html#fill
        mainWidget = QWidget()
        mainWidget.setMaximumWidth(300)

        # init game state, stop state and answer state
        self.game = False
        self.stop = False
        self.answerState = False

        # draw settings (default)
        self.allowDrawing = True  # usefull for when the game started
        self.drawing = False
        self.brushSize = 3
        self.brushStyle = Qt.PenStyle.SolidLine
        self.capStyle = Qt.PenCapStyle.RoundCap
        self.joinStyle = Qt.PenJoinStyle.RoundJoin
        self.brushColor = (
            Qt.GlobalColor.black
        )  # documentation: https://doc.qt.io/qt-6/qt.html#GlobalColor-enum
        self.isEraserActive = False  # Track if the eraser is active

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()  # documentation: https://doc.qt.io/qt-6/qpoint.html

        # Initialize default game settings
        self.draw_time_limit = 30  # Default draw time in seconds
        self.answer_time_limit = 10  # Default answer time in seconds
        self.rounds = 5  # Default number of rounds
        self.difficulty = "easy"  # Default word list difficulty

        # Init the score and round
        self.score = [0, 0]
        self.round_id = 0

        # set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(
            " File "
        )  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac

        # Add Eraser option
        eraserAction = QAction(QIcon("./icons/eraser.png"), "", self)
        eraserAction.setShortcut("Ctrl+E")
        mainMenu.addAction(eraserAction)
        eraserAction.triggered.connect(self.activateEraser)
        eraserAction.setShortcut("Ctrl+E")  # set shortcut for earser

        # Restore Brush option
        restoreBrushAction = QAction(QIcon("./icons/pen.png"), "", self)
        restoreBrushAction.setShortcut("Ctrl+R")
        mainMenu.addAction(restoreBrushAction)
        restoreBrushAction.triggered.connect(self.restoreBrush)
        restoreBrushAction.setShortcut("Ctrl+R")  # set shortcut for  restor brush

        brushSizeMenu = mainMenu.addMenu(
            " Brush Size "
        )  # add the "Brush Size" menu to the menu bar
        brushColorMenu = mainMenu.addMenu(
            " Brush Colour "
        )  # add the "Brush Colour" menu to the menu barself.capStyle, self.joinStyle
        brushStyleMenu = mainMenu.addMenu(" Brush Style ")  # adding brush style menu
        game_setting_menu = mainMenu.addAction(
            " Game Setting "
        )  # add " Game Setting" menu to the menu bar

        helpMenu = mainMenu.addMenu(
            " ? "
        )  # adding help menu to menu bar adding space as it's the style of the bar

        # Connecting the button game setting to the setting window
        game_setting_menu.triggered.connect(self.update_game_setting)

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

        # open
        openAction = QAction(
            QIcon("./icons/folder.png"), "Open", self
        )  # create an open action to open file
        openAction.setShortcut(
            "Ctrl+O"
        )  # connect the open action to a keyboard shortcut
        fileMenu.addAction(openAction)  # add this action to the file menu
        openAction.triggered.connect(
            self.open
        )  # when the menu option is selected or the shortcut is used the open slot is triggered

        # brush thickness
        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")
        brushSizeMenu.addAction(
            threepxAction
        )  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction("5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction("7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction("9px", self)
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

        # adding blue as it's a primmary color
        blueAction = QAction(QIcon("./icons/blue.png"), "Blue", self)
        blueAction.setShortcut("Ctrl+U")
        brushColorMenu.addAction(blueAction)
        blueAction.triggered.connect(self.blue)

        # Action for the color picker to the Brush Colour menu
        colorPickerAction = QAction(
            QIcon("./icons/color-wheel.png"), "Choose Color", self
        )
        colorPickerAction.setShortcut("Ctrl+P")
        brushColorMenu.addAction(colorPickerAction)
        colorPickerAction.triggered.connect(self.openColorPicker)

        lineStyleMenu = brushStyleMenu.addMenu(
            " Line Style "
        )  # add the Brush Style menu
        capStyleMenu = brushStyleMenu.addMenu(" Cap Style ")  # add the Cap Style menu
        joinStyleMenu = brushStyleMenu.addMenu(
            " Join Style "
        )  # add the Join Style menu

        # Brush style
        solidAction = QAction("Solid", self)
        solidAction.triggered.connect(self.setSolidStyle)
        lineStyleMenu.addAction(solidAction)

        dashedAction = QAction("Dashed", self)
        dashedAction.triggered.connect(self.setDashedStyle)
        lineStyleMenu.addAction(dashedAction)

        dottedAction = QAction("Dotted", self)
        dottedAction.triggered.connect(self.setDottedStyle)
        lineStyleMenu.addAction(dottedAction)

        roundCapAction = QAction("Round Cap", self)
        roundCapAction.triggered.connect(self.setRoundCap)
        capStyleMenu.addAction(roundCapAction)

        squareCapAction = QAction("Square Cap", self)
        squareCapAction.triggered.connect(self.setSquareCap)
        capStyleMenu.addAction(squareCapAction)

        flatCapAction = QAction("Flat Cap", self)
        flatCapAction.triggered.connect(self.setFlatCap)
        capStyleMenu.addAction(flatCapAction)

        roundJoinAction = QAction("Round Join", self)
        roundJoinAction.triggered.connect(self.setRoundJoin)
        joinStyleMenu.addAction(roundJoinAction)

        bevelJoinAction = QAction("Bevel Join", self)
        bevelJoinAction.triggered.connect(self.setBevelJoin)
        joinStyleMenu.addAction(bevelJoinAction)

        miterJoinAction = QAction("Miter Join", self)
        miterJoinAction.triggered.connect(self.setMiterJoin)
        joinStyleMenu.addAction(miterJoinAction)

        # Help menu
        # help menu buttons action
        # Define help text
        helpMessageAbout = (
            f"<b>Welcome to Pictionary Game!</b><br><br>"
            f"<b>Instructions:</b><br>"
            f"- Use the left mouse button to draw on the canvas.<br>"
            f"- Use the eraser (Ctrl+E) to erase parts of your drawing.<br>"
            f"- Select brush size, style, and color from the menu.<br>"
            f"- Save your drawing by selecting 'Save' (Ctrl+S).<br>"
            f"- Clear the canvas by selecting 'Clear' (Ctrl+C).<br>"
            f"- Open a new canvas by selecting 'Open' (Ctrl+O).<br>"
            f"- Customize game settings in the 'Game Setting' menu.<br>"
            f"- Start the game by clicing on the start button on bottom right.<br>"
            f"- You can stop the game by clicking on the stop button, the game will stop at the end of the round.<br><br>"
            f"<br><i>Enjoy playing!</i>"
        )

        helpMessageShortcut = (
            f"<b>Welcome to Pictionary Game!</b><br><br>"
            f"<b>Shortcuts:</b><br>"
            f"- Change brush size: 3px (Ctrl+3), 5px (Ctrl+5), 7px (Ctrl+7), 9px (Ctrl+9).<br>"
            f"- Change color: Black (Ctrl+B), Red (Ctrl+R), Green (Ctrl+G), Yellow (Ctrl+Y), Blue (Ctrl+U)"
            f"or choose from the color palette (Ctrl+P).<br>"
            f"- Use the eraser tool: (Ctrl+E) <br>"
            f"- Restore brush after erasing: (Ctrl+R) <br>"
            f"- Clear the canvas: (Ctrl+C) <br>"
            f"- Save the canvas: (Ctrl+S) <br><br>"
            f"<br><i>Enjoy playing!</i>"
        )

        helpMessageGame = (
            f"<b>Welcome to Pictionary Game!</b><br><br>"
            f"<b>Game Settings:</b><br>"
            f"- Customize game settings in the 'Game Setting' menu.<br>"
            f"- Default settings: 30 seconds for drawing, 10 seconds for guessing, 5 rounds, and 'Easy' difficulty.<br><br>"
            f"<b>Game Information:</b><br>"
            f"- Players take turns to draw randomly selected words.<br>"
            f"- Check the left sidebar for the current turn, player scores, and round number.<br>"
            f"- The timer displays the remaining time for each turn, when it stop you can't draw anymore or can't answer.<br>"
            f"- Click on the ster button to start the game.<br>"
            f"- Click on stop to stop at the end of the actual round.<br><br>"
            f"<br><i>Enjoy playing!</i>"
        )

        # add about button to help menu
        helpaboutButton = QAction(" About ", self)
        helpaboutButton.triggered.connect(lambda: self.helpMessageBox(" About ", helpMessageAbout))
        helpMenu.addAction(helpaboutButton)

        # add Shortcuts button to help menu
        helpShortcutButton = QAction(" Shortcuts ", self)
        helpShortcutButton.triggered.connect(lambda:self.helpMessageBox(" Shortcuts ", helpMessageShortcut))
        helpMenu.addAction(helpShortcutButton)

        # add game info button to help menu
        helpGameButton = QAction(" Game Info ", self)
        helpGameButton.triggered.connect(lambda:self.helpMessageBox(" Game Info ", helpMessageGame))
        helpMenu.addAction(helpGameButton)
        

        # Side Dock, putting the dock and playInfo into class property to modify the label of playerInfo and modify the dockInfo size when resizing the image
        self.dockInfo = QDockWidget()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockInfo)

        # widget inside the Dock
        self.playerInfo = QWidget()
        self.vbdock = QVBoxLayout()
        self.playerInfo.setLayout(self.vbdock)
        self.playerInfo.setMaximumSize(150, self.height())
        # add controls to custom widget
        # init label
        self.turn_label = QLabel("Current Turn: -")
        self.round_label = QLabel("Current Round: -")
        self.player1_label = QLabel("Player 1: -")
        self.player2_label = QLabel("Player 2: -")
        self.timer_label = QLabel("Time Left: -")

        self.vbdock.addWidget(self.round_label)
        self.vbdock.addWidget(self.turn_label)
        self.vbdock.addSpacing(20)
        self.vbdock.addWidget(QLabel("Scores:"))
        self.vbdock.addWidget(self.player1_label)
        self.vbdock.addWidget(self.player2_label)
        self.vbdock.addSpacing(20)
        self.vbdock.addWidget(QLabel("Timer:"))
        self.vbdock.addWidget(self.timer_label)

        self.vbdock.addStretch(1)

        # create the starting button
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.play)
        self.vbdock.addWidget(start_button)

        # Create the next turn button
        self.next_turn_button = QPushButton("Next Turn", self)
        self.next_turn_button.clicked.connect(self.next_turn)
        self.vbdock.addWidget(self.next_turn_button) 

        # create the stop button
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_action)
        self.vbdock.addWidget(self.stop_button) 

        # Update the dock's background color by making it gray, and text black 
        self.playerInfo.setAutoFillBackground(True)
        palette = self.playerInfo.palette()
        palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.gray)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Button, Qt.GlobalColor.gray)
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)

        # Setting the palette to the element were there is text
        self.playerInfo.setPalette(palette)
        self.dockInfo.setPalette(palette)
        mainMenu.setPalette(palette) 

        # Set widget for dock
        self.dockInfo.setWidget(self.playerInfo)
        # Self.dockInfo.setAutoFillBackground(True) # drawing not updated on real time need to open another children window and close it

        # Initialize the current word list
        self.getList(self.difficulty)
        self.currentWord = self.getWord()

        # Init timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

    # Event handlers
    def mousePressEvent(
        self, event
    ):  # When the mouse is pressed, documentation: https://doc.qt.io/qt-6/qwidget.html#mousePressEvent
        if (
            event.button() == Qt.MouseButton.LeftButton
        ):  # If the pressed button is the left button
            self.drawing = True  # Enter drawing mode
            self.lastPoint = (
                event.pos()
            )  # Save the location of the mouse press as the lastPoint
            print(self.lastPoint)  # Print the lastPoint for debugging purposes

    def mouseMoveEvent(
        self, event
    ):  # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-6/qwidget.html#mouseMoveEvent
        if self.drawing & self.allowDrawing:

            painter = QPainter(
                self.image
            )  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-6/qpen.html

            # Set eraser mode if eraser is active
            if self.isEraserActive:
                # Eraser mode
                painter.setPen(
                    QPen(Qt.GlobalColor.white, self.brushSize, Qt.PenStyle.SolidLine)
                )
            else:
                # Normal drawing mode
                painter.setPen(
                    QPen(
                        self.brushColor,
                        self.brushSize,
                        self.brushStyle,
                        self.capStyle,
                        self.joinStyle,
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
        self.playerInfo.setMaximumSize(150, self.height())
        super().resizeEvent(event)

    def helpMessageBox(self, about, message):
        """
        Creating the Help message pop up window
        """
        QMessageBox.information(self, about, message)

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

    # Functions to change brush style
    def setSolidStyle(self):
        self.brushStyle = Qt.PenStyle.SolidLine

    def setDashedStyle(self):
        self.brushStyle = Qt.PenStyle.DashLine

    def setDottedStyle(self):
        self.brushStyle = Qt.PenStyle.DotLine

    # Functions to set Cap Styles
    def setRoundCap(self):
        self.capStyle = Qt.PenCapStyle.RoundCap

    def setSquareCap(self):
        self.capStyle = Qt.PenCapStyle.SquareCap

    def setFlatCap(self):
        self.capStyle = Qt.PenCapStyle.FlatCap

    # Functions to set Join Styles
    def setRoundJoin(self):
        self.joinStyle = Qt.PenJoinStyle.RoundJoin

    def setBevelJoin(self):
        self.joinStyle = Qt.PenJoinStyle.BevelJoin

    def setMiterJoin(self):
        self.joinStyle = Qt.PenJoinStyle.MiterJoin

    # Function to activate the eraser
    def activateEraser(self):
        self.isEraserActive = True

    # Function to activate brush
    def restoreBrush(self):
        self.isEraserActive = False

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)"
        )
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        end = ".png" if filePath[:-4] != ".png" else ""
        self.image.save(filePath + end)  # save file image to the file path

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

    def blue(self):
        self.brushColor = Qt.GlobalColor.blue

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

    def update_game_setting(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Game Settings")

        # Time limit (seconds per round)
        draw_time_spinbox = QSpinBox()
        draw_time_spinbox.setRange(0, 300)
        draw_time_spinbox.setValue(self.draw_time_limit)
        answer_time_spinbox = QSpinBox()
        answer_time_spinbox.setRange(0, 300)
        answer_time_spinbox.setValue(self.answer_time_limit)

        # Number of rounds
        rounds_spinbox = QSpinBox()
        rounds_spinbox.setRange(1, 20)
        rounds_spinbox.setValue(self.rounds)

        # Difficulty level
        difficulty_combo = QComboBox()
        difficulty_combo.addItems(["easy", "hard"])
        difficulty_combo.setCurrentText(self.difficulty)

        # Layout for settings dialog
        form_layout = QFormLayout()
        form_layout.addRow("Time to draw per round (s):", draw_time_spinbox)
        form_layout.addRow("Time to answer per round (s):", answer_time_spinbox)
        form_layout.addRow("Number of rounds:", rounds_spinbox)
        form_layout.addRow("Difficulty:", difficulty_combo)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        layout = QVBoxLayout(dialog)
        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        # Show dialog and update settings if accepted
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.answer_time_limit = answer_time_spinbox.value()
            self.draw_time_limit = draw_time_spinbox.value()
            self.rounds = rounds_spinbox.value()
            self.difficulty = difficulty_combo.currentText()
            self.getList(self.difficulty)
            self.currentWord = self.getWord()

    def show_word(self):
        # Create a dialog to show the current word
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Round {self.round_id}")

        # Set the size of the dialog
        dialog.setFixedSize(300, 150)

        # Create a grid layout for the dialog
        grid_layout = QGridLayout(dialog)

        # Display player turn (centered)
        turn = QLabel(f"Player {self.draw_turn + 1} turn to draw")
        turn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(turn, 0, 0, 1, 2)

        # Create button to show the word
        button = QPushButton("Show word")
        button.setStyleSheet("text-align: center;")
        word = QLabel(f"The word is: {self.currentWord}")
        word.setVisible(False)

        # Toggle word visibility when button is clicked
        button.clicked.connect(lambda: word.setVisible(not word.isVisible()))
        grid_layout.addWidget(button, 1, 0)

        # Separation line (centered)
        separation = QLabel(f"------------------------------------------")
        separation.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(separation, 2, 0, 1, 2)

        # The word label (centered)
        word.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(word, 3, 0, 1, 2)

        # Create Close button (placed next to "Show word" button)
        close_button = QPushButton("Ok")
        close_button.setStyleSheet("text-align: center;")
        close_button.clicked.connect(dialog.accept)

        # Add the Close button to the grid layout
        grid_layout.addWidget(close_button, 1, 1)

        # Set margins and spacing for the grid layout
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(10)

        # Set a timer to automatically close the dialog after a limit time
        drawing_timer = QTimer(self)
        drawing_timer.setSingleShot(True)  # Run only once
        drawing_timer.timeout.connect(
            dialog.accept
        )  # Close the dialog when the timer ends
        drawing_timer.start(self.draw_time_limit * 1000)  # Set drawing time limit

        # Show the dialog
        dialog.show()

    def answer_window(self):
        # Create a dialog for answering the word
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Round {self.round_id} - Answer")

        # Set the size of the dialog
        dialog.setFixedSize(300, 200)

        # Create a grid layout for the dialog
        grid_layout = QGridLayout(dialog)

        # Display player turn (centered)
        turn = QLabel(f"Player {self.answer_turn + 1} turn to answer")
        turn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(turn, 0, 0, 1, 2)

        # Label asking for the answer (centered)
        answer_prompt = QLabel("Enter your answer:")
        answer_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(answer_prompt, 1, 0, 1, 2)

        # Text field for answer input
        answer_input = QLineEdit()
        answer_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(answer_input, 2, 0, 1, 2)

        # Create a button to submit the answer
        submit_button = QPushButton("Submit Answer")
        submit_button.setStyleSheet("text-align: center;")
        submit_button.clicked.connect(
            lambda: self.submit_answer(answer_input.text(), dialog)
        )
        grid_layout.addWidget(submit_button, 4, 0, 1, 2)

        # Set margins and spacing for the grid layout
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(10)

        # Set a timer to automatically close the dialog after a limit time
        answer_timer = QTimer(self)
        answer_timer.setSingleShot(True)  # Run only once
        answer_timer.timeout.connect(
            dialog.accept
        )  # Close the dialog when the timer ends
        answer_timer.start(self.answer_time_limit * 1000)  # Set answering time limit

        # Set answerState to False when the dialog is closed
        dialog.finished.connect(self.setAnswerStateOnClose)

        # Show the dialog
        dialog.show()

    def setAnswerStateOnClose(self):
        self.answerState = False

    def submit_answer(self, answer, dialog):
        # Logic to handle the submitted answer
        if answer.lower() == self.currentWord.lower():
            QMessageBox.information(self, "Correct!", "You guessed the word!")
            # add two point to the drawer and one to the finder
            self.score[self.answer_turn] += 1
            self.score[self.draw_turn] += 2
            dialog.accept() # close window to avoid cheating by answering right again
            self.update_points() # update points
        else:
            QMessageBox.warning(self, "Incorrect", "Try again!")

    def update_points(self):
        self.turn_label.setText(f"Current Turn: {self.draw_turn + 1}")
        self.round_label.setText(f"Current Round: {self.round_id}")
        self.player1_label.setText(f"Player 1: {self.score[0]}")
        self.player2_label.setText(f"Player 2: {self.score[1]}")

    def start_timer(self, seconds):
        # Initialize the timer for a new turn
        self.time_left = seconds
        self.update_timer_display()
        self.timer.start(1000)  # Update every 1000 ms = 1 second

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_display()
        else:
            self.timer.stop()
            self.timer_label.setText("Time's up!")

    def reset_timer(self):
        self.timer_label.setText(f"Time Left: -")

    def update_timer_display(self):
        # Display the time in MM:SS format
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.setText(f"Time Left: {minutes:02}:{seconds:02}")

    def reset_points(self):
        self.turn_label.setText("Current Turn: -")
        self.round_label.setText("Current Round: -")
        self.player1_label.setText("Player 1: -")
        self.player2_label.setText("Player 2: -")

    def whoIsWinning(self):
        """
        Create a new window to show the results of the game
        """

        # Determine the winner based on scores
        if self.score[0] > self.score[1]:
            winner_text = "Player 1 wins!"
        elif self.score[1] > self.score[0]:
            winner_text = "Player 2 wins!"
        else:
            winner_text = "It's a tie!"

        # Create a dialog to display the winner
        dialog = QDialog(self)
        dialog.setWindowTitle("Game Over")

        # Set dialog size
        dialog.setFixedSize(250, 150)

        # Create a vertical layout for the dialog
        layout = QVBoxLayout(dialog)

        # Winner label
        winner_label = QLabel(winner_text)
        winner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(winner_label)

        # Display the final scores
        score_label = QLabel(
            f"Final Scores:\nPlayer 1: {self.score[0]}\nPlayer 2: {self.score[1]}"
        )
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(score_label)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        # Show the dialog
        dialog.show()

    def answer(self):
        # setting answerState to true as we answer
        self.answerState = True

        # do not permit drawing when answering
        self.allowDrawing = False

        # start timer and show answer window
        self.start_timer(self.answer_time_limit)
        self.answer_window()

    def turn(self):
        # clear the canvas
        self.clear()

        # Get a new word for the turn
        self.currentWord = self.getWord()

        # permit drawing
        self.allowDrawing = True

        # start timer and show word
        self.start_timer(self.draw_time_limit)
        self.show_word()

        # show answer window after end of drawing
        self.answer_timer.start(self.draw_time_limit * 1000)

    def swap_turn(self):
        self.draw_turn, self.answer_turn = self.answer_turn, self.draw_turn

    def end_round(self):
        # swap turn and increase round id
        self.swap_turn()
        self.round_id += 1

        if self.round_id > self.rounds:
            # stopping timer and reseting the game state info
            self.timer.stop()
            self.reset_timer()
            self.reset_points()
            self.whoIsWinning()
            # allowing drawing and resetting the game and stop state
            self.allowDrawing = True
            self.game = False
            self.stop = True
        else:
            self.update_points()
            self.round()

    def round(self):
        if self.draw_turn == 0:
            # turn 1
            self.turn()

            # swap turn and update
            self.swap_turn_timer.start((self.draw_time_limit + self.answer_time_limit + 1) * 1000)
            self.update_points_timer.start((self.draw_time_limit + self.answer_time_limit + 1) * 1000)
            
            # turn 2 after changing player roles
            self.turn_timer.start((self.draw_time_limit + self.answer_time_limit + 1) * 1000)

            # show next_round window after end of round
            self.end_round_timer.start((self.draw_time_limit + self.answer_time_limit + 1) * 2000)

        elif self.draw_turn == 1:
            # turn 2
            self.turn()
            self.end_round_timer.start((self.draw_time_limit + self.answer_time_limit + 1) * 1000)

        else:
            # Raise an error if the draw_turn number is invalid
            raise ValueError(f"Invalid draw number: {self.draw_turn}. The draw number should be 0 or 1.")


    def initTimer(self):
        # init timer to stop them when skipping turn
        self.answer_timer = QTimer(self)
        self.answer_timer.timeout.connect(self.answer)
        self.answer_timer.setSingleShot(True)

        self.swap_turn_timer = QTimer(self)
        self.swap_turn_timer.timeout.connect(self.swap_turn)
        self.swap_turn_timer.setSingleShot(True)

        self.update_points_timer = QTimer(self)
        self.update_points_timer.timeout.connect(self.update_points)
        self.update_points_timer.setSingleShot(True)

        self.turn_timer = QTimer(self)
        self.turn_timer.timeout.connect(self.turn)
        self.turn_timer.setSingleShot(True)

        self.end_round_timer = QTimer(self)
        self.end_round_timer.timeout.connect(self.end_round)
        self.end_round_timer.setSingleShot(True)

    def stopTimer(self):
        # stop all the timer 
        self.answer_timer.stop()
        self.swap_turn_timer.stop()
        self.update_points_timer.stop()
        self.turn_timer.stop()
        self.end_round_timer.stop()
        self.timer.stop()

    def play(self):

        if self.game:
            QMessageBox.information(self, " Start Game ", "There is an ongoing game stop it to start a new one. ")

        else:
            # Confirm starting a new game
            reply = QMessageBox.question(
                self,
                "Start Game",
                "Are you ready to start the game?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:

                # setting game state to true
                self.game = True

                # setting the drawing state to false
                self.allowDrawing = False

                # Reset scores and start a new game
                self.score = [0, 0]
                self.round_id = 1
                self.draw_turn = 0
                self.answer_turn = 1
                self.update_points()

                # init the timer and start first round
                self.initTimer()
                self.round()

            else:
                QMessageBox.information(self, "Game", "Game start cancelled.")

    def stop_action(self):
        # Show confirmation dialog
        if self.game:
            if not self.stop:
                reply = QMessageBox.question(
                    self,
                    "Confirm Stop",
                    "Are you sure you want to stop the game at the end of this round?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )

                # If the user clicks "Yes", set rounds to current round to stop the game at the end of the round
                if reply == QMessageBox.StandardButton.Yes:
                    self.rounds = self.round_id
                    self.stop = True
        else: 
            QMessageBox.information(self, " Stop Game ", "There is no ongoing game, cannot stop it. ")

    def next_turn(self):
        if self.game and not self.answerState:
            self.stopTimer()

            # if draw turn is player 1 swap turn the update the points and restart round process
            if self.draw_turn == 0:
                self.swap_turn()
                self.update_points()
                self.round()

            # if draw turn is player 2 go to end round which will swap player turns and add 1 to round 
            elif self.draw_turn == 1:
                self.end_round() 

            # Raise an error if the draw_turn number is invalid
            else:
                 raise ValueError(f"Invalid draw number: {self.draw_turn}. The draw number should be 0 or 1.")

        elif self.answerState:
            QMessageBox.information(self, " Next Turn ", "Finish answering before skiping turn.")

        else:
            QMessageBox.information(self, " Next Turn ", "There is no ongoing game, cannot skip turn.")

# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PictionaryGame()
    window.show()
    app.exec()  # start the event loop running

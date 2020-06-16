#!/usr/bin/python3

import sys
import random
import time
from enum import Enum

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Status(Enum):
    IDLE = 0
    TYPING = 1
    ANSWER = 2
    GAME_OVER = 3

class CalculMentalWin(QMainWindow):

    def __init__(self, res_min, res_max, score_max, *args, **kwargs):

        super(CalculMentalWin, self).__init__(*args, **kwargs)

        # Initial Result Range
        self.res_min = res_min
        self.res_max = res_max

        # Initial Q & A Status
        self.status = Status.IDLE

        # Question
        self.result = -1
        self.nb1 = -1
        self.nb2 = -1

        # User's answer
        self.answer = ''

        # In-game time
        self.startTime = -1
        self.finalTime = -1

        # Score
        self.score_max = score_max
        self.score = 0

        self.initialize_gui()

    def initialize_gui(self):

        self.setWindowTitle(f'Calcul Mental - Results between {self.res_min} and {self.res_max}')

        # Initial Window Size
        self.WIDTH = 1200
        self.HEIGHT = 920

        # Default Fonts
        self.FONT = QFont('Arial', 128, QFont.Bold)
        self.COLOR_TYPING = "color: darkgray"
        self.COLOR_CORRECT = "color: rgb(0,180,0)"
        self.COLOR_INCORRECT = "color: rgb(255,0,0)"
        self.COLOR_END = "color: rgb(180,180,0)"

        self.STATUS_FONT = QFont('Arial', 32, QFont.Bold)

        # Default Window Style
        self.WIN_STYLE = "background-color: lightblue; color: black"

        # GUI Refresh Rate
        self.REFRESH_RATE = 500

        # Main Formula Label
        self.textLabel = QLabel()
        self.textLabel.setFont(self.FONT)

        # User's Answer Label
        self.answerLabel = QLabel()
        self.answerLabel.setFont(self.FONT)

        # Result Label (in case of error)
        self.resultLabel = QLabel()
        self.resultLabel.setFont(self.FONT)

        # Main Horizontal Layout
        mainHLayout = QHBoxLayout()
        mainHLayout.addWidget(self.textLabel)
        mainHLayout.addWidget(self.answerLabel)
        mainHLayout.addWidget(self.resultLabel)

        # Main Vertical Layout
        mainVLayout = QVBoxLayout()
        mainVLayout.addLayout(mainHLayout)

        # Final Container + Display
        container = QWidget()
        container.setLayout(mainVLayout)
        container.setStyleSheet(self.WIN_STYLE)
        self.setCentralWidget(container)

        # Status Bar: Status Label (Left)
        self.statusLabel = QLabel()
        self.statusLabel.setFont(self.STATUS_FONT)

        # Status Bar: Time Label (Right)
        self.timeLabel = QLabel()
        self.timeLabel.setFont(self.STATUS_FONT)
        self.timeLabel.setAlignment(Qt.AlignRight)

        # Status Bar
        #statusHLayout = QHBoxLayout()
        #mainHLayout.addWidget(self.statusLabel)
        #mainHLayout.addWidget(self.timeLabel)
        #self.statusBar.addLayout(statusHLayout)

        self.statusBar = QStatusBar()
        self.statusBar.addWidget(self.statusLabel, 2)
        self.statusBar.addWidget(self.timeLabel, 1)
        self.setStatusBar(self.statusBar)

        # Window Size
        self.resize(self.WIDTH, self.HEIGHT)
        # Window Position
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        # GUI Refresh Timer
        self.refreshTimer = QTimer()
        self.refreshTimer.timeout.connect(self.update)

        self.show()

        self.update()

    def keyPressEvent(self, QKeyEvent):

        if (QKeyEvent.type() == QEvent.KeyPress):
            if (QKeyEvent.key() == Qt.Key_Escape):
                QCoreApplication.exit(0)

            self.updateState(QKeyEvent)

    def updateState(self, QKeyEvent):
        """ Automaton State Update """

        if (self.status in [Status.IDLE, Status.ANSWER]):
            if (self.status == Status.IDLE):
                # Starting of the game
                self.startTime = time.time()
                self.finalTime = -1
                self.score = 0
                self.refreshTimer.start(self.REFRESH_RATE)

            self.status = Status.TYPING
            self.result = random.randint(self.res_min, self.res_max)
            prev_nb1, prev_nb2 = self.nb1, self.nb2
            while True:
                self.nb1 = random.randint(0, self.result)
                self.nb2 = self.result - self.nb1
                if (self.nb1 != prev_nb1) and (self.nb2 != prev_nb2):
                    break
            self.answer = ''

        elif (self.status == Status.TYPING):
            # Typing the user answer
            if (QKeyEvent.key() >= Qt.Key_0) and (QKeyEvent.key() <= Qt.Key_9):
                self.answer += str(QKeyEvent.key() - Qt.Key_0)
            # Correcting the answer
            elif (QKeyEvent.key() == Qt.Key_Backspace):
                if (len(self.answer) > 0):
                    self.answer = self.answer[:-1]

            # Reaching the length of the result => changing status to ANSWER
            if (len(self.answer) >= len(str(self.result))):

                # Score update
                if (int(self.answer) == self.result):
                    self.score += 1

                if (self.score >= self.score_max):
                    self.status = Status.GAME_OVER
                    self.finalTime = time.time() - self.startTime
                else:
                    self.status = Status.ANSWER

        elif (self.status == Status.GAME_OVER):
            # Reinitializing the game
            self.status = Status.IDLE
            self.refreshTimer.stop()

        self.update()

    def update(self):

        self.refreshGui()
        self.refreshStatusBar()

    def refreshGui(self):

        if (self.status == Status.IDLE):
            self.textLabel.setText('Ready?')
            self.textLabel.setAlignment(Qt.AlignCenter)
            self.answerLabel.setVisible(False)
            self.answerLabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.resultLabel.setVisible(False)
            self.resultLabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        elif (self.status == Status.TYPING):
            self.textLabel.setText(f'  {self.nb1} + {self.nb2} = ')
            self.textLabel.setAlignment(Qt.AlignVCenter)
            if (len(self.answer) > 0):
                self.answerLabel.setText(f'{self.answer}')
            else:
                self.answerLabel.setText(f'?')
            self.answerLabel.setVisible(True)
            self.answerLabel.setStyleSheet(self.COLOR_TYPING)
            self.resultLabel.setVisible(False)

        elif (self.status in [Status.ANSWER, Status.GAME_OVER]):
            self.textLabel.setText(f'  {self.nb1} + {self.nb2} = ')
            self.textLabel.setAlignment(Qt.AlignVCenter)
            if (int(self.answer) == self.result):
                self.answerLabel.setText(f'{self.answer}')
                self.answerLabel.setStyleSheet(self.COLOR_CORRECT)
            else:
                self.answerLabel.setText(f'{self.answer}')
                self.answerLabel.setStyleSheet(self.COLOR_INCORRECT)
                self.resultLabel.setText(f' ({self.result})')
                self.resultLabel.setStyleSheet(self.COLOR_CORRECT)
                self.resultLabel.setVisible(True)

            # Game over message
            if (self.status == Status.GAME_OVER):
                self.textLabel.setStyleSheet(self.COLOR_END)
                self.answerLabel.setStyleSheet(self.COLOR_END)


    def refreshStatusBar(self):
        #self.statusBar().showMessage(self.status.name)
        self.statusLabel.setText(f'Score: {self.score} / {self.score_max} - [{self.status.name}]')
        if (self.status == Status.IDLE):
            self.timeLabel.setText('00:00:00')
        elif (self.status == Status.GAME_OVER):
            self.timeLabel.setText(time.strftime('%H:%M:%S', time.gmtime(int(self.finalTime))))
        else:
            self.timeLabel.setText(time.strftime('%H:%M:%S', time.gmtime(int(time.time() - self.startTime))))


if __name__ == '__main__':
    def usage():
        print(f'Usage: {sys.argv[0]} <res_min> <res_max> <score_max>')
        print(f'  - res_min must be >= 4')
        print(f'  - res_max must be >= 5')
        print(f'  - res_min must be < res_max')
        print(f'  - score_max must be >= 1')

    if (len(sys.argv) != 4):
        usage()
        sys.exit(-1)

    # Reading input parameters
    res_min = int(sys.argv[1])
    res_max = int(sys.argv[2])
    score_max = int(sys.argv[3])

    if (res_min < 4) or (res_max < 5) or (score_max < 1) or (res_min > res_max):
        usage()
        sys.exit(-2)

    app = QApplication(sys.argv)
    app.setApplicationName("Calcul Mental")

    window = CalculMentalWin(res_min, res_max, score_max)
    app.exec_()

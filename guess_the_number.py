#!/usr/bin/python3

import sys
import random
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QPushButton, QGridLayout,
                             QDesktopWidget, QApplication)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIntValidator

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.new_game()

    def initUI(self):
        self.answer = QLabel('Your answer',self)
        self.answerEdit = QLineEdit(self)
        self.answerEdit.setValidator(QIntValidator(1, 10))
        self.answerEdit.setPlaceholderText('Type a number from 1 to 10 and press Enter.')
        self.answerEdit.returnPressed.connect(self.get_user_answer)
        
        self.message = QLabel('Message',self)
        self.messageEdit = QTextEdit(self)
        
        self.btn_close = QPushButton ('Exit',self)
        self.btn_close.clicked.connect(QCoreApplication.instance().quit)
        
        self.btn_restart = QPushButton ('New game',self)
        self.btn_restart.clicked.connect(self.new_game)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(self.answer, 0, 0)
        grid.addWidget(self.answerEdit, 0, 1)
        grid.addWidget(self.message, 1, 0)
        grid.addWidget(self.messageEdit, 1, 1)
        grid.addWidget(self.btn_close, 3, 0)
        grid.addWidget(self.btn_restart, 3, 1)
        self.setLayout(grid)
        
        self.resize(500, 300)
        self.center()
        self.setWindowTitle('Guess the number')
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def new_game(self):
        self.count = 0
        self.number = random.randint(1, 10)
        self.answerEdit.setEnabled(True)
        self.answerEdit.setFocus()
        self.messageEdit.clear()
        self.messageEdit.append('New game!')
        
    def messages(self, text, user_answer, count=None):
        self.answerEdit.clear()
        if count:
            self.messageEdit.append(text+' The number is {}. Your count: {} attempt(s).'.format(user_answer, count))
        else:
            self.messageEdit.append('{} '.format(user_answer)+text+' than number')
    
    def get_user_answer(self):
        if self.answerEdit.text():
            self.count +=1
            user_answer = int(self.answerEdit.text())
            if user_answer == self.number:
                self.messages('You win!', user_answer, self.count)
                self.answerEdit.setDisabled(True)
            elif user_answer > self.number:
                self.messages('more', user_answer)
            elif user_answer < self.number:
                self.messages('less', user_answer)
                

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QLabel,
                             QComboBox, QGridLayout, QTextEdit, QLineEdit, QMainWindow,
                             QToolButton, QSizePolicy, QStackedWidget, QLayout)
from PyQt5.QtCore import Qt
import web
from gtts import gTTS
import pygame as pg
import random
import pyperclip
from Vocabulary import Vocabulary
from Writing import Writing

word_list = web.crawler("https://www.vocabulary.com/lists/274832")
menuOrder = ["단어 공부하기", "발음 확인하기", "영작 연습하기"]

class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size


class Menu(QWidget):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)
        layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        menu_layout = QHBoxLayout()
        self.title = QLabel("FeelMore")
        self.menu_btn = []
        
        for n, i in enumerate(menuOrder):
            self.menu_btn.append(QPushButton(i))
            self.menu_btn[n].setFixedHeight(200)
            menu_layout.addWidget(self.menu_btn[n])

        title_layout.addWidget(self.title)
        title_layout.setAlignment(Qt.AlignCenter)
        layout.addStretch(1)
        layout.addLayout(title_layout)
        layout.addStretch(1)
        layout.addLayout(menu_layout)
        layout.addStretch(1)
        self.setLayout(layout)

class Functions(QWidget):
    def __init__(self, parent=None):
        super(Functions, self).__init__(parent)
        sender = self.sender().text()
        layout = QVBoxLayout()
        exit_layout = QHBoxLayout()
        exit_layout.addStretch(1)
        self.exit_button = QPushButton("메뉴로", self)
        exit_layout.addWidget(self.exit_button)
        layout.addLayout(exit_layout)
        self.shuffle_btn = QPushButton()

        if sender == "발음 확인하기":
            main_layout = QHBoxLayout()
            text = '''웹사이트를 참고하세요!\n도움말: 앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠'''
            self.instruction = QLabel(text)
            main_layout.addWidget(self.instruction)
            main_layout.setAlignment(Qt.AlignCenter)
            layout.addLayout(main_layout)
            self.setLayout(layout)

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setGeometry(300, 300, 1000, 600)
        self.startMenu()

    def startMenu(self):
        self.setStyleSheet('font-size: 20pt; font-family: Courier;')
        self.window = Menu(self)
        self.setWindowTitle("FeelMore")
        self.setCentralWidget(self.window)
        self.window.menu_btn[0].clicked.connect(self.useFunctions)
        self.window.menu_btn[1].clicked.connect(self.useFunctions)
        self.window.menu_btn[2].clicked.connect(self.useFunctions)
        self.show()

    def useFunctions(self):
        self.setStyleSheet('font-size: 11pt; font-family: Courier;')
        sender = self.sender().text()
        print(sender)
        if sender == menuOrder[0] or sender == "단어 섞기":
            self.window = Vocabulary()
            self.window.shuffle_btn.clicked.connect(self.useFunctions)
        elif sender == menuOrder[1]:
            print("d")
        elif sender == menuOrder[2]:
            self.window = Writing()
        self.setCentralWidget(self.window)
        self.window.exit_button.clicked.connect(self.startMenu)


        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()
    sys.exit(app.exec_())
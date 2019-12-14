import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QLabel,
                             QComboBox, QGridLayout, QTextEdit, QLineEdit, QMainWindow, QStackedWidget)
from PyQt5.QtCore import Qt
import web

url = "https://www.vocabulary.com/lists/274832"

class Menu(QWidget):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)
        layout = QHBoxLayout()
        self.word_button = QPushButton("단어 공부하기")
        self.word_button.setFixedHeight(200)

        self.diction_button = QPushButton("발음 체크하기")
        self.diction_button.setFixedHeight(200)

        self.writing_button = QPushButton("영작 연습하기")
        self.writing_button.setFixedHeight(200)

        layout.addWidget(self.word_button)
        layout.addWidget(self.diction_button)
        layout.addWidget(self.writing_button)
        self.setLayout(layout)

class Functions(QWidget):
    def __init__(self, parent=None):
        super(Functions, self).__init__(parent)
        layout = QVBoxLayout()
        exit_layout = QHBoxLayout()
        exit_layout.addStretch(1)
        self.exit_button = QPushButton("메뉴로", self)
        exit_layout.addWidget(self.exit_button)
        layout.addLayout(exit_layout)

        sender = self.sender().text()

        if sender == "단어 공부하기":
            main_layout = QHBoxLayout()
            word_layout = QGridLayout()
            stats_layout = QVBoxLayout()
            self.word_screen = QTextEdit()
            self.trans_button = QPushButton("번역하기")
            self.word_screen.setReadOnly(True)
            stats_layout.addWidget(self.trans_button)
            stats_layout.addWidget(self.word_screen)
            main_layout.addLayout(word_layout)
            main_layout.addLayout(stats_layout)
            layout.addLayout(main_layout)

        self.setLayout(layout)


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setGeometry(300, 300, 960, 540)
        self.startMenu()

    def startMenu(self):
        self.window = Menu(self)
        self.setWindowTitle("FeelMore")
        self.setCentralWidget(self.window)
        self.window.word_button.clicked.connect(self.callback)
        self.show()

    def callback(self):
        self.window = Functions(self)
        self.setWindowTitle(self.sender().text())
        self.setCentralWidget(self.window)
        self.window.exit_button.clicked.connect(self.startMenu)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()
    sys.exit(app.exec_())
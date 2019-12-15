import sys
import pyperclip
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QLabel,
                             QComboBox, QGridLayout, QTextEdit, QLineEdit, QMainWindow, QStackedWidget)
from PyQt5.QtCore import Qt
import web

url = "https://www.vocabulary.com/lists/274832"

class Menu(QWidget):
    def __init__(self, parent=None):

        super(Menu, self).__init__(parent)
        layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        menu_layout = QHBoxLayout()
        self.title = QLabel("FeelMore")
        self.word_button = QPushButton("단어 공부하기")
        self.word_button.setFixedHeight(200)

        self.diction_button = QPushButton("발음 확인하기")
        self.diction_button.setFixedHeight(200)

        self.writing_button = QPushButton("영작 연습하기")
        self.writing_button.setFixedHeight(200)

        title_layout.addWidget(self.title)
        title_layout.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(self.word_button)
        menu_layout.addWidget(self.diction_button)
        menu_layout.addWidget(self.writing_button)
        layout.addStretch(1)
        layout.addLayout(title_layout)
        layout.addStretch(1)
        layout.addLayout(menu_layout)
        layout.addStretch(1)
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

        elif sender == "발음 확인하기":
            main_layout = QHBoxLayout()
            text = '''웹사이트를 참고하세요!\n도움말: 앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠'''
            self.instruction = QLabel(text)
            main_layout.addWidget(self.instruction)
            main_layout.setAlignment(Qt.AlignCenter)
            layout.addLayout(main_layout)

        elif sender == "영작 연습하기":
            main_layout = QVBoxLayout()
            button_layout = QHBoxLayout()
            self.draft_input = QTextEdit()
            self.korean_input = QLineEdit()
            self.copy_button = QPushButton("클립보드에 복사")
            self.to_eng_button = QPushButton("영어로")
            self.read_button = QPushButton("읽어주기")
            self.copy_button.clicked.connect(self.copy)
            self.to_eng_button.clicked.connect(self.korToEng)
            self.korean_input.setFixedWidth(300)
            main_layout.addStretch(1)
            main_layout.addWidget(self.draft_input)
            button_layout.addWidget(self.copy_button)
            button_layout.addStretch(1)
            button_layout.addWidget(self.korean_input)
            button_layout.addWidget(self.to_eng_button)
            button_layout.addWidget(self.read_button)
            main_layout.addLayout(button_layout)
            main_layout.addStretch(1)
            layout.addLayout(main_layout)

        self.setLayout(layout)

    def copy(self):
        pyperclip.copy(self.draft_input.toPlainText())

    def korToEng(self):
        translated = web.papago(self.korean_input.text()[:300], True)
        self.draft_input.setText(self.draft_input.toPlainText() + " " + translated)


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setGeometry(300, 300, 960, 540)
        self.startMenu()

    def startMenu(self):
        self.setStyleSheet('font-size: 20pt; font-family: Courier;')
        self.window = Menu(self)
        self.setWindowTitle("FeelMore")
        self.setCentralWidget(self.window)
        self.window.word_button.clicked.connect(self.useFunctions)
        self.window.diction_button.clicked.connect(self.useFunctions)
        self.window.writing_button.clicked.connect(self.useFunctions)
        self.show()

    def useFunctions(self):
        self.setStyleSheet('font-size: 11pt; font-family: Courier;')
        self.window = Functions(self)
        self.setWindowTitle(self.sender().text())
        self.setCentralWidget(self.window)
        self.window.exit_button.clicked.connect(self.startMenu)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()
    sys.exit(app.exec_())

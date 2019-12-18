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
        
        for i, n in enumerate(menuOrder):
            self.menu_btn[n] = QPushButton(i)
            self.menu_btn[n].setFixedHeight(200)

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
        sender = self.sender().text()
        layout = QVBoxLayout()
        exit_layout = QHBoxLayout()
        exit_layout.addStretch(1)
        self.exit_button = QPushButton("메뉴로", self)
        exit_layout.addWidget(self.exit_button)
        layout.addLayout(exit_layout)

        if sender == "발음 확인하기":
            main_layout = QHBoxLayout()
            text = '''웹사이트를 참고하세요!\n도움말: 앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠'''
            self.instruction = QLabel(text)
            main_layout.addWidget(self.instruction)
            main_layout.setAlignment(Qt.AlignCenter)
            layout.addLayout(main_layout)
            self.setLayout(layout)

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
            layout.addLayout(main_layout) # self.setLayout(main_layout)
            self.setLayout(layout)

    def copy(self):
        pyperclip.copy(self.draft_input.toPlainText())

    def korToEng(self):
        translated = web.papago(self.korean_input.text()[:300], True)
        self.draft_input.setText(self.draft_input.toPlainText() + " " + translated)


    def play_music(self, music_file, volume=0.8):
        '''
        stream music with mixer.music module in a blocking manner
        this will stream the sound from disk while playing
        '''
        # set up the mixer
        freq = 24100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 1  # 1 is mono, 2 is stereo
        buffer = 1000  # number of samples (experiment to get best sound)
        pg.mixer.init(freq, bitsize, channels, buffer)
        # volume value 0.0 to 1.0
        pg.mixer.music.set_volume(volume)
        clock = pg.time.Clock()
        try:
            pg.mixer.music.load(music_file)
        except pg.error:
            print("File {} not found! ({})".format(music_file, pg.get_error()))
            return
        pg.mixer.music.play()
        while pg.mixer.music.get_busy():
            # check if playback has finished
            clock.tick(30)

    def buttonClicked(self):
        button = self.sender()
        word = button.text()
        self.eng_display.setText("English: " + word)
        self.kor_display.setText("Korean: "+ web.papago(word))
        if self.country.currentText() == "US":
            us = gTTS(text=word, lang='en-us')
            us_file = "us.mp3"
            us.save(us_file)
            music_file = us_file
            volume = 0.8
            self.play_music(music_file, volume)
        elif self.country.currentText() == "UK":
            uk = gTTS(text=word, lang='en-uk')
            uk_file = "uk.mp3"
            uk.save(uk_file)
            music_file = uk_file
            volume = 0.8
            self.play_music(music_file, volume)
        else:
            za = gTTS(text=word, lang='en-ca')
            za_file = "ca.mp3"
            za.save(za_file)
            # print("convert complete")
            music_file = za_file
        # optional volume 0 to 1.0
            volume = 0.8
            self.play_music(music_file, volume)

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
        self.window.menu_btn[0].clicked.connect(self.useFunctions)
        self.window.menu_btn[0].clicked.connect(self.useFunctions)
        self.show()

    def useFunctions(self):
        self.setStyleSheet('font-size: 11pt; font-family: Courier;')
        sender = self.sender().text()
        if sender == menuOrder[0]:
            self.window = Vocabulary()
        elif sender == menuOrder[1]:
        elif sender == menuOrder[2]:
            self.window = Writing()
        self.setCentralWidget(self.window)
        self.window.exit_button.clicked.connect(self.startMenu)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()
    sys.exit(app.exec_())
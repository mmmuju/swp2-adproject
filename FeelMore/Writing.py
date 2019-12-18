from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QLabel,
                             QComboBox, QGridLayout, QTextEdit, QLineEdit, QMainWindow,
                             QToolButton, QSizePolicy, QStackedWidget, QLayout)
from PyQt5.QtCore import Qt
import web
from gtts import gTTS
import pygame as pg
import pyperclip

class Writing(QWidget):
    def __init__(self, parent=None):
        super(Writing, self).__init__(parent)
        layout = QVBoxLayout()
        exit_layout = QHBoxLayout()
        exit_layout.addStretch(1)
        self.exit_button = QPushButton("메뉴로", self)
        exit_layout.addWidget(self.exit_button)
        layout.addLayout(exit_layout)

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
        layout.addLayout(main_layout)  # self.setLayout(main_layout)
        self.setLayout(layout)

    def copy(self):
        pyperclip.copy(self.draft_input.toPlainText())

    def korToEng(self):
        translated = web.papago(self.korean_input.text()[:300], True)
        self.draft_input.setText(self.draft_input.toPlainText() + " " + translated)

    def play_music(self, music_file, volume=0.8):
        freq = 24100
        bitsize = -16
        channels = 1
        buffer = 1000
        pg.mixer.init(freq, bitsize, channels, buffer)
        pg.mixer.music.set_volume(volume)
        clock = pg.time.Clock()
        try:
            pg.mixer.music.load(music_file)
        except pg.error:
            print("File {} not found! ({})".format(music_file, pg.get_error()))
            return
        pg.mixer.music.play()
        while pg.mixer.music.get_busy():
            clock.tick(30)
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QLabel,
                             QComboBox, QGridLayout, QTextEdit, QLineEdit, QMainWindow,
                             QToolButton, QSizePolicy, QStackedWidget, QLayout)
from random import shuffle
from PyQt5.QtCore import Qt
from gtts import gTTS
import pygame as pg

import web
word_list = web.crawler("https://www.vocabulary.com/lists/274832")

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


class Vocabulary(QWidget):

    def __init__(self, parent=None):
        super(Vocabulary, self).__init__(parent)
        self.initLayout()

    def initLayout(self):
        self.layout = QVBoxLayout()
        exit_layout = QHBoxLayout()
        exit_layout.addStretch(1)
        self.exit_button = QPushButton("메뉴로", self)
        exit_layout.addWidget(self.exit_button)
        self.layout.addLayout(exit_layout)
        self.shuffle_btn = Button("단어 섞기", self.wordClicked)

        self.words = word_list[:40]
        word_layout = QGridLayout()
        country_layout = QGridLayout()
        self.country = QComboBox()
        self.country.addItem("US")
        self.country.addItem("UK")
        self.country.addItem("CA")
        self.eng_display = QLineEdit()
        self.eng_display.setReadOnly(True)
        self.eng_display.setAlignment(Qt.AlignLeft)
        self.eng_display.setMaxLength(30)
        self.kor_display = QLineEdit()
        self.kor_display.setReadOnly(True)
        self.kor_display.setAlignment(Qt.AlignLeft)
        self.kor_display.setMaxLength(30)
        country_layout.addWidget(self.eng_display, 0, 0)
        country_layout.addWidget(self.kor_display, 1, 0)
        country_layout.addWidget(self.country, 0, 1)
        r, c = 0, 0
        for btnText in self.words:
            button = Button(btnText, self.wordClicked)
            word_layout.addWidget(button, r, c)
            c += 1
            if c >= 5:
                c = 0
                r += 1
        main_layout = QVBoxLayout()
        main_layout.addLayout(country_layout)
        main_layout.addLayout(word_layout)
        main_layout.addWidget(self.shuffle_btn)
        self.layout.addLayout(main_layout)
        self.setLayout(self.layout)

    def wordClicked(self):
        button = self.sender()
        word = button.text()
        self.eng_display.setText("English: " + word)
        self.kor_display.setText("Korean: "+ web.papago(word))
        if word == "단어 섞기":
            shuffle(word_list)
            self.initLayout()
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
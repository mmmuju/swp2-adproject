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

class CheckDiction(QWidget):
    def __init__(self, parent=None):
        super(CheckDiction, self).__init__(parent)
        layout = QVBoxLayout()
        exit_layout = QHBoxLayout()
        exit_layout.addStretch(1)
        self.exit_button = QPushButton("메뉴로", self)
        exit_layout.addWidget(self.exit_button)
        layout.addLayout(exit_layout)
        self.shuffle_btn = QPushButton()
        main_layout = QHBoxLayout()
        text = '''웹사이트를 참고하세요!\n도움말: 앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠앙기모띠'''
        self.instruction = QLabel(text)
        main_layout.addWidget(self.instruction)
        main_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(main_layout)
        self.setLayout(layout)
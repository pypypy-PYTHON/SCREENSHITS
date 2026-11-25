import sys
import ctypes
import os, random
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QTimer, Qt, QSize
from dbus_idle import IdleMonitor
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtGui import QKeySequence, QShortcut

IDLE_LIMIT = 120

class SleepGif(QLabel):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setStyleSheet("background-color: black;")

        self.movie = QMovie("funny.gif")
        self.setMovie(self.movie)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_idle)
        self.timer.start(1000)
        self.idle_counter = 0

        QShortcut(QKeySequence("Escape"), self, activated=self.close)
        

    def idle_seconds(self):
        milliseconds = IdleMonitor().get_dbus_idle()
        return milliseconds / 1000.0

    def check_idle(self):
        idle = self.idle_seconds()

        if idle > IDLE_LIMIT:
            self.idle_counter += 1
        else:
            self.idle_counter = 0

        if self.idle_counter >= 3 and not self.isVisible():
            self.showFullScreen()
            
            screen = QGuiApplication.primaryScreen()
            screen_size = screen.size()
            self.movie.setScaledSize(screen_size)
            
            self.movie.start()

        elif self.idle_counter == 0 and self.isVisible():
            self.movie.stop()
            self.hide()

app = QApplication(sys.argv)
w = SleepGif()
sys.exit(app.exec())
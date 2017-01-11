from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from ..codeedit.codeeditview import CodeEditView


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("resources/interface/mainwindow.ui", self)

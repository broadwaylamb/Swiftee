from typing import Optional
from PyQt5.QtWidgets import QWidget
import PyQt5.uic as uic


class SetParametersWindow(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(SetParametersWindow, self).__init__(parent)
        uic.loadUi("newproject/setparameters.ui", self)

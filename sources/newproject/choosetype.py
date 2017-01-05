from typing import Optional
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
import PyQt5.uic as uic
# noinspection PyUnresolvedReferences
import sources.ui.icons_rc


class NewProjectWindow(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super(NewProjectWindow, self).__init__(parent)
        uic.loadUi("newproject/choosetype.ui", self)

        self.tab_bar.addTab("Default")
        self.tab_bar.addTab("Custom")
        self.tab_bar.currentChanged.connect(self.__update_model)

        default_templates = [
            QStandardItem(QIcon(QPixmap(":icons/executable.png")), "Executable"),
            QStandardItem(QIcon(QPixmap(":icons/library.png")), "Library"),
            QStandardItem(QIcon(QPixmap(":icons/empty.png")), "Empty")
        ]

        custom_templates = [
            QStandardItem(QIcon(QPixmap(":icons/empty.png")), "Custom 1"),
            QStandardItem(QIcon(QPixmap(":icons/empty.png")), "Custom 2"),
        ]

        self.default_model = QStandardItemModel(self)
        self.default_model.appendColumn(default_templates)
        self.custom_model = QStandardItemModel(self)
        self.custom_model.appendColumn(custom_templates)

        self.template_view.setModel(self.default_model)
        self.template_view.setDragEnabled(False)

    @pyqtSlot()
    def __update_model(self) -> None:
        if self.tab_bar.currentIndex() == 0:
            self.template_view.setModel(self.default_model)
        elif self.tab_bar.currentIndex() == 1:
            self.template_view.setModel(self.custom_model)
import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QTreeView, QToolBar
from PyQt5.QtCore import Qt
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Annotate types to use code completion
        self.variables_view: QTreeView = None
        self.navigator_switch: QToolBar = None
        self.navigator_stack: QWidget = None
        self.code_edit_toolbar: QToolBar = None
        self.debug_toolbar: QToolBar = None
        self.variables_view: QTreeView = None
        self.variables_toolbar: QToolBar = None
        self.console_toolbar: QToolBar = None
        self.inspector_switch: QToolBar = None
        self.inspector_stack: QWidget = None
        self.library_switch: QToolBar = None
        self.library_stack: QWidget = None

        uic.loadUi("resources/interface/mainwindow.ui", self)

        self._polish_ui()

    def _polish_ui(self):

        """
        This method sets platform-dependent UI parameters that could not be set in a .ui file.
        """
        self.variables_view.setAttribute(Qt.WA_MacShowFocusRect, False)

        if sys.platform == "darwin":
            self.navigator_stack.setStyleSheet(
                "QWidget {"
                "    border: none;"
                "}"
            )
            self.navigator_switch.setStyleSheet(
                "QToolBar {"
                "   background: palette(window);"
                "   border-color: palette(mid);"
                "   border-width: 0px 0px 1px 0px;"
                "   border-style: solid;"
                "}"
            )
            self.code_edit_toolbar.setStyleSheet(
                "QToolBar {"
                "   background: white;"
                "   border-color: palette(mid);"
                "   border-width: 0px 0px 1px 0px;"
                "   border-style: solid;"
                "}"
            )
            self.inspector_switch.setStyleSheet(
                "QToolBar {"
                "   background: palette(window);"
                "   border-color: palette(mid);"
                "   border-width: 0px 0px 1px 1px;"
                "   border-style: solid;"
                "}"
            )
            self.variables_view.setStyleSheet(
                "QTreeView {"
                "   border: none"
                "}"
            )
            self.variables_toolbar.setStyleSheet(
                "QToolBar {"
                "   background: white;"
                "   border-color: palette(mid);"
                "   border-width: 1px 0px 0px 0px;"
                "   border-style: solid;"
                "}"
            )

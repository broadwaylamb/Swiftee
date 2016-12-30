from .codeeditview import CodeEditView
from .linenumberrulerview import LineNumberRulerView
from .rulermarker import RulerMarker

__all__ = ["CodeEditView", "LineNumberRulerView", "RulerMarker"]


def test():
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from PyQt5.QtCore import pyqtSlot
    from codeedit.test_ui import Ui_MainWindow

    class MainWindow(QMainWindow):

        def __init__(self):
            super(MainWindow, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.codeEdit.has_ruler = True

        @pyqtSlot()
        def on_push_button_clicked(self):
            if self.ui.codeEdit.is_ruler_visible:
                self.ui.codeEdit.is_ruler_visible = False
            else:
                self.ui.codeEdit.is_ruler_visible = True

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

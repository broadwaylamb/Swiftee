from .codeeditview import CodeEditView
from .linenumberrulerview import LineNumberRulerView
from .rulermarker import RulerMarker

__all__ = ["CodeEditView", "LineNumberRulerView", "RulerMarker"]


def test():
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget
    from PyQt5.QtCore import pyqtSlot
    import PyQt5.uic as uic

    class CodeEditWindow(QWidget):

        def __init__(self):
            super(CodeEditWindow, self).__init__()
            uic.loadUi("codeedit/test_ui.ui", self)
            self.code_edit_view.has_ruler = True

        @pyqtSlot()
        def on_button_clicked(self):
            self.code_edit_view.is_ruler_visible = not self.code_edit_view.is_ruler_visible

    app = QApplication(sys.argv)
    window = CodeEditWindow()
    window.show()
    sys.exit(app.exec_())

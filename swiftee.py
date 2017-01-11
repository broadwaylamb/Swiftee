if __name__ == '__main__':

    import sys
    from PyQt5.QtWidgets import QApplication, QToolBar
    from PyQt5.QtGui import QPalette
    from PyQt5.QtCore import Qt
    from sources.workspace.mainwindow import MainWindow
    from sources.codeedit.codeeditview import CodeEditView

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    window.code_edit_view: CodeEditView
    window.code_edit_toolbar: QToolBar

    window.code_edit_view.has_ruler = True
    window.code_edit_view.is_ruler_visible = True

    sys.exit(app.exec_())

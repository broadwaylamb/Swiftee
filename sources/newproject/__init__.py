def test():
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget, QStackedLayout
    from PyQt5.QtCore import pyqtSlot
    from .choosetype import NewProjectWindow
    from .setparameters import SetParametersWindow

    app = QApplication(sys.argv)

    window = QWidget()
    ctw = NewProjectWindow(window)
    spw = SetParametersWindow(window)

    stacked_layout = QStackedLayout(window)
    stacked_layout.addWidget(ctw)
    stacked_layout.addWidget(spw)
    stacked_layout.setCurrentIndex(0)
    window.setLayout(stacked_layout)
    window.setFixedSize(586, 485)
    window.show()

    @pyqtSlot()
    def next_():
        stacked_layout.setCurrentIndex(1)

    @pyqtSlot()
    def previous_():
        stacked_layout.setCurrentIndex(0)

    ctw.next_button.clicked.connect(next_)
    spw.previous_button.clicked.connect(previous_)

    sys.exit(app.exec_())

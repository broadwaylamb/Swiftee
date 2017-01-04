
def test():
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget, QAbstractItemView
    from PyQt5.QtCore import QSize
    from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon, QPixmap
    # noinspection PyUnresolvedReferences
    import sources.ui.icons_rc
    import PyQt5.uic as uic

    class NewProjectWindow(QWidget):

        def __init__(self):
            super(QWidget, self).__init__()
            uic.loadUi("newproject/choosetype.ui", self)

            items = [
                QStandardItem(QIcon(QPixmap(":icons/executable.png")), "Executable"),
                QStandardItem(QIcon(QPixmap(":icons/library.png")), "Library"),
                QStandardItem(QIcon(QPixmap(":icons/empty.png")), "Empty")
            ]

            model = QStandardItemModel(self)
            model.appendColumn(items)

            self.list_view.setModel(model)
            self.list_view.setDragEnabled(False)
            self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.list_view.setUniformItemSizes(True)
            self.list_view.setGridSize(QSize(100, 100))
            self.list_view.setIconSize(QSize(70, 70))
            self.list_view.setCurrentIndex(model.indexFromItem(items[0]))

    app = QApplication(sys.argv)
    window = NewProjectWindow()
    window.show()
    sys.exit(app.exec_())
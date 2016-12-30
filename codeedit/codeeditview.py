import typing
from PyQt5.QtWidgets import QTextEdit, QWidget
from PyQt5.QtGui import QWheelEvent, QResizeEvent
from PyQt5.QtCore import pyqtSlot, QTimer
from .linenumberrulerview import LineNumberRulerView


class CodeEditView(QTextEdit):

    __resize_timeout_in_milliseconds = 250

    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.__ruler_view: LineNumberRulerView = None
        self.__has_ruler = False
        self.__is_ruler_visible = False
        self.__resize_timer = QTimer(self)
        self.__resize_timer.timeout.connect(self.resize_timeout)
        self.__old_size = self.size()
        self.__new_size = self.size()

    def tile(self) -> None:
        if self.__is_ruler_visible:
            self.setViewportMargins(self.__ruler_view.required_thickness, 0, 0, 0)
        else:
            self.setViewportMargins(0, 0, 0, 0)

        self.update()

    @property
    def has_ruler(self) -> bool:
        return self.__has_ruler

    @has_ruler.setter
    def has_ruler(self, value: bool):

        if self.__has_ruler == value:
            return

        self.__has_ruler = value

        if self.__has_ruler and self.__ruler_view is None:
            self.__ruler_view = LineNumberRulerView(self)
            self.__ruler_view.setVisible(False)

        if self.__is_ruler_visible:

            if self.__has_ruler:
                self.__ruler_view.show()
            else:
                self.__ruler_view.hide()

            self.tile()

    @property
    def is_ruler_visible(self) -> bool:
        return self.__is_ruler_visible

    @is_ruler_visible.setter
    def is_ruler_visible(self, value: bool):

        if self.__is_ruler_visible == value or not self.__has_ruler:
            return

        self.__is_ruler_visible = value

        if value:
            self.__ruler_view.show()
        else:
            self.__ruler_view.hide()

        self.tile()

    @property
    def ruler(self) -> LineNumberRulerView:
        return self.__ruler_view

    @ruler.setter
    def ruler(self, value: LineNumberRulerView):

        if self.__is_ruler_visible and self.__ruler_view is not None:
            self.__ruler_view.hide()

        self.__ruler_view = value

        if self.__ruler_view is None:
            self.__has_ruler = False
        elif self.__is_ruler_visible:
            self.__ruler_view.show()

    def wheelEvent(self, event: QWheelEvent) -> None:
        super().wheelEvent(event)

        if not event.pixelDelta().isNull() or not event.angleDelta().isNull():
            if self.__has_ruler:
                self.__ruler_view.update()

    @pyqtSlot()
    def resize_timeout(self):
        self.__resize_timer.stop()
        print("resize timeout")
        super(CodeEditView, self).resizeEvent(QResizeEvent(self.__new_size, self.__old_size))

    def resizeEvent(self, event: QResizeEvent):

        # When there are too many lines of code, horizontal resizing is too laggy because `resizeEvent` is
        # invoked too often and therefore `repaintEvent` is invoked too often as well.
        # So we defer invoking super's `resizeEvent` using QTimer.
        # See also http://robertfelten.com/2013/08/20/tip-for-resizing-qt-windows/
        print("resize event")

        # If resizing is only begun, we set the `self.__old_size` variable to the current size
        # in order to invoke super's `resizeEvent` with correct parameters later.
        if not self.__resize_timer.isActive():
            self.__old_size = event.oldSize()
        self.__new_size = event.size()
        self.__resize_timer.start(CodeEditView.__resize_timeout_in_milliseconds)

        if self.__has_ruler:
            self.__ruler_view.setGeometry(0, 0, self.__ruler_view.required_thickness, self.height())
            self.__ruler_view.update()

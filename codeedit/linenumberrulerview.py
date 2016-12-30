import typing
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QTextBlock, QTextCursor, QMouseEvent, QPaintEvent, QColor
from PyQt5.QtCore import QRect, QPoint, Qt


class LineNumberRulerView(QWidget):

    __ruler_thickness = 32

    def __init__(self, code_edit_view) -> None:
        super().__init__(code_edit_view)

        from .codeeditview import CodeEditView

        self.__code_edit: CodeEditView = code_edit_view
        self.__markers = []
        self.__accessory_widget: typing.Optional[QWidget] = None
        self.__rule_thickness: int = LineNumberRulerView.__ruler_thickness
        self.__reserved_thickness_for_markers: int = 0
        self.__reserved_thickness_for_accessory_widget: int = 0

        self.__code_edit.textChanged.connect(self.update)
        self.__code_edit.cursorPositionChanged.connect(self.update)
        self.__code_edit.selectionChanged.connect(self.update)
        self.__code_edit.verticalScrollBar().valueChanged.connect(self.update)

    @property
    def code_edit(self):
        return self.__code_edit

    @code_edit.setter
    def code_edit(self, value):
        self.__code_edit = value

    @property
    def accessory_widget(self) -> typing.Optional[QWidget]:
        return self.__accessory_widget

    @accessory_widget.setter
    def accessory_widget(self, value: typing.Optional[QWidget]):
        # TODO: support for accessory widgets is not implemented
        self.__accessory_widget = value
        self.update()

    def __verify_reserved_thickness_for_markers(self) -> None:

        if not self.__markers:
            return

        max_thickness: int = max(list(map(lambda element: element.thickness_required_in_ruler, self.__markers)))

        if max_thickness > self.__reserved_thickness_for_markers:
            self.reserved_thickness_for_markers = max_thickness

    @property
    def markers(self):
        return self.__markers

    @markers.setter
    def markers(self, value):
        self.__markers = value
        self.update()

    def add_marker(self, marker):
        marker_thickness: int = marker.thickness_required_in_ruler

        if marker_thickness > self.reserved_thickness_for_markers:
            self.reserved_thickness_for_markers = marker_thickness

        if not self.__markers:
            self.__markers = [marker]
        else:
            self.__markers.append(marker)

        self.update()
    
    def remove_marker(self, marker):
        if not self.__markers:
            return

        self.__markers.remove(marker)
        self.update()

    def track_marker(self, marker, event: QMouseEvent) -> bool:
        return marker.trackMouse(event, True)

    def __first_visible_block(self) -> QTextBlock:
        cursor = self.__code_edit.cursorForPosition(QPoint(0, 0))
        return cursor.block()

    def __last_visible_block(self) -> QTextBlock:
        cursor = self.__code_edit.cursorForPosition(self.__code_edit.geometry().bottomLeft())
        return cursor.block().next()

    @staticmethod
    def __draw_line_number(line_number: int, y: int, painter: QPainter):
        painter.drawText(QPoint(0, y), str(line_number))
    
    def _draw_line_numbers_in_rect(self, rect: QRect):
        painter = QPainter(self)
        first_visible_block = self.__first_visible_block()
        last_visible_block = self.__last_visible_block()

        block = first_visible_block
        while block.isValid() and block != last_visible_block:
            line_number = block.blockNumber() + 1
            y = self.__code_edit.cursorRect(QTextCursor(block)).bottom()
            self.__draw_line_number(line_number, y, painter)
            block = block.next()
    
    def _draw_markers_in_rect(self, rect: QRect):
        for marker in self.__markers:
            marker.drawRect(rect)

    @property
    def reserved_thickness_for_accessory_widget(self) -> int:
        return self.__reserved_thickness_for_accessory_widget

    @reserved_thickness_for_accessory_widget.setter
    def reserved_thickness_for_accessory_widget(self, value: int):
        self.__reserved_thickness_for_accessory_widget = value
        self.__code_edit.tile()

    @property
    def rule_thickness(self) -> int:
        return self.__rule_thickness

    @rule_thickness.setter
    def rule_thickness(self, value: int):
        self.__rule_thickness = value
        self.__code_edit.tile()

    @property
    def reserved_thickness_for_markers(self) -> int:
        return self.__reserved_thickness_for_markers

    @reserved_thickness_for_markers.setter
    def reserved_thickness_for_markers(self, value: int):
        self.__reserved_thickness_for_markers = value
        self.__code_edit.tile()

    @property
    def required_thickness(self) -> int:
        return self.rule_thickness +\
               self.reserved_thickness_for_markers +\
               self.reserved_thickness_for_accessory_widget

    def paintEvent(self, event: QPaintEvent):
        super(LineNumberRulerView, self).paintEvent(event)

        painter = QPainter(self)
        background_color = QColor(Qt.lightGray)
        painter.fillRect(event.rect(), background_color)

        self._draw_line_numbers_in_rect(event.rect())
        self._draw_markers_in_rect(event.rect())


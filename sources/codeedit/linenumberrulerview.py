import sys
from typing import Optional, List
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QTextBlock, QTextCursor, QMouseEvent, QPaintEvent, QColor, QFontMetrics, QFont
from PyQt5.QtCore import QRect, QPoint, Qt
try:
    from .codeeditview import CodeEditView
except ImportError:
    CodeEditView = sys.modules[__package__ + ".codeeditview"]
from .rulermarker import RulerMarker


class LineNumberRulerView(QWidget):

    # TODO: Make this equal to 4 widths of the current font
    __ruler_thickness = 32

    def __init__(self, code_edit_view: CodeEditView) -> None:
        super().__init__(code_edit_view)

        self.__code_edit: CodeEditView = code_edit_view
        self.__markers: List[RulerMarker] = []
        self.__accessory_widget: Optional[QWidget] = None
        self.__rule_thickness = LineNumberRulerView.__ruler_thickness
        self.__reserved_thickness_for_markers = 0
        self.__reserved_thickness_for_accessory_widget = 0

        self.__code_edit.textChanged.connect(self.update)
        self.__code_edit.cursorPositionChanged.connect(self.update)
        self.__code_edit.selectionChanged.connect(self.update)
        self.__code_edit.verticalScrollBar().valueChanged.connect(self.update)

    @property
    def code_edit(self) -> CodeEditView:
        return self.__code_edit

    @code_edit.setter
    def code_edit(self, value: CodeEditView) -> None:
        self.__code_edit = value

    @property
    def accessory_widget(self) -> Optional[QWidget]:
        return self.__accessory_widget

    @accessory_widget.setter
    def accessory_widget(self, value: Optional[QWidget]) -> None:
        # TODO: Implement support for accessory widgets
        self.__accessory_widget = value
        self.update()

    def __verify_reserved_thickness_for_markers(self) -> None:

        if not self.__markers:
            return

        max_thickness: int = max(list(map(lambda element: element.thickness_required_in_ruler, self.__markers)))

        if max_thickness > self.__reserved_thickness_for_markers:
            self.reserved_thickness_for_markers = max_thickness

    @property
    def markers(self) -> List[RulerMarker]:
        return self.__markers

    @markers.setter
    def markers(self, value: List[RulerMarker]):
        self.__markers = value
        self.update()

    def add_marker(self, marker: RulerMarker):
        marker_thickness: int = marker.thickness_required_in_ruler

        if marker_thickness > self.reserved_thickness_for_markers:
            self.reserved_thickness_for_markers = marker_thickness
            self.__markers.append(marker)

        self.update()
    
    def remove_marker(self, marker: RulerMarker) -> None:
        if not self.__markers:
            return

        self.__markers.remove(marker)
        self.update()

    def track_marker(self, marker: RulerMarker, event: QMouseEvent) -> bool:
        return marker.trackMouse(event, True)

    def __first_visible_block(self) -> QTextBlock:
        cursor = self.__code_edit.cursorForPosition(QPoint(0, 0))
        return cursor.block()

    @staticmethod
    def __draw_line_number(line_number: int, y: int, painter: QPainter) -> None:
        painter.drawText(QPoint(0, y), str(line_number))
    
    def _draw_line_numbers_in_rect(self, rect: QRect) -> None:
        painter = QPainter(self)
        first_visible_block = self.__first_visible_block()

        block = first_visible_block

        line_number_font_metrics = QFontMetrics(painter.font(), painter.device())

        while block.isValid():
            line_number = block.blockNumber() + 1

            cursor = QTextCursor(block)

            y = self.__code_edit.cursorRect(cursor).bottom()

            if y >= rect.bottom() + line_number_font_metrics.height():
                break

            self.__draw_line_number(line_number, y, painter)
            block = block.next()
    
    def _draw_markers_in_rect(self, rect: QRect) -> None:
        for marker in self.__markers:
            marker.drawRect(rect)

    @property
    def reserved_thickness_for_accessory_widget(self) -> int:
        return self.__reserved_thickness_for_accessory_widget

    @reserved_thickness_for_accessory_widget.setter
    def reserved_thickness_for_accessory_widget(self, value: int) -> None:
        self.__reserved_thickness_for_accessory_widget = value
        self.__code_edit.tile()

    @property
    def rule_thickness(self) -> int:
        return self.__rule_thickness

    @rule_thickness.setter
    def rule_thickness(self, value: int) -> None:
        self.__rule_thickness = value
        self.__code_edit.tile()

    @property
    def reserved_thickness_for_markers(self) -> int:
        return self.__reserved_thickness_for_markers

    @reserved_thickness_for_markers.setter
    def reserved_thickness_for_markers(self, value: int) -> None:
        self.__reserved_thickness_for_markers = value
        self.__code_edit.tile()

    @property
    def required_thickness(self) -> int:
        return self.rule_thickness +\
               self.reserved_thickness_for_markers +\
               self.reserved_thickness_for_accessory_widget

    def paintEvent(self, event: QPaintEvent) -> None:
        super(LineNumberRulerView, self).paintEvent(event)

        painter = QPainter(self)
        background_color = QColor(Qt.lightGray)
        painter.fillRect(event.rect(), background_color)

        self._draw_line_numbers_in_rect(event.rect())
        self._draw_markers_in_rect(event.rect())

    def wheelEvent(self, event) -> None:
        super(LineNumberRulerView, self).wheelEvent(event)
        self.__code_edit.wheelEvent(event)

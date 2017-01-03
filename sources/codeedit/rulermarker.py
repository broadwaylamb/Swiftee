import sys
from typing import Optional
from PyQt5.Qt import QObject, QRect, QMouseEvent
try:
    from .linenumberrulerview import LineNumberRulerView
except ImportError:
    LineNumberRulerView = sys.modules[__package__ + ".linenumberrulerview"]


class RulerMarker(QObject):
    def __init__(self, ruler: LineNumberRulerView, location: int) -> None:
        super().__init__(ruler)
        self.__ruler_view: LineNumberRulerView = ruler
        self.__location: int = location
        self.__is_movable = False
        self.__represented_object: Optional[QObject] = None
        self.__is_removable = False
        self.__is_dragging = False

    @property
    def ruler(self) -> LineNumberRulerView:
        return self.__ruler_view

    @ruler.setter
    def ruler(self, value: LineNumberRulerView) -> None:
        pass

    @property
    def thickness_required_in_ruler(self) -> int:
        return 0

    @property
    def is_movable(self) -> bool:
        return self.__is_movable

    @is_movable.setter
    def is_movable(self, value: bool):
        pass

    @property
    def is_removable(self) -> bool:
        return self.__is_removable

    @is_removable.setter
    def is_removable(self, value: bool):
        pass

    @property
    def location(self) -> int:
        return self.__location

    @location.setter
    def location(self, value: int):
        pass

    @property
    def represented_object(self) -> Optional[QObject]:
        return self.__represented_object

    @represented_object.setter
    def represented_object(self, value: QObject) -> None:
        pass

    def draw_rect(self, rect: QRect) -> None:
        pass

    @property
    def is_dragging(self) -> bool:
        return self.__is_dragging

    def track_mouse(self, event: QMouseEvent, adding: bool) -> bool:
        self
        return False

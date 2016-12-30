import typing
from PyQt5.Qt import QObject, QRect, QMouseEvent
from .linenumberrulerview import LineNumberRulerView


class RulerMarker(QObject):
    def __init__(self, ruler: LineNumberRulerView, location: int) -> None:
        super().__init__(ruler)
        self.__ruler_view: LineNumberRulerView = ruler
        self.__location: int = location
        self.__is_movable: bool = False
        self.__represented_object: typing.Optional[QObject] = None
        self.__is_removable: bool = False
        self.__is_dragging: bool = False

    @property
    def ruler(self):
        return self.__ruler_view

    @ruler.setter
    def ruler(self, value):
        pass

    @property
    def thickness_required_in_ruler(self):
        return 0

    @property
    def is_movable(self):
        return self.__is_movable

    @is_movable.setter
    def is_movable(self, value):
        pass

    @property
    def is_removable(self):
        return self.__is_removable

    @is_removable.setter
    def is_removable(self, value):
        pass

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        pass

    @property
    def represented_object(self):
        return self.__represented_object

    @represented_object.setter
    def represented_object(self, value):
        pass

    def draw_rect(self, rect: QRect):
        pass

    @property
    def is_dragging(self):
        return self.__is_dragging

    def track_mouse(self, event: QMouseEvent, adding: bool) -> bool:
        return False

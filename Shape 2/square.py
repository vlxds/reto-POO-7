from .rectangle import Rectangle
from .point import Point


class Square(Rectangle):
    def __init__(self, method: int = 1, point: Point = None, center: Point = None,
                 side: float = 0.0, point1: Point = None, point2: Point = None,
                 lines: list = None):

        if method == 4 and lines is not None:
            lengths = [line.length for line in lines]
            if not all(abs(l - lengths[0]) < 0.001 for l in lengths):
                raise ValueError("Para un cuadrado, todas las líneas deben tener la misma longitud")
            super().__init__(method=4, lines=lines)

        elif method == 1:
            super().__init__(method=1, point=point, width=side, height=side)

        elif method == 2:
            super().__init__(method=2, center=center, width=side, height=side)

        elif method == 3:
            if point1 is None:
                point1 = Point(0, 0)
            if point2 is None:
                point2 = Point(1, 1)

            width = abs(point2.x - point1.x)
            height = abs(point2.y - point1.y)
            side_length = max(width, height)

            center_x = (point1.x + point2.x) / 2
            center_y = (point1.y + point2.y) / 2

            super().__init__(method=2, center=Point(center_x, center_y),
                             width=side_length, height=side_length)

        self._is_regular = True
from .shape import Shape
from .point import Point
from .line import Line

class Rectangle(Shape):
    def __init__(self, method: int = 1, point: Point = None, center: Point = None,
                 width: float = 0.0, height: float = 0.0,
                 point1: Point = None, point2: Point = None,
                 lines: list = None):
        super().__init__()

        if method == 1:
            if point is None:
                point = Point(0, 0)
            self._width = width
            self._height = height
            self._center = Point(point.x + self._width / 2, point.y + self._height / 2)
            bottom_left = point

        elif method == 2:
            if center is None:
                center = Point(0, 0)
            self._center = center
            self._width = width
            self._height = height
            bottom_left = Point(center.x - width / 2, center.y - height / 2)

        elif method == 3:
            if point1 is None:
                point1 = Point(0, 0)
            if point2 is None:
                point2 = Point(1, 1)
            self._width = abs(point2.x - point1.x)
            self._height = abs(point2.y - point1.y)
            center_x = (point1.x + point2.x) / 2
            center_y = (point1.y + point2.y) / 2
            self._center = Point(center_x, center_y)
            bottom_left = Point(min(point1.x, point2.x), min(point1.y, point2.y))

        elif method == 4 and lines is not None:
            if len(lines) != 4:
                raise ValueError("Se requieren exactamente 4 líneas para formar un rectángulo")
            self._edges = lines
            self._width = lines[0].length
            self._height = lines[1].length
            bottom_left = lines[0].start_point
            top_right = lines[2].end_point
            center_x = (bottom_left.x + top_right.x) / 2
            center_y = (bottom_left.y + top_right.y) / 2
            self._center = Point(center_x, center_y)

        else:
            raise ValueError("Error, seleccionar método 1, 2, 3, o 4")

        bottom_right = Point(bottom_left.x + self._width, bottom_left.y)
        top_right = Point(bottom_left.x + self._width, bottom_left.y + self._height)
        top_left = Point(bottom_left.x, bottom_left.y + self._height)

        self._vertices = [bottom_left, bottom_right, top_right, top_left]

        if method != 4:
            self._edges = [
                Line(bottom_left, bottom_right),
                Line(bottom_right, top_right),
                Line(top_right, top_left),
                Line(top_left, bottom_left)
            ]

        self._inner_angles = [90.0, 90.0, 90.0, 90.0]
        self._is_regular = (abs(self._width - self._height) < 0.001)

    def get_width(self):
        return self._width

    def set_width(self, value):
        self._width = value

    def get_height(self):
        return self._height

    def set_height(self, value):
        self._height = value

    def get_center(self):
        return self._center

    def set_center(self, value):
        self._center = value

    def compute_area(self) -> float:
        return self._width * self._height

    def compute_perimeter(self) -> float:
        return sum(line.length for line in self._edges)

    def compute_inner_angles(self):
        return self._inner_angles

    def compute_interference_point(self, point: Point) -> bool:
        left = self._center.x - self._width / 2
        right = self._center.x + self._width / 2
        bottom = self._center.y - self._height / 2
        top = self._center.y + self._height / 2
        return left <= point.x <= right and bottom <= point.y <= top
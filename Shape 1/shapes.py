import math


class Point():
    definition: str = "Entidad geometrica abstracta que representa una ubicación en un espacio."

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def move(self, new_x: float, new_y: float):
        self.x = new_x
        self.y = new_y

    def reset(self):
        self.x = 0
        self.y = 0

    def compute_distance(self, point: "Point") -> float:
        distance = ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5
        return distance


class Line():
    def __init__(self, start_point: Point, end_point: Point):
        self.start_point = start_point
        self.end_point = end_point
        self.length = self.compute_length()

    def compute_length(self) -> float:
        length = ((self.end_point.x - self.start_point.x) ** 2 +
                  (self.end_point.y - self.start_point.y) ** 2) ** 0.5
        return length

    def compute_slope(self) -> float:
        if self.end_point.x - self.start_point.x == 0:
            return float('inf')
        slope = (self.end_point.y - self.start_point.y) / (self.end_point.x - self.start_point.x)
        angle_rad = math.atan(slope)
        angle_deg = math.degrees(angle_rad)
        return angle_deg


class Shape():
    def __init__(self):
        self.is_regular = False
        self.vertices = []
        self.edges = []
        self.inner_angles = []

    def compute_area(self):
        raise NotImplementedError("Debe implementarse en las subclases")

    def compute_perimeter(self):
        return sum(edge.length for edge in self.edges)

    def compute_inner_angles(self):
        raise NotImplementedError("Debe implementarse en las subclases")


class Triangle(Shape):
    def __init__(self, vertices: list):
        super().__init__()
        if len(vertices) != 3:
            raise ValueError("Un triángulo debe tener exactamente 3 vértices")

        self._vertices = vertices
        self._edges = [
            Line(vertices[0], vertices[1]),
            Line(vertices[1], vertices[2]),
            Line(vertices[2], vertices[0])
        ]
        self._inner_angles = self.compute_inner_angles()
        self._check_if_regular()

    def _check_if_regular(self):
        lengths = [edge.length for edge in self._edges]
        self._is_regular = all(abs(l - lengths[0]) < 0.001 for l in lengths)

    def compute_area(self):
        s = self.compute_perimeter() / 2 # Fórmula de Herón
        a, b, c = [edge.length for edge in self._edges]
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return area

    def compute_inner_angles(self):
        a, b, c = [edge.length for edge in self._edges]
        angle_A = math.degrees(math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))
        angle_B = math.degrees(math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)))
        angle_C = 180 - angle_A - angle_B

        return [angle_A, angle_B, angle_C]


class Isosceles(Triangle):
    def __init__(self, vertices: list):
        super().__init__(vertices)
        if not self._is_isosceles():
            raise ValueError("Los vértices no forman un triángulo isósceles")

    def _is_isosceles(self):
        lengths = sorted([edge.length for edge in self._edges])
        return (abs(lengths[0] - lengths[1]) < 0.001 or
                abs(lengths[1] - lengths[2]) < 0.001)


class Equilateral(Triangle):
    def __init__(self, vertices: list):
        super().__init__(vertices)
        if not self._is_regular:
            raise ValueError("Los vértices no forman un triángulo equilátero")


class Scalene(Triangle):
    def __init__(self, vertices: list):
        super().__init__(vertices)
        if not self._is_scalene():
            raise ValueError("Los vértices no forman un triángulo escaleno")

    def _is_scalene(self):
        lengths = [edge.length for edge in self._edges]
        return (abs(lengths[0] - lengths[1]) > 0.001 and
                abs(lengths[1] - lengths[2]) > 0.001 and
                abs(lengths[0] - lengths[2]) > 0.001)


class TriRectangle(Triangle):
    def __init__(self, vertices: list):
        super().__init__(vertices)
        if not self._has_right_angle():
            raise ValueError("Los vértices no forman un triángulo rectángulo")

    def _has_right_angle(self):
        return any(abs(angle - 90) < 0.1 for angle in self._inner_angles)


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
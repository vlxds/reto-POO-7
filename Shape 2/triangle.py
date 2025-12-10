import math
from .shape import Shape
from .line import Line
import time


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {end - start:.6f} s")
        return result
    return wrapper


class Rectangle(Shape):
    def __init__(self, vertices: list):
        super().__init__()
        if len(vertices) != 4:
            raise ValueError("Un rectángulo debe tener exactamente 4 vértices")

        self._vertices = vertices
        self._edges = [
            Line(vertices[0], vertices[1]),
            Line(vertices[1], vertices[2]),
            Line(vertices[2], vertices[3]),
            Line(vertices[3], vertices[0])
        ]
        self._inner_angles = self.compute_inner_angles()
        self._check_if_regular()

    def _check_if_regular(self):
        lengths = [edge.length for edge in self._edges]
        self._is_regular = abs(lengths[0] - lengths[1]) < 0.001

    @timeit
    def compute_area(self):
        base = self._edges[0].length
        height = self._edges[1].length
        return base * height

    def compute_inner_angles(self):
        return [90, 90, 90, 90]

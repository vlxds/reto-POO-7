import math
from .point import Point

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


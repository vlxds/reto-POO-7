class Shape():

    shape_type = "generic"

    def __init__(self):
        self._is_regular = False
        self._vertices = []
        self._edges = []
        self._inner_angles = []

    @property
    def is_regular(self):
        return self._is_regular

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    @property
    def inner_angles(self):
        return self._inner_angles

    @classmethod
    def set_shape_type(cls, new_type):
        cls.shape_type = new_type

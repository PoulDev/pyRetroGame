class Vector2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self) -> str:
        return f'<Vector2 ({self.x}, {self.y})>'

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, vectorObj):
        vector = Vector2(0,0)
        vector.x += vectorObj.x
        vector.y += vectorObj.y
        return vector

    def __sub__(self, vectorobj):
        self.x -= vectorobj.x
        self.y -= vectorobj.y
        return self

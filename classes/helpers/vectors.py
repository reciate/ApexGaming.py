import math

class Vector3:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

    def subtract(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z

    def multiply(self, vector):
        self.x *= vector.x
        self.y *= vector.y
        self.z *= vector.z

    def divide(self, vector):
        self.x /= vector.x
        self.y /= vector.y
        self.z /= vector.z

    def magnitude(self):
        return math.sqrt(self.x **2 + self.y **2 + self.z **2)

    def array(self):
        return [self.x, self.y, self.z]

class Vector2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def subtract(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def multiply(self, vector):
        self.x *= vector.x
        self.y *= vector.y

    def divide(self, vector):
        self.x /= vector.x
        self.y /= vector.y

    def magnitude(self):
        return math.sqrt(self.x **2 + self.y **2)

    def array(self):
        return [self.x, self.y]
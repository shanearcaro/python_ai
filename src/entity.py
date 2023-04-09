class Entity:
    width = 10
    height = 10

    def __init__(self, x: int, y: int, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color

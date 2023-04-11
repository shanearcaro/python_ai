from direction import Direction

class Entity:
    """A single unit within a Snake"""
    def __init__(self, x: int, y: int, size: int, color: tuple[int, int, int] = (255, 255, 255)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.next: Entity | None = None

    def get_position(self) -> tuple[int, int]:
        """Get the current x and y position of an entity"""
        return self.x, self.y

    def update_position(self, x: int, y: int) -> None:
        """Update the x and y position of an entity"""
        self.x = x
        self.y = y

    def update_position_direction(self, direction: Direction) -> None:
        """
        Update the position of the entity based on direction. This should only be called
        on the head entity of a snake object. The rest of the position updates will be propagated
        """
        if direction == Direction.NORTH:
            self.y -= self.size
        elif direction == Direction.SOUTH:
            self.y += self.size
        elif direction == Direction.EAST:
            self.x += self.size
        elif direction == Direction.WEST:
            self.x -= self.size

    def __str__(self) -> str:
        return f'x: {self.x}, y: {self.y}'

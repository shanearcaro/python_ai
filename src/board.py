import entity
import random
from enum import Enum

class Direction(Enum):
    NONE = 1
    NORTH = 2
    SOUTH = 3
    EAST = 4
    WEST = 5

class Board:
    def __init__(self, width: int, height: int, dimension: int):
        self.width = width
        self.height = height
        self.dimension = dimension
        self.head = entity.Entity(
            x=width / dimension // 2 * dimension,
            y=height / dimension // 2 * dimension,
            color=(255, 255, 0)
        )
        self.body = [self.head]
        self.direction = Direction.NONE
        self.spawn_apple()

    def set_direction(self, direction):
        """Update the direction of the head entity"""
        self.direction = direction

    def _move_in_direction(self):
        """Move head in the direciton"""
        if self.direction == Direction.NORTH:
            self.head.y -= self.dimension
        elif self.direction == Direction.SOUTH:
            self.head.y += self.dimension
        elif self.direction == Direction.EAST:
            self.head.x += self.dimension
        elif self.direction == Direction.WEST:
            self.head.x -= self.dimension

    def update_positions(self):
        """Update positions of snake in reverse"""
        for index in range(len(self.body) - 1, 0, -1):
            node = self.body[index]

            # Set current position to previous node position
            node.x = self.body[index - 1].x
            node.y = self.body[index - 1].y

        # Move head after updating all other positions
        self._move_in_direction()

    def detect_collisions(self, current: entity.Entity, other: entity.Entity):
        """Detect if two entities collide"""
        if current == other:
            return False
        return current.x == other.x and current.y == other.y

    def detect_boundaries(self):
        """Detect if the head is out of bounds"""
        return self.head.x >= self.width or self.head.x < 0 or self.head.y >= self.height or self.head.y < 0

    def reset(self):
        """Reset the board to its initial state"""
        self.head.x = self.width / self.dimension // 2 * self.dimension
        self.head.y = self.height / self.dimension // 2 * self.dimension

        self.body = [self.head]
        self.direction = Direction.NONE
        self.spawn_apple()

    def position_available(self, x, y):
        """Find where the apple can spawn"""
        for node in self.body:
            if (node.x == x or node.y == y):
                return False
        return True

    def spawn_apple(self):
        x_range = self.width / self.dimension - 1
        y_range = self.height / self.dimension - 1

        x = random.randint(0, x_range)
        y = random.randint(0, y_range)

        while (not self.position_available(x, y)):
            x = random.randint(0, x_range)
            y = random.randint(0, y_range)

        x *= self.dimension
        y *= self.dimension

        self.apple = entity.Entity(x=x, y=y, color=(255, 0, 0))

    def spawn_entity(self):
        ent = entity.Entity(-self.dimension, -self.dimension)
        self.body.append(ent)
        self.spawn_apple()

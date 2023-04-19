from entity import Entity
from direction import Direction

import random

class Snake:
    def __init__(self, head: Entity):
        self.head = head
        self.tail = head
        self.body = [head]
        self.is_alive = True
        self.size = self.head.size
        self.length = 1

        self.apple = Entity(-self.size, -self.size, self.size, (255, 0, 0))

        self.width: int | None = None
        self.height: int | None = None

        self.energy = 100

    def reset_energy(self):
        self.energy = min(100 + self.length * 5, 250)

    def set_boundaries(self, width: int, height: int) -> None:
        """Define the playable area for the snake"""
        self.width = width
        self.height = height

    def in_bounds(self) -> bool:
        """Verify the head is in bounds"""
        # Width and height must be implemented
        if self.width is None or self.height is None:
            raise NotImplementedError("Set the width and height boundaries")

        # Check that head is within the bounds
        x, y = self.head.get_position()
        return 0 <= x < self.width and 0 <= y < self.height

    def update(self, direction: Direction) -> None:
        """Update snake position on direction"""
        # Get the current head position
        current_x, current_y = self.head.get_position()

        # Update the location of head based on direction
        self.head.update_position_direction(direction=direction)

        # Verify head is within boundaries
        if not self.in_bounds():
            self.is_alive = False
            return

        # Verify head has not collided with body
        if self.check_collision_with_body():
            self.is_alive = False
            return

        next = self.head.next
        while next:
            # Record position of next element
            temp_x, temp_y = next.get_position()

            # Update element and current position
            next.update_position(current_x, current_y)
            current_x, current_y = temp_x, temp_y

            # Continue iteration
            next = next.next

    def check_collision_with_body(self) -> bool:
        """Check if the head collides with any part of the body"""
        for index in range(1, len(self.body)):
            # Skip first element since it will always be the head
            element = self.body[index]

            if self.head.get_position() == element.get_position():
                return True
        return False

    def is_position_free(self, x: int, y: int) -> bool:
        """Check if a position is available"""
        for entity in self.body:
            if entity.x == x and entity.y == y:
                return False
        return True

    def check_collision_with_apple(self):
        """Verify head collision with apple"""
        return self.head.get_position() == self.apple.get_position()

    def spawn_apple(self):
        """Find a location for and spawn the apple"""
        # Width and height must be implemented
        if self.width is None or self.height is None:
            raise NotImplementedError("Set the width and height boundaries")

        # Possible locations
        locations = []

        # O(n^2), not the best
        for x in range(0, self.width, self.size):
            for y in range(0, self.height, self.size):
                if self.is_position_free(x, y):
                    locations.append((x, y))

        # Set new position
        if len(locations) == 0:
            self.is_alive = False
        new_x, new_y = locations[random.randint(0, len(locations) - 1)]
        self.apple.update_position(new_x, new_y)

    def reset(self) -> None:
        """Set snake to its default state"""
        self.is_alive = True
        self.body = [self.head]

        self.tail = self.head
        self.head.next = None
        self.length = 1

        self.spawn_apple()

    def add_element(self) -> None:
        """Add element to Snake"""
        # Create offscreen entity
        entity = Entity(x=-self.size, y=-self.size, size=self.size)

        # Add entity to tail
        self.tail.next = entity
        self.tail = self.tail.next

        # Add element to body
        self.body.append(entity)
        self.length += 1

    def __str__(self) -> str:
        output = ''
        for entity in self.body:
            output += entity.__str__() + '\n'
        return output

from components.snake import Snake
from components.entity import Entity
from components.direction import Direction

snake = Snake(Entity(0, 0))
snake.add_element(Entity(0, 0))
snake.add_element(Entity(0, 0))

snake.update(Direction.SOUTH)
snake.update(Direction.SOUTH)
snake.update(Direction.SOUTH)
snake.update(Direction.EAST)

print(snake)

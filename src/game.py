import pygame

from snake import Snake
from direction import Direction
from entity import Entity

# Need to initialize pygame before useage
pygame.init()

# Screen variables
width, height = 820, 820
screen = pygame.display.set_mode((width, height))

# Game loop variables
clock = pygame.time.Clock()
running = True

# Snake starting position
start_x, start_y = 400, 400

# Create the snake
snake = Snake(Entity(start_x, start_y, 20))
snake.set_boundaries(width, height)

# Spawn the apple
snake.spawn_apple()

# Stops snake from moving initially
direction = Direction.NONE

# Game loop
while running:
    for event in pygame.event.get():
        # Window has been exited
        if event.type == pygame.QUIT:
            running = False

    # Color the entire screen black
    screen.fill('black')

    # Perform game logic
    keys = pygame.key.get_pressed()

    # Set direction based on keys pressed
    if keys[pygame.K_w]:
        direction = Direction.NORTH
    elif keys[pygame.K_s]:
        direction = Direction.SOUTH
    elif keys[pygame.K_d]:
        direction = Direction.EAST
    elif keys[pygame.K_a]:
        direction = Direction.WEST

    # Update head location
    snake.update(direction)

    # Check if the snake eats the apple
    if snake.check_collision_with_apple():
        snake.spawn_apple()
        snake.add_element()

    # If the snake is dead reset
    if not snake.is_alive:
        direction = Direction.NONE
        snake.reset()
        snake.head.update_position(start_x, start_y)

    # Render game here
    for entity in snake.body:
        pygame.draw.rect(screen, entity.color, (entity.x, entity.y, entity.size - 1, entity.size - 1))

    # Render apple
    pygame.draw.rect(screen, snake.apple.color, (snake.apple.x, snake.apple.y, snake.size, snake.size))

    # Update the screen and advance
    pygame.display.update()
    clock.tick(18)

# Game has been exited
pygame.quit()

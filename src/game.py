import pygame
from board import Board, Direction
import neat
import os

# Screen size
width = height = 410
dimension = 10

# Create the board for snake
board = Board(width, height, dimension)

# Start pygame and initialize screen
pygame.init()
screen = pygame.display.set_mode((width, height))

# Set the screen dimensions
clock = pygame.time.Clock()
running = True

# Game loop
while running:
    # Check if player quits game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a black background
    screen.fill("black")

    # Draw the snake
    for node in board.body:
        pygame.draw.rect(
            surface=screen,
            color=node.color,
            rect=(node.x, node.y, board.dimension, board.dimension)
        )

    # Draw the apple
    pygame.draw.rect(surface=screen,
                     color=board.apple.color,
                     rect=(board.apple.x, board.apple.y, board.dimension, board.dimension)
                     )

    # Get the pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        board.set_direction(direction=Direction.NORTH)
    elif keys[pygame.K_s]:
        board.set_direction(direction=Direction.SOUTH)
    elif keys[pygame.K_d]:
        board.set_direction(direction=Direction.EAST)
    elif keys[pygame.K_a]:
        board.set_direction(direction=Direction.WEST)

    board.update_positions()

    # This is such a bad way of doing it lol O(n^2)
    if len(board.body) != 1:
        for current in range(0, len(board.body)):
            for target in range(current, len(board.body)):
                if board.detect_collisions(board.body[current], board.body[target]):
                    board.reset()
                    break

    # Detect if head is colliding
    if board.detect_collisions(board.head, board.apple):
        board.spawn_entity()

    # Detect is head is out of bounds
    if board.detect_boundaries():
        board.reset()

    pygame.display.flip()
    clock.tick(18)

pygame.quit()

def evaluate(genomes, config):
    pass

def start(config):
    # Restore checkpoint
    # population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1')

    # Create initial population
    population = neat.Population(config)

    # Report neat statistics to console
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Save progress on each iteration
    population.add_reporter(neat.Checkpointer(1))

    best = population.run(evaluate, 50)

if __name__ == "main":
    directory = os.path.dirname(__file__)
    config_path = os.path.join(directory, "config.Config")

    config = neat.Config(neat.DefaultGenome,
                         neat.DefaultReproduction,
                         neat.DefaultSpeciesSet,
                         neat.DefaultStagnation,
                         filename=config_path
                         )
    start(config)

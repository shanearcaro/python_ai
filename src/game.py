import pygame

from snake import Snake
from direction import Direction
from entity import Entity
import neat
import math

class Game:
    def __init__(self,
                 width: int = 820,
                 height: int = 820,
                 size: int = 20,
                 start_x: int = 400,
                 start_y: int = 400,
                 fps: int = 18):
        # Need to initialize pygame before useage
        pygame.init()

        # Set screen variables
        self.width = width
        self.height = height
        self.size = size
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Snake starting position
        self.start_x = start_x
        self.start_y = start_y

        # Game loop variables
        self.clock = pygame.time.Clock()
        self.is_alive = True
        self.fps = fps
        self.moves = 0

        # Create the snake
        self.snake = Snake(Entity(self.start_x, self.start_y, self.size))
        self.snake.set_boundaries(self.width, self.height)

        # Spawn the apple
        self.snake.spawn_apple()
        # self.snake.apple.x = 400
        # self.snake.apple.y = 100

        # Stops snake from moving initially
        self.direction = Direction.NONE

    def distance(self, head: Entity, apple: Entity):
        head_center = (head.x + head.size / 2, head.y + head.size / 2)
        apple_center = (apple.x + apple.size / 2, apple.y + apple.size / 2)

        dx = apple_center[0] - head_center[0]
        dy = apple_center[1] - head_center[1]

        return math.sqrt(dx**2 + dy**2)

    def angle(self, head: Entity, apple: Entity):
        head_center = (head.x + head.size / 2, head.y + head.size / 2)
        apple_center = (apple.x + apple.size / 2, apple.y + apple.size / 2)

        dx = apple_center[0] - head_center[0]
        dy = apple_center[1] - head_center[1]

        return math.atan2(dy, dx)

    def take_action(self, action):
        """Provide an action to the game"""
        if action == 0 and self.direction != Direction.SOUTH:
            self.direction = Direction.NORTH
        if action == 1 and self.direction != Direction.NORTH:
            self.direction = Direction.SOUTH
        if action == 2 and self.direction != Direction.WEST:
            self.direction = Direction.EAST
        if action == 3 and self.direction != Direction.EAST:
            self.direction = Direction.WEST

        self.snake.update(self.direction)
        self.moves += 1
        self.snake.energy -= 1

    def get_state(self):
        distances = self.get_wall_distance()
        return (self.angle(self.snake.head, self.snake.apple),
                distances[0], distances[1], distances[2], distances[3])

    def draw_game(self):
        """Render the snake body and apple"""
        # Render game here
        for entity in self.snake.body:
            pygame.draw.rect(self.screen, entity.color, (entity.x, entity.y, entity.size - 1, entity.size - 1))

        # Render apple
        pygame.draw.rect(self.screen, self.snake.apple.color,
                         (self.snake.apple.x, self.snake.apple.y, self.snake.size, self.snake.size))

    def fitness(genomes, config):
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            game = Game()  # Create a new game instance for each genome

            # Play the game and get the final score
            while game.snake.is_alive:
                inputs = game.get_state()
                output = net.activate(inputs)
                action = output.index(max(output))
                game.take_action(action)

            # Calculate the fitness score
            fitness_score = game.snake.length * 1000 + game.moves * 1

            if not game.snake.is_alive:
                fitness_score -= 1000

            genome.fitness = fitness_score

    def get_wall_distance(self):
        snake_head = self.snake.head
        left_distance = snake_head.x
        right_distance = self.width - snake_head.x - self.size
        up_distance = snake_head.y
        down_distance = self.height - snake_head.y - self.size

        # Loop snake and find entities blocking path to wall
        for entity in self.snake.body:
            if entity == self.snake.head:
                continue
            if entity.y == snake_head.y:
                if entity.x < snake_head.x:
                    left_distance = min(left_distance, snake_head.x - entity.x)
                else:
                    right_distance = min(right_distance, entity.x - snake_head.x)
            elif entity.x == snake_head.x:
                if entity.y < snake_head.y:
                    up_distance = min(up_distance, snake_head.y - entity.y)
                else:
                    down_distance = min(down_distance, entity.y - snake_head.y)

        return up_distance, down_distance, right_distance, left_distance

    def human_play(self):
        # Game loop
        while self.is_alive:
            for event in pygame.event.get():
                # Window has been exited
                if event.type == pygame.QUIT:
                    self.is_alive = False

            if self.direction != Direction.NONE:
                self.moves += 1
                self.snake.energy -= 1

            # Color the entire screen black
            self.screen.fill('black')

            # Perform game logic
            keys = pygame.key.get_pressed()

            # Set direction based on keys pressed
            if keys[pygame.K_w]:
                self.direction = Direction.NORTH
            elif keys[pygame.K_s]:
                self.direction = Direction.SOUTH
            elif keys[pygame.K_d]:
                self.direction = Direction.EAST
            elif keys[pygame.K_a]:
                self.direction = Direction.WEST

            # Update head location
            self.snake.update(self.direction)
            # print(self.distance_to_wall())
            print("State:", self.get_state())
            print("Fitness:", self.fitness(self.get_state()))

            # Check if the snake eats the apple
            if self.snake.check_collision_with_apple():
                self.snake.spawn_apple()
                self.snake.reset_energy()
                self.snake.add_element()

            if self.snake.energy == 0:
                self.snake.is_alive = False
                self.snake.reset_energy()

            # If the snake is dead reset
            if not self.snake.is_alive:
                self.direction = Direction.NONE
                self.snake.reset()
                self.snake.head.update_position(self.start_x, self.start_y)
                self.moves = 0

            # Render the game
            self.draw_game()

            # Update the screen and advance
            pygame.display.update()
            self.clock.tick(self.fps)

        # Game has been exited
        pygame.quit()

# game = Game()
# game.human_play()

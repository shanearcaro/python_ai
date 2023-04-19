import neat
from game import Game
from direction import Direction
import pygame
import os
import pickle

def save_generation(generation, generation_num, save_folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Save the generation to a file
    filename = os.path.join(save_folder, f"generation_{generation_num}.pkl")
    with open(filename, "wb") as f:
        pickle.dump(generation, f)

def fitness(genome, config):
    # Create a game object
    game = Game()

    # Create a neural network using the genome and configuration
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    # Run the game with the neural network as the controller
    while game.snake.is_alive:
        for event in pygame.event.get():
            # Window has been exited
            if event.type == pygame.QUIT:
                game.is_alive = False
                break

        # Color the entire screen black
        game.screen.fill('black')

        inputs = game.get_state()
        # print("Input:", inputs)
        output = net.activate(inputs)
        action = output.index(max(output))
        game.take_action(action)

        # Check if the snake eats the apple
        if game.snake.check_collision_with_apple():
            game.snake.spawn_apple()
            game.snake.reset_energy()
            game.snake.add_element()

        modifier = 0 if game.snake.in_bounds() else 1000

        if game.snake.energy == 0:
            game.snake.is_alive = False
            modifier = 500

        game.draw_game()
        pygame.display.update()
        game.clock.tick(game.fps)

    # Calculate the fitness of the genome
    fitness_score = game.snake.length * 600 + game.moves * 50 - modifier - (game.distance(game.snake.head, game.snake.apple) / 2)

    return fitness_score

def evaluate_genomes(genomes, config):
    for genome_id, genome in genomes:
        fitness_score = fitness(genome, config)
        genome.fitness = fitness_score
        print("Genome:", genome_id, "Fitness:", fitness_score)

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(evaluate_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

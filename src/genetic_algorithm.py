"""
Genetic algorithm has 5 phases:
    1. initial population
    2. evaluation
    3. selection
    4. crossover
    5. mutation
"""

from gene import Gene
from population import Population
import time
import random


class GeneticAlgorithm:
    def __init__(self, gene_length=5, population_size=100, crossover_rate=0.8, mutation_rate=0.01, target=None):
        self.target = target
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

        initial_population = Population(gene_length=gene_length, target=target)
        initial_population.init_random(population_size=population_size)
        self.generations = [initial_population]
        self.current_generation = 0
        self.gene_length = gene_length

    def train(self):
        generation = self.generations[self.current_generation]

        next_generation = Population(self.gene_length, self.target)

        while next_generation.population_size != generation.population_size:
            father = generation.roulette_wheel_selection()
            mother = generation.roulette_wheel_selection()

            print('Father:  ', father)
            print('Mother:  ', mother)

            if random.random() < self.crossover_rate:
                print('Crossover happening')
                son, daughter = father.crossover(mother)
                print('Son:     ', son)
                print('Daughter:', daughter)

                son.mutate(self.mutation_rate)
                daughter.mutate(self.mutation_rate)

                next_generation.add_chromosome(son, daughter)
                print(next_generation.__str__())
                print()

        self.generations.append(next_generation)
        self.current_generation += 1
        return

    def __str__(self):
        ret = ''
        for index, gen in enumerate(self.generations):
            ret += f'Generation {index}:' + '\n'
            ret += str(gen)
        return ret

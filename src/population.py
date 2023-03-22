from __future__ import annotations
import random
import math

from gene import Gene
from chromosome import Chromosome


class Population:
    def __init__(self, gene_length=5, target: Chromosome = None):
        self.gene_length = gene_length

        # Generate initial target value if empty
        if target is None:
            self.target = [Gene('1') for _ in range(self.gene_length)]

        self.chromosomes: list[Chromosome] = []
        self.population_size = len(self.chromosomes)

    def add_chromosome(self, *args):
        """Append a chromosome to the population"""

        for element in args:
            if type(element) != Chromosome:
                raise ValueError('Elements must be of type chromosome')
        self.chromosomes.append(args)
        self.population_size = len(self.chromosomes)

    def del_chromosome(self, index):
        """Delete a chromosome from the population"""
        chromosome = self.chromosomes.pop(index)
        self.population_size = len(self.chromosomes)
        return chromosome

    def calculate_fitness(self):
        """Calculate the fitness for every chromosome within the population"""
        for chromosome in self.chromosomes:
            chromosome.calculate_fitness(self.target)

    def average_fitness(self):
        """Get the average fitness for this population"""
        total_fitness = 0.0
        for chromosome in self.chromosomes:
            total_fitness += chromosome.fitness
        return total_fitness / self.population_size

    def init_random(self, population_size=10, override=False):
        """Generated a random initial population"""
        # Verify initial population can be generated
        if len(self.chromosomes):
            if override:
                self.chromosomes = []
            else:
                raise AttributeError("Chromosomes must be empty to"
                                     "create a random population without the override flag")

        # Set population size
        self.population_size = population_size

        # Generate random chromosomes
        self.chromosomes = [Chromosome(length=self.gene_length) for _ in range(population_size)]

    def roulette_wheel_selection(self):
        """Routlette Wheel Selection for single parent"""
        # Calculate total fitness and fixed routless position
        print('Length:', len(self.chromosomes))

        total_fitness = sum([chromosome.fitness for chromosome in self.chromosomes])
        fixed_point = random.random() * total_fitness

        print('Total fitness:', total_fitness)
        print('Fixed point:', fixed_point)
        print()

        parent_index = 0
        partial_fitness = 0

        # Iterate chromosomes list updating partial fitness
        for index, chromosome in enumerate(self.chromosomes):
            partial_fitness += chromosome.fitness

            # Select parent
            if partial_fitness > fixed_point:
                parent_index = index - 1
                break

        return self.chromosomes[parent_index]

    def tournament_selection(self, k=3):
        """Tournament Selection for single parent"""

        # Generate a k length of random candidates
        candidates = [self.chromosomes[random.randint(0, self.population_size)] for _ in range(k)]

        # Determine the best candidate of those randomly selected
        best_candidate = 0
        for index in range(1, k):
            if candidates[k].fitness > candidates[best_candidate].fitness:
                best_candidate = index

        return candidates[best_candidate]

    def __str__(self):
        ret = ''
        for chromosome in self.chromosomes:
            ret += str(chromosome) + '\n'
        return ret

from chromosome import Chromosome
from population import Population

import random


class GeneticAlgorithm:
    """Genetic Algorithm to optimize a binary string"""
    def __init__(self, gene_length=10, population_size=3, crossover_rate=0.8, mutation_rate=0.01):
        self.gene_length = gene_length
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generations = []

        self.crossover_count = 0
        self.mutation_count = 0

    def init_pop(self):
        """Generates the initial population for the algorithm."""

        # Create initial random population
        self.generations = [Population.from_random(self.gene_length, self.population_size)]

    def stochastic_sampling(self) -> Chromosome:
        """Stochastic Universal Sampling of population chromosomes"""
        gen = self.latest_generation()

        # Total population fitness and current target sample
        fitness = sum([chromosome.fitness for chromosome in gen.pool])
        sample = random.randint(0, fitness)

        # Speed up with binary search
        partial_fitness = 0
        for index, chromosome in enumerate(gen.pool):
            partial_fitness += chromosome.fitness

            # Evaluate current fitness against target sample
            if partial_fitness > sample:
                return gen.pool[index - 1]
        return gen.pool[-1]

    def next_generation(self, r=0, k=1):
        """
        Create the next generation using parents from the latest

        :param r: Number of top of the class chromosomes to be included into next generation
        :param k: Number of parents to use for generation the next generation
        """
        top_class = self.latest_generation().best_chromosomes(r=r)
        parents = self._select_parents(k)

        # Start with pool of most fit from previous generation
        new_pool = top_class
        count = 0
        # Continue adding to pool unit it reaches population size
        while len(new_pool) != self.population_size:
            # Generate two chromosomes
            father = parents.pool[random.randint(0, len(parents.pool) - 1)]
            mother = parents.pool[random.randint(0, len(parents.pool) - 1)]

            # Determine if parents should mate

            if random.random() > self.crossover_rate:
                # Add father to pool instead of child
                new_pool.append(father)
                continue

            # Add child to new gene pool
            new_pool.append(self.double_point_crossover(father, mother))
            self.crossover_count += 1

        # Mutate chromosomes in the new pool
        for chromosome in new_pool:
            self.mutation_count += chromosome.mutate(self.mutation_rate)
        self.generations.append(Population.from_source(new_pool))

    def single_point_crossover(self, father: Chromosome, mother: Chromosome) -> Chromosome:
        """Single point crossover with two parents"""
        crossover_point = random.randint(0, len(father.genes))

        # Create child with first part of father's genes and second part of mother's genes
        child = father.genes[:crossover_point].append(mother.genes[crossover_point:])
        return Chromosome(genes=child)

    def double_point_crossover(self, father: Chromosome, mother: Chromosome) -> Chromosome:
        """Double point crossover with two parents"""
        length = len(father.genes)

        # Generate two points on each half of the chromosome
        left_point = random.randint(0, length // 2)
        right_point = random.randint(length // 2, length)

        # First and third part of child is father, second part is mother
        child = father.genes[:left_point] + mother.genes[left_point:right_point] + father.genes[right_point:]
        return Chromosome(genes=child)

    def _select_parents(self, k) -> Population:
        """Select number of parents to initialize the next generation"""

        # Select k number of parents
        parents = [self.stochastic_sampling() for _ in range(k)]
        return Population.from_source(parents)

    def latest_generation(self):
        """Get the latest generation"""
        return self.generations[-1]

    def generation_count(self):
        """Get the number of created generations"""
        return len(self.generations)

    def print_fitness(self):
        """Regular str conversion with included fitness"""
        return "".join([population.print_fitness() + '\n' for population in self.generations])

    def __str__(self):
        return "".join([f'Generation: {index}' + '\n' + str(population) + '\n'
                        for index, population in enumerate(self.generations)])

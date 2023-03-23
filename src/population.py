from chromosome import Chromosome


class Population:
    """Representation of the search space for a specific generation of a genetic algorithm"""

    def __init__(self, gene_length=10, population_size=3):
        self.gene_length = gene_length
        self.population_size = population_size
        self.pool: list[Chromosome] = []

    def from_source(pool: list[Chromosome]):
        if not pool:
            raise ValueError('Pool cannot be empty')
        population = Population(gene_length=pool[0].gene_length, population_size=len(pool))
        population.pool = pool
        return population
    from_source = staticmethod(from_source)

    def from_random(gene_length=10, population_size=3):
        """Generate the population dna from random values"""
        p = Population(gene_length, population_size)
        p.pool = [Chromosome(p.gene_length) for _ in range(0, p.population_size)]
        return p
    from_random = staticmethod(from_random)

    def average_fitness(self):
        fitness = sum([chromosome.fitness for chromosome in self.pool])
        return fitness / self.population_size

    def best_chromosome(self) -> Chromosome:
        "Returns the chromosome with the best fitness"
        best_fitness = 0
        best_chromosome = None
        for chromosome in self.pool:
            if chromosome.fitness > best_fitness:
                best_fitness = chromosome.fitness
                best_chromosome = chromosome
        return best_chromosome

    def best_chromosomes(self, r) -> list[Chromosome]:
        """Return the top k chromosomes within a population"""
        chromosomes = sorted([chromosome for chromosome in self.pool], key=lambda x: x.fitness, reverse=True)
        return [c for c in chromosomes[:r]]

    def print_fitness(self):
        return "".join(str(chromosome) + ": " + str(chromosome.fitness) + '\n'
                       for chromosome in self.pool)

    def __str__(self):
        return "".join(str(chromosome) + '\n' for chromosome in self.pool)

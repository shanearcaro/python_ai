from chromosome import Chromosome


class Population:
    """Representation of the search space for a specific generation of a genetic algorithm"""

    def __init__(self, gene_length=10, population_size=3, target=None):
        self.gene_length = gene_length
        self.population_size = population_size
        self.dna: list[Chromosome] = []
        self.target = target

    def from_random(self):
        """Generate the population dna from random values"""
        self.dna = [Chromosome(self.gene_length) for _ in range(self.population_size)]

    # def crossover(self, father: Chromosome, mother: Chromosome):
    #     if father.gene_length != mother.gene_length:
    #         raise ValueError('Father and mother must be the same size')

    #     # Pick random, single crossover point
    #     crossover_point = random.randrange(0, len(father.genes))

    #     # Create children
    #     son = Chromosome(genes=father.snip(0, crossover_point) + mother.snip(crossover_point, len(mother.genes)))
    #     daughter = Chromosome(genes=mother.snip(0, crossover_point) + father.snip(crossover_point, len(father.genes)))

    #     # Return children elements
    #     return [son, daughter]

    def print_fitness(self, target):
        return "".join(str(chromosome) + ": " + str(chromosome.calculate_fitness(target=target)) + '\n'
                       for chromosome in self.dna)

    def __str__(self):
        return "".join(str(chromosome) + '\n' for chromosome in self.dna)

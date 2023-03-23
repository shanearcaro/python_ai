from gene import Gene
import random

class Chromosome:
    """Representation of a chromosome within a population"""
    fitness = 0

    def __init__(self, gene_length=10, genes: list[Gene] = []):
        self.genes = genes

        # Check if genes list is provided
        if self.genes:
            self.gene_length = len(self.genes)
        else:
            self.__randomize(gene_length=gene_length)
        self.fitness = 0
        self.calculate_fitness()

    def __randomize(self, gene_length=None):
        """Generate a chromosome with random genes"""
        if gene_length is None:
            if self.gene_length == 0:
                raise ValueError('Cannot generate a random chromosome with length 0')
        else:
            self.gene_length = gene_length

        # Generate the random genes
        self.genes = [Gene() for _ in range(self.gene_length)]

    def snip(self, low, high):
        """Snip a sequency of genes from a chromosome"""
        return self.genes[low:high]

    def mutate(self, rate: float):
        """Mutate a random gene on"""
        mutation_count = 0

        for index in range(len(self.genes)):
            if random.random() < rate:
                mutation_count += 1
                self.genes[index] = Gene('1')
        return mutation_count

    def calculate_fitness(self):
        """Calculate the fitness against a target"""
        if not self.genes:
            raise ValueError('Cannot calculate fitness for empty chromosome')

        self.fitness = [gene.allele for gene in self.genes].count('1')

    def __str__(self):
        return "".join([str(gene) for gene in self.genes])

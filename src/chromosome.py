from __future__ import annotations
import random

from gene import Gene


class Chromosome:
    """Represents an individual within a population"""

    def __init__(self, length=5, genes: list[Chromosome] = None):
        if genes:
            self.genes = genes
        else:
            self.genes = [Gene() for _ in range(length)]
        self.fitness = 0.0

    def calculate_fitness(self, target: Chromosome):
        """Calculate the fitness of this entity against a target"""
        # Verify target and chromosome have same length
        if len(self.genes) != len(target):
            raise ValueError(f'Target must be size {len(self.genes)}')
        
        self.fitness = sum([1 if self.genes[index].allele == str(target[index]) else 0
                            for index in range(0, len(self.genes))])
        
        print("Caulculated fitness:", self.fitness)

    def crossover(self, target: Chromosome):
        """Create two offspring entities"""
        # Calculate crossoverpoint
        crossover_point = random.randint(0, len(self.genes) - 1)
        print("Crossover point:", crossover_point)

        # Get father and mother switch points
        father_slice = self.genes[:crossover_point]
        mother_slice = target.genes[crossover_point:]

        print("Father slice:", "".join([e.allele for e in father_slice]))
        print("Mother slice:", "".join([e.allele for e in mother_slice]))

        # Generate two kids as offspring
        son = Chromosome(genes=mother_slice + self.genes[crossover_point:])
        daughter = Chromosome(genes=father_slice + target.genes[crossover_point:])

        return son, daughter

    def mutate(self, rate=0.01):
        """Mutate a random gene within a chromosome by the mutation rate"""
        for index in range(len(self.genes)):
            # If success, flip gene
            if random.random() < rate:
                self.genes[index].allele = '1' if self.genes[index].allele == '0' else '0'

    def __str__(self) -> str:
        ret = ''
        for gene in self.genes:
            ret += str(gene)
        return ret

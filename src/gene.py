import random


class Gene:
    """Representation of a single gene within a chromosome"""

    def __init__(self, allele=None):
        self.allele = allele if allele is not None else str(int(random.randint(0, 100) < 5))

    def __mul__(self, other: int):
        return [Gene(self.allele) for _ in range(other)]

    def __str__(self):
        return self.allele

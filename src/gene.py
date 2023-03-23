import random


class Gene:
    """Representation of a single gene within a chromosome"""

    def __init__(self, allel=None):
        self.allel = allel if allel is not None else str(random.randint(0, 1))

    def __str__(self):
        return self.allel

import random

class Gene:
    """Represents a single gene within a chromosome"""

    def __init__(self, allele: str = None):
        # Generate a random value for the allele
        if not allele:
            self.allele = str(random.randint(0, 1))
            return

        # Verify allele value
        if allele != '0' and allele != '1':
            raise ValueError('Allele must be a binary value')

        self.allele = allele

    def __str__(self):
        return self.allele

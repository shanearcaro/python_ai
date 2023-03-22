from gene import Gene
from chromosome import Chromosome
from population import Population
from genetic_algorithm import GeneticAlgorithm

ga = GeneticAlgorithm(gene_length=30,
                      population_size=3,
                      crossover_rate=0.8,
                      mutation_rate=0.01)

ga.generations[-1].calculate_fitness()
ga.train()
print(ga)


# ga = GeneticAlgorithm(gene_length=30, population_size=20)
# ga.generations[-1].calculate_fitness()

# print(ga)
# print(ga.generations[-1].average_fitness())

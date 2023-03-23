from gene import Gene
from chromosome import Chromosome
from population import Population

population = Population(gene_length=20, population_size=20)
population.from_random()

target = '1' * population.population_size

print(population.print_fitness(target=target))

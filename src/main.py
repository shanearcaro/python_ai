from gene import Gene
from genetic_algorithm import GeneticAlgorithm

# Length of chromosome
gene_length = 110

# Target for genetic algorithm
target = Gene('1') * gene_length

# Create the ga
ga = GeneticAlgorithm(gene_length=gene_length,
                      population_size=20,
                      crossover_rate=0.9,
                      mutation_rate=0.01)

# Generate initial population and print
ga.init_pop()
print(f'Generation[{ga.generation_count()}]: {ga.latest_generation().best_chromosome()}: '
      f'({ga.latest_generation().best_chromosome().fitness}) avg: {ga.latest_generation().average_fitness()}')

# While the latest generation is not optimal: train
while ga.latest_generation().best_chromosome().fitness != gene_length:
    # Train new generation
    ga.next_generation(r=int(ga.population_size * 0.1), k=int(ga.population_size * 0.4))

    # Print results
    print(f'Generation[{ga.generation_count()}]: {ga.latest_generation().best_chromosome()}: '
          f'({ga.latest_generation().best_chromosome().fitness}) avg: {ga.latest_generation().average_fitness()}')
print()

# Final generation count
print("Total number of generations:", ga.generation_count())

__author__ = 'Ralph F. Leyva'

import random
import pprint
import numpy as np
import matplotlib.pyplot as plt

'''
    Introduction to Genetic Algorithms - Problem #1:

        Implement a single GA with the fitness proportionate selection, roulette-
        wheel sampling, population size 100, single-point crossover rate pc = 0.7,
        and bitwise mutation rate pm = 0.001. Try it on the following fitness function:
        f(x) = number of ones in c, where x is a chromosome of length 20.
'''

# Script Globals
initial_population = []
avg_fitness = []
fitness_sum = 0
generation_cnt = 0

pm_array = np.zeros(1000, dtype = np.int)
pm_array[random.randint(0,999)] = 1
pc_array = np.array([1,1,1,1,1,1,1,0,0,0])

class Chromosome:
    def __init__(self, base_10_rep):
        self.base_10_rep = base_10_rep
        self.binary_rep = self.convert_to_binary_string(self.base_10_rep)
        self.fitness = self.calculate_fitness(self.binary_rep)

    def calculate_fitness(self, binary_str_val):
        return binary_str_val.count('1')

    def convert_to_binary_string(self, base_10_val):
        # Using the bin() function returns a '0b..." to the beginnning
        # of each value converted. We remove this by splicing and zero-pad
        # the chromosome.
        return bin(base_10_val)[2:].zfill(20)

    def mutate(self):
        # As the name suggests, this function will mutate the chromosome
        bit2flip = random.randint(0,(len(self.binary_rep)-1))
        if str(self.binary_rep[bit2flip]) == '1':
            self.binary_rep = self.binary_rep[0:bit2flip] + '0' + self.binary_rep[bit2flip+1:]
            self.base_10_rep = int(self.binary_rep, 2)
            self.fitness -= 1
        else:
            self.binary_rep = self.binary_rep[0:bit2flip] + '1' + self.binary_rep[bit2flip+1:]
            self.base_10_rep = int(self.binary_rep, 2)
            self.fitness += 1

    # Utility functions for printing
    def __str__(self):
        return "Value: %s  Chromosome: %s  Fitness: %s" % (self.base_10_rep, self.binary_rep, self.fitness)

    def __repr__(self):
        return "Value: %s  Chromosome: %s  Fitness: %s" % (self.base_10_rep, self.binary_rep, self.fitness)

def generate_population():
    # Generates the initial population of chromosomes
    # The high value contains the maximum value that 20-bits can hold
    global initial_population, fitness_sum, avg_fitness
    np.set_printoptions(suppress=True)

    for _ in xrange(100):
        x = Chromosome(np.random.randint(low=0, high=1048575))
        fitness_sum += x.fitness
        initial_population.append(x)

    avg_fitness.append(fitness_sum/100.0)
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(initial_population)

def roulette_wheel_sample():
    # Returns two chromosomes from the population to breed
    global inital_population
    pick = random.uniform(0,fitness_sum)
    current = 0
    for chromosome in initial_population:
        current += chromosome.fitness
        if(current > pick):
            return chromosome

def crossover(chromosome_1, chromosome_2):
    # Will crossover two chromosomes, returning two new chromosomes
    # The crossover point is randomly generated. Returns two new Chromosome objs.
    crossover_point = random.randint(0,len(chromosome_1.binary_rep)-1)
    return Chromosome(int(chromosome_1.binary_rep[0:crossover_point] + chromosome_2.binary_rep[crossover_point:],2)), \
           Chromosome(int(chromosome_2.binary_rep[0:crossover_point] + chromosome_1.binary_rep[crossover_point:],2))

def mutate_chromosome(chromosome):
    if random.choice(pm_array) == 1:
        chromosome.mutate()

def run_generation():
    global initial_population, generation_cnt, fitness_sum, avg_fitness
    temp_population = []

    while(len(temp_population) != 100):
        chromosome_x = roulette_wheel_sample()
        chromosome_y = roulette_wheel_sample()

        # Carry out mutation
        if(pm_array[random.randint(0,999)] == 1):
            mutate_chromosome(chromosome_x)
        if(pm_array[random.randint(0,999)] == 1):
            mutate_chromosome(chromosome_y)

        if(pc_array[random.randint(0,9)] == 1):
            # We carry out a crossover, otherwise the selected chromosomes
            # pass on to the other side.
            chromosome_x, chromosome_y = crossover(chromosome_x, chromosome_y)
            temp_population.append(chromosome_x)
            temp_population.append(chromosome_y)
        else:
            temp_population.append(chromosome_x)
            temp_population.append(chromosome_y)

    # Replaces previous generation with new generation
    initial_population = temp_population
    fitness_sum = 0

    for chromosome in initial_population:
        fitness_sum += chromosome.fitness

    avg_fitness.append(fitness_sum/100.0)
    #print 'Average Fitness: ' + str(avg_fitness)
    generation_cnt += 1

if __name__ == '__main__':
    generate_population()
    print 'Average Fitness: ' + str(avg_fitness[-1])

    while avg_fitness[-1] != 20:
        run_generation()
    print 'Final Generation Count: ' + str(generation_cnt) + '\n\n'
    print initial_population
    plt.plot(avg_fitness, 'ro')
    plt.ylabel('Average Fitness')
    plt.xlabel('Generation Count')
    print avg_fitness
    plt.show()

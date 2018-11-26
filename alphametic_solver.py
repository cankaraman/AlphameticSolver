from pyeasyga import pyeasyga
import random
import pdb

INPUT_DATA = "SEND+MORE=MONEY"


def parse_input():
    raw_arguments, result = INPUT_DATA.split("=")
    arguments = raw_arguments.split("+")

    return arguments, result

def parse_genetic_code():
    arguments, result = parse_input()

    chars = list("".join(arguments))
    chars.extend(list(result))
    genetic_code = []

    for char in chars:
        if char not in genetic_code:
            genetic_code.append(char)

    # print(genetic_code)
    return genetic_code

GENETIC_CODE = parse_genetic_code()

def generate_individual(data):
    individual = []

    while len(GENETIC_CODE) != len(individual):
        rnd_int = random.randint(0,9)
        if rnd_int not in individual:
            individual.append(rnd_int)
    return individual

def generate_genetic_dictionary(individual):

    individual = generate_individual(None)
    # pdb.set_trace()
    genom_dictionary = {}
    for char, value in zip(GENETIC_CODE, individual):
        genom_dictionary[char] = value

    #print(genom_dictionary)
    return genom_dictionary

def calc_fitness(individual, data):
    arguments, result = parse_input()
    data = generate_genetic_dictionary(individual)

    argument_total = 0
    for argument in arguments:
        argument_string = ""
        for char in argument:
            argument_string += str(data[char])
        argument_total += int(argument_string)

    result_string = ""
    for char in result:
        result_string += str(data[char])

    result_total = int(result_string)

    return abs(argument_total - result_total)
    #return argument_total, result_total

seed_data = generate_genetic_dictionary(generate_individual(None))

ga = pyeasyga.GeneticAlgorithm(seed_data,
                               population_size=10,
                               generations=20,
                               crossover_probability=0.8,
                               mutation_probability=0.05,
                               elitism=True,
                               maximise_fitness=False)

ga.create_individual = generate_individual
ga.fitness_function = calc_fitness
ga.run()
print(ga.best_individual())

#print(calc_fitness(generate_individual()))

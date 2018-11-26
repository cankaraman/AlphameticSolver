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

    return genetic_code


GENETIC_CODE = parse_genetic_code()


def generate_individual(data):
    individual = []

    while len(GENETIC_CODE) != len(individual):
        rnd_int = random.randint(0, 9)
        if rnd_int not in individual:
            individual.append(rnd_int)
    return individual


def generate_genetic_dictionary(individual):

    individual = generate_individual(None)
    genom_dictionary = {}
    for char, value in zip(GENETIC_CODE, individual):
        genom_dictionary[char] = value

    # print(genom_dictionary)
    return genom_dictionary


def calc_fitness(individual, data):

    debug = False

    arguments, result = parse_input()
    data = generate_genetic_dictionary(individual)

    # find sum of the arguments of the alphametic addition
    argument_total = 0
    for argument in arguments:
        argument_string = ""
        for char in argument:
            argument_string += str(data[char])
        if debug:
            print("args: ", argument_string)
        argument_total += int(argument_string)

    # find result of the alphametic addition
    result_string = ""
    for char in result:
        result_string += str(data[char])

    result_total = int(result_string)
    if debug:
        print("res: ", result_string, "\n", "fitness: ", abs(argument_total -
                                                             result_total), "\n\n")

    # return the absolute value of diffirence between the two. If it's close to
    # zero then individual has a good fitness
    return abs(argument_total - result_total)


def crossover_at_random_index(parent_1, parent_2):
    # crosovers at random index but doesn't repeat genes
    crossover_index = random.randrange(1, len(parent_1))

    child_1a = parent_1[:crossover_index]
    child_1b = []
    for i in parent_2:
        if i not in child_1a and len(child_1a) + len(child_1b) < len(parent_1):
            child_1b.append(i)
    child_1 = child_1a + child_1b

    child_2a = parent_2[crossover_index:]
    child_2b = []
    for i in parent_1:
        if i not in child_2a and len(child_2a) + len(child_2b) < len(parent_1):
            child_2b.append(i)
    child_2 = child_2a + child_2b

    return child_1, child_2


def mutate(individual):

    mutate_index = random.randrange(len(individual))
    mutation_val = random.randint(0, len(individual))

    # find a random value that is not in the individual genom
    while mutation_val in individual:
        mutation_val = random.randint(0, len(individual))

    individual[mutate_index] = mutation_val


seed_data = generate_genetic_dictionary(generate_individual(None))

ga = pyeasyga.GeneticAlgorithm(seed_data,
                               population_size=20,
                               generations=30,
                               crossover_probability=0.8,
                               mutation_probability=0.1,
                               elitism=True,
                               maximise_fitness=False)
ga.mutate_function = mutate
ga.create_individual = generate_individual
ga.fitness_function = calc_fitness
ga.crossover_function = crossover_at_random_index
ga.run()
print(ga.best_individual())

# print(calc_fitness(generate_individual()))

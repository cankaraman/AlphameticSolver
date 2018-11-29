from pyeasyga import pyeasyga
import random
import pdb

INPUT_DATA = "SEND+MORE=MONEY"


def parse_input():
    raw_arguments, result = INPUT_DATA.split("=")
    arguments = raw_arguments.split("+")

    return arguments, result


def parse_genetic_code():
    # parse unique chars in input string to create a rna like genetic code
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
    # create individual with unique values. A letter can only a have a one
    # value. It's a constraint that must stay intact no matter what
    individual = []

    while len(GENETIC_CODE) != len(individual):
        rnd_int = random.randint(0, 9)
        if rnd_int not in individual:
            individual.append(rnd_int)
    return individual


def generate_genetic_dictionary(individual):
    # creates a dictionary to be used in calculations. Dictionary hold  a value
    # for each letter in genetic code
    genom_dictionary = {}
    for char, value in zip(GENETIC_CODE, individual):
        genom_dictionary[char] = value

    # print(genom_dictionary)
    return genom_dictionary


def convert_individual_toint(individual, data):

    arguments, result = parse_input()

    argument_ints = []
    for argument in arguments:
        argument_string = ""
        for char in argument:
            argument_string += str(data[char])
        argument_ints.append(int(argument_string))

    result_string = ""
    for char in result:
        result_string += str(data[char])

    result_total = int(result_string)

    return argument_ints, result_total


def change_a_value(individual, digit_to_change, new_value):
    # changes a value in indivual with uniqueness of a gene in mind
    index = individual.index(digit_to_change)
    if new_value in individual:
        conflicted_index = individual.index(new_value)
        not_done = True
        while not_done:
            r_int = random.randint(0, 9)
            if r_int not in individual or r_int == digit_to_change:
                not_done = False

        individual[conflicted_index] = r_int

    individual[index] = new_value


def repair(individual, arguments, result, data):
    change_argument = random.choice([True, False])

    if change_argument:
        last_digits = []
        #last_digits.append(arg % 10 for arg in arguments)
        for arg in arguments:
            last_digits.append(arg % 10)
        digit_to_change = random.choice(last_digits)
        # TODO same value could be more than one. check later
        other_digits = [i for i in last_digits if i != digit_to_change]
        new_value = result % 10 - sum(other_digits) % 10
        if new_value < 0:
            new_value += 10
        change_a_value(individual, digit_to_change, new_value)
    else:
        # change result's last digit
        digit_to_change = result % 10
        new_value = sum(arguments) % 10
        change_a_value(individual, digit_to_change, new_value)

    data = generate_genetic_dictionary(individual)


def calc_fitness(individual, data):

    debug = False
    handle_type = "repair"
    data = generate_genetic_dictionary(individual)

    arguments, result = convert_individual_toint(individual, data)
    arguments_total = sum(arguments)

    penalty = 1
    # first digit of the sum of arguments must be equal to fisrt digit of the
    # result. If not handle the constraint accordingly
    if arguments_total % 10 != result % 10:
        # default constraint handling method is repair
        if handle_type == "repair":
            repair(individual, arguments, result, data)
            # try here for Y error
            arguments, result = convert_individual_toint(individual, data)
            arguments_total = sum(arguments)
        else:
            penalty = 100

    if debug:
        print("args: ", arguments, "\nres: ", result,
              "\nfitness: ", abs(arguments_total - result), "\n\n")

    return abs(arguments_total - result) * penalty


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
                               population_size=40,
                               generations=200,
                               crossover_probability=0.8,
                               mutation_probability=0.1,
                               elitism=True,
                               maximise_fitness=False)
ga.mutate_function = mutate
ga.create_individual = generate_individual
ga.fitness_function = calc_fitness
ga.crossover_function = crossover_at_random_index
count_feasible = 0
iteraions = 30

for i in range(iteraions):
    ga.run()
    best_ind = ga.best_individual()[1]
    best_fitness = ga.best_individual()[0]
    genetic_dictionary = generate_genetic_dictionary(best_ind)
    args, result = convert_individual_toint(best_ind, genetic_dictionary)
    if best_fitness == 0:
        count_feasible += 1
    print("\nBest Fitness: ", best_fitness, "\nBest individual: ", best_ind,
          "\nGenetic Dictionary: ", genetic_dictionary, "\nArgs: ", args,
          "\nRes: ", result)

print("\n\nOut of ", iteraions, "iteraions ", count_feasible,
      " of them were feasible")
# print(calc_fitness(generate_individual()))

"""

This is a python version of the genetic algorithm tutorial from ai-junkie.com
converted by Ryan Massoth
http://www.ryanmassoth.com
https://github.com/rmassoth/ga_tut.git
"""
import random

# constants
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.001
POP_SIZE = 100
CHROMO_LENGTH = 300
GENE_LENGTH = 4
MAX_ALLOWABLE_GENERATIONS = 20

# return random number between 0 and 1
RANDOM_NUM = random.random

class chromo_typ():
    """

    Define a class which will define a chromosome
    """
    def __init__(self, bits="", fitness=0.0):
        self.bits = bits
        self.fitness = fitness

def get_random_bits(length):
    """Return a string of random 1s and 0s of desired length."""
    bit_string = ""
    for _ in range(length):
        if RANDOM_NUM() > 0.5:
            bit_string = "{}{}".format(bit_string, "1")
        else:
            bit_string = "{}{}".format(bit_string, "0")
    return bit_string

def bin_to_dec(bit_string):
    """Convert string of bits to a decimal integer."""
    return int(bit_string, 2)

def parse_bits(bit_string, gene_buffer, gene_length):
    """

    Given a string, this function will step through the genes one at a time
    and insert the decimal values of each gene into the buffer.  Returns the
    number of elements in the buffer.
    Step through the bits one gene at a time until end and store decimal values
    of valid operators and numbers.  Don't forget we are looking for operator
    number - operator - number and so on... We ignore the unused genes 1111 and
    1110

    I changed this one to include gene_length as a parameter for automated test
    purposes.

    Also, it doesn't return the number of elements like the original c++
    program because it's unnecessary in Python.
    """

    # Flag to determine if we are looking for an operator or a number
    b_operator = True

    # Storage for a decimal value of currently tested gene
    this_gene = 0

    for i in range(0, len(bit_string), gene_length):
        # Convert the current gene to decimal
        this_gene = bin_to_dec(bit_string[i:i+gene_length])

        # Find a gene which represents an operator
        if b_operator:
            if this_gene < 10 or this_gene > 13:
                continue
            else:
                b_operator = False
                gene_buffer.append(this_gene)
                continue
        # Find a gene which represents a number
        else:
            if this_gene > 9:
                continue
            else:
                b_operator = True
                gene_buffer.append(this_gene)
                continue

    # Now we have to run through buffer to see if a possible divide by zero
    # is included and delete it. (id a '/' followed by a '0').  We take an
    # easy way out here and just change the '/' to a '+'.  This will not
    # effect the evolution of the solution.
    for i, val in enumerate(gene_buffer):
        if i<len(gene_buffer)-1:
            if val == 13 and gene_buffer[i+1] == 0:
                gene_buffer[i] = 10

def assign_fitness(bit_string, target_value):
    """

    Given a string of bits and a target value this function will calculate
    its representation and return a fitness score accordingly
    """

    # Holds decimal values of gene sequence
    gene_buffer = []

    # Fill buffer from bit_string
    parse_bits(bit_string, gene_buffer, GENE_LENGTH)

    # Now we a have a buffer filled with valid values of: operator - number -
    # operator - number..
    # Now we calculate what this represents
    result = 0.0

    for i in range(0, len(gene_buffer)-1, 2):
        # No switch/case in Python :'(
        if gene_buffer[i] == 10:
            result += gene_buffer[i+1]
        elif gene_buffer[i] == 11:
            result -= gene_buffer[i+1]
        elif gene_buffer[i] == 12:
            result *= gene_buffer[i+1]
        elif gene_buffer[i] == 13:
            result /= gene_buffer[i+1]
    # Now we calculate the fitness.  First check to see if a solution has been
    # Found and assign an arbitrarily high fitness score if this is so.
    if result == target_value:
        return 999.0
    else:
        return 10/abs(target_value - result)

def print_chromo(bit_string):
    """

    Decodes and prints a chromo to screen.  This is a little redundant for
    Python but for the sake of following the original source I will copy it.
    I will do this better in my own code eventually.
    """
    # Buffer to hold the chromosome
    gene_buffer = []

    # Parse the string into genes
    parse_bits(bit_string, gene_buffer, GENE_LENGTH)

    # Loop over every integer in the buffer and convert it to a string
    # representing the uncoded values
    for _, val in enumerate(gene_buffer):
        print_gene_symbol(val)

def print_gene_symbol(val):
    """

    Given and integer, this function outputs its symbol to the screen
    """

    if val < 10:
        print(val, " ", end="")
    else:
        if val == 10:
            print("+", end="")
        elif val == 11:
            print("-", end="")
        elif val == 12:
            print("*", end="")
        elif val == 13:
            print("/", end="")
        print(" ", end="")

def mutate(bit_string):
    """

    Mutates a chromosome's bits dependent on the MUTATION_RATE
    """
    for i, _ in enumerate(bit_string):
        original_string = bit_string
        mutated = False
        if RANDOM_NUM() < MUTATION_RATE:
            mutated = True
            if bit_string[i] == "1":
                bit_string[i] = "0"
            else:
                bit_string[i] = "1"
        return original_string, mutated

def crossover(offspring1, offspring2):
    """

    Dependent on the CROSSOVER_RATE, this function selects a random point along
    the length of the chromosomes and swaps all the bits after that point
    """
    # Dependent on the crossover rate
    if RANDOM_NUM() < CROSSOVER_RATE:
        # Create a random crossover point
        crossover = int(RANDOM_NUM() * len(offspring1))
        t1 = "{}{}".format(
            offspring1[:crossover], offspring2[crossover:])
        t2 = "{}{}".format(
            offspring2[:crossover], offspring1[crossover:])

        return (t1, t2, True,)
    else:
        return (offspring1, offspring2, False)

def roulette(total_fitness, population, pop_size):
    """

    Selects a chromosome from the population via roulette wheel selection.
    """
    # Generate a random number between 0 and total fitness count
    pie_slice = RANDOM_NUM() * total_fitness

    # Go through the chromosomes adding up the fitness so far
    fitness_so_far = 0.0

    for i in range(pop_size):
        fitness_so_far += population[i].fitness

        # If the fitness so far > random number return the chromo at this point
        if fitness_so_far >= pie_slice:
            return population[i].bits

    return ""

def main():
    """

    Main function where all the magic happens.
    """

    # Loop forever.  I will probably change this.
    while True:
        population = []

        # Get a target number from the user. (no error checking)
        target = input("Input a target number: ")

        # First create a random population, all with zero fitness
        for _ in range(POP_SIZE):
            new_chromo = chromo_typ(bits=get_random_bits(CHROMO_LENGTH),
                                    fitness=0.0)
            population.append(new_chromo)

        generations_required_to_find_solution = 0
        # We will set this flag if a solution has been found
        bFound = False
        total_fitness_list = []

        while not bFound:
            # Main GA loop

            # Used for roulette wheel sampling
            total_fitness = 0.0

            # Test and update the fitness of every chromosome in the 
            # population
            for i in range(POP_SIZE):
                population[i].fitness = assign_fitness(
                    population[i].bits, float(target))
                total_fitness += population[i].fitness
            total_fitness_list.append(total_fitness)
            # Check to see if we have found any solutions (fitness will be 999)
            for i in range(POP_SIZE):
                if population[i].fitness == 999.0:
                    print("Solution found in ",
                          generations_required_to_find_solution, 
                          " generations")
                    print_chromo(population[i].bits)
                    bFound = True
                    break

            # Create a new population by selecting two parents at a time and 
            # creating offspring by applying crossover and mutation.  Do this
            # until the desired number of offspring have been created.

            # Define some temporary storage for the new population we are about
            # to create.
            temp = []
            cPop = 0

            # Loop until we have created POP_SIZE new chromosomes
            while cPop < POP_SIZE:
                # We are going to create the new population by grabbing members
                # of the old population two at a time via roulette wheel 
                # selection.
                offspring1 = roulette(total_fitness, population, POP_SIZE)
                offspring2 = roulette(total_fitness, population, POP_SIZE)

                # Add crossover dependent on the crossover rate
                offspring1, offspring2, crossed_over = crossover(offspring1,
                                                                 offspring2)
                # Add these offspring to the new population. (Assigning zero as 
                # their fitness scores)
                temp.append(chromo_typ(offspring1, 0.0))
                temp.append(chromo_typ(offspring2, 0.0))
                cPop += 2

            # Copy temp population into main population array
            population = temp

            generations_required_to_find_solution += 1

            # Exit app if no solution found within the maximum allowable number
            # of generations
            if generations_required_to_find_solution > \
               MAX_ALLOWABLE_GENERATIONS:

                print("No solutions found this run!")
                bFound = True

        with open("fitness.csv", 'w') as output:
            for i, val in enumerate(total_fitness_list):
                output.write('{},{}\n'.format(i, val))

# Run main function if started from the command line
if __name__ == "__main__":
    main()
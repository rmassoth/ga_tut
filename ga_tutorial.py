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
MAX_ALLOWABLE_GENERATIONS = 400

# return random number between 0 and 1
RANDOM_NUM = random.random

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

    for i in range(0, len(gene_buffer), 2):
        # No switch/case in Python :'(
        if gene_buffer[i] == 10:
            result += gene_buffer[i+1]
            break
        elif gene_buffer[i] == 11:
            result -= gene_buffer[i+1]
            break
        elif gene_buffer[i] == 12:
            result *= gene_buffer[i+1]
            break
        elif gene_buffer[i] == 13:
            result /= gene_buffer[i+1]
            break

    # Now we calculate the fitness.  First check to see if a solution has been
    # Found and assign an arbitrarily high fitness score if this is so.
    if result == target_value:
        return 999.0
    else:
        return 1/abs(target_value - result)

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
        return mutated, original_string

"""

This is a python version of the genetic algorithm tutorial from ai-junkie.com
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

def parse_bits(bit_string, gene_buffer):
    """

    Given a string, this function will step through the genes one at a time
    and insert the decimal values of each gene into the buffer.  Returns the
    number of elements in the buffer.
    """

    # Count for buffer position
    c_buff = 0
    """

    step through the bits a gene at a time until end and store decimal values
    of valid operators and numbers.  Don't forget we are looking for operator
    number - operator - number and so on... We ignore the unused genes 1111 and
    1110
    """

    # Flag to determine if we are looking for an operator or a number
    b_operator = True

    # Storage for a decimal value of currently tested gene
    this_gene = 0

    for i in range(0, CHROMO_LENGTH, GENE_LENGTH):
        # Convert the current gene to decimal
        this_gene = bin_to_dec(bits[i:GENE_LENGTH])

        # Find a gene which represents an operator
        if b_operator:
            if this_gene < 10 or this_gene >13:
                continue
            else:
                b_operator = False
                gene_buffer[c_buff += 1] = this_gene
                continue
        # Find a gene which represents a number
        else:
            if this_gene > 9:
                continue
            else:
                b_operator = True
                gene_buffer[c_buff += 1] = this_gene
                continue

        """
        
        Now we have to run through buffer to see if a possible divide by zero
        is included and delete it. (id a '/' followed by a '0').  We take an
        easy way out here and just change the '/' to a '+'.  This will not
        effect the evolution of the solution.
        """
        for i in range(c_buff):
            if gene_buffer[i] == 13 and gene_buffer[i+1] == 0:
                gene_buffer = 10
            return c_buff

parse_bits(bits)
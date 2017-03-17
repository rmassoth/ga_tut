import pytest

import ga_tutorial
bit_string = '1010011111000010'
decoded_string = '+ 7  * 2  '
def test_random_bits():
    length = 30
    bits = ga_tutorial.get_random_bits(length)
    assert len(bits) == length

def test_bin_to_dec():
    single_gene_string = '0110'
    assert ga_tutorial.bin_to_dec(single_gene_string) == 6

def test_parse_bits():
    test_buffer = []
    compare_buffer = [10, 7, 12, 2]
    ga_tutorial.parse_bits(bit_string, test_buffer, 4)
    assert test_buffer == compare_buffer

def test_assign_fitness_perfect():
    target_value = 14
    fitness_value = ga_tutorial.assign_fitness(bit_string, target_value)
    assert fitness_value == 999.0

def test_assign_fitness():
    target_value = 2
    fitness_value = ga_tutorial.assign_fitness(bit_string, target_value)
    assert fitness_value == (1/abs(target_value-7*2))

def test_print_chromo(capsys):
    ga_tutorial.print_chromo(bit_string)
    printed_string, err = capsys.readouterr()
    assert printed_string == decoded_string

def test_print_gene_symbol(capsys):
    ga_tutorial.print_gene_symbol(10)
    printed_val, err = capsys.readouterr()
    assert printed_val == "+ "

def test_mutate():
    # This one is difficult to test given its probabilistic nature.  It must
    # tell that it has mutated and also give the mutated string for testing
    # against the original.  Randomness is difficult to test for.
    original_string, mutated = ga_tutorial.mutate(bit_string)
    if mutated:
        assert original_string != bit_string
    else:
        assert original_string == bit_string

def test_chromo_class():
    bits = "11001010"
    fitness = 0.5
    my_chromo = ga_tutorial.chromo_typ(bits=bits, fitness=fitness)
    assert my_chromo.bits == bits
    assert my_chromo.fitness == fitness

def test_roulette():
    bits = "11001010"
    fitness = 0.5
    my_chromo = ga_tutorial.chromo_typ(bits=bits, fitness=fitness)
    selected_chromo = ga_tutorial.roulette(fitness, [my_chromo], 1)
    assert selected_chromo == my_chromo.bits

def test_roulette_empty():
    selected_chromo = ga_tutorial.roulette(0, [], 0)
    assert selected_chromo == ""

def test_crossover():
    offspring1 = "11001010"
    offspring2 = "00100101"
    offspring1_new, offspring2_new, crossed_over, = ga_tutorial.crossover(
        offspring1, offspring2)
    for _ in range(1000):
        if crossed_over:
            print(offspring1, offspring1_new)
            print(offspring2, offspring2_new)
            assert offspring1_new != offspring1
            assert offspring2_new != offspring2
            assert len(offspring1_new) == len(offspring1)
            assert len(offspring2_new) == len(offspring2)
        else:
            assert offspring1_new == offspring1
            assert offspring2_new == offspring2

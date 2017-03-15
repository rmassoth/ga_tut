import pytest

import ga_tutorial
bit_string = '1101011111000010'
decoded_string = '/ 7  * 2  '
def test_random_bits():
    length = 30
    bits = ga_tutorial.get_random_bits(length)
    assert len(bits) == length

def test_bin_to_dec():
    single_gene_string = '0110'
    assert ga_tutorial.bin_to_dec(single_gene_string) == 6

def test_parse_bits():
    test_buffer = []
    compare_buffer = [13, 7, 12, 2]
    ga_tutorial.parse_bits(bit_string, test_buffer, 4)
    assert test_buffer == compare_buffer

def test_assign_fitness():
    target_value = 20
    fitness_value = ga_tutorial.assign_fitness(bit_string, target_value)
    assert isinstance(fitness_value, float)

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
    mutated, original_string = ga_tutorial.mutate(bit_string)
    if mutated:
        assert original_string != bit_string
    else:
        assert original_string == bit_string

def test_crossover():
    pass

def test_roulette():
    pass

def test_roulette_empty():
    pass
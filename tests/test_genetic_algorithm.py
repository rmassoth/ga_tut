import pytest

import ga_tutorial
bit_string = '1101011111000010'
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
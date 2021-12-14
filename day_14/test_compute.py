from time import time

import pytest

from day_14.compute import Bench, Rule


class TestRule:

    @pytest.mark.parametrize('value, expected', (
        ('CH -> B', Rule('CH', 'B')),
        ('HH -> N', Rule('HH', 'N')),
    ))
    def test_from_str(self, value, expected):
        assert Rule.from_str(value) == expected


class TestBench:

    def test_simulate_reaction(self):
        bench = Bench.from_file('example.txt')

        assert bench.simulate_reaction(1) == ('NNCB', 'NCNBCHB')
        assert bench.simulate_reaction(1) == ('NCNBCHB', 'NBCCNBBBCBHCB')
        assert bench.simulate_reaction(1) == ('NBCCNBBBCBHCB', 'NBBBCNCCNBBNBNBBCHBHHBCHB')
        assert bench.simulate_reaction(1) == (
            'NBBBCNCCNBBNBNBBCHBHHBCHB', 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
        )

    def test_q1_example_score(self):
        bench = Bench.from_file('example.txt')
        bench.simulate_reaction(10)
        assert bench._polymer_map.get('B') == 1749
        assert bench._polymer_map.get('C') == 298
        assert bench._polymer_map.get('H') == 161
        assert bench.score() == 1588

    # def test_q2_example_score_slow(self):
    #     bench = Bench.from_file('example.txt')
    #     bench.simulate_reaction(40)
    #     assert bench._polymer_map.get('B') == 2192039569602
    #     assert bench._polymer_map.get('H') == 3849876073
    #     assert bench.score() == 2188189693529

    def test_q1(self):
        bench = Bench.from_file('input.txt')
        bench.simulate_reaction(10)
        assert bench.score() == 2068

    @pytest.mark.parametrize('value, expected', (
        ('NNCB', ['NN', 'NC', 'CB']),
    ))
    def test_pairs(self, value, expected):
        assert Bench.pairs(list(value)) == expected

from typing import List

import pytest

from day_18.compute import Pair


class TestPair:

    @pytest.mark.parametrize('source_str, expected', (
        ('[1,2]', Pair(1, 2)),
        ('[[1,2],3]', Pair(Pair(1, 2), 3)),
        ('[9,[8,7]]', Pair(9, Pair(8, 7))),
        ('[[1,9],[8,5]]', Pair(Pair(1, 9), Pair(8, 5))),
        (
            '[['
            '[[1,2],[3,4]],'
            '[[5,6],[7,8]]'
            '],9]',
            Pair(
                Pair(
                    Pair(Pair(1, 2), Pair(3, 4)),
                    Pair(Pair(5, 6), Pair(7, 8)),
                ),
                9,
            )
        ),
        (
            '[['
            '[[1,3],[5,3]],'
            '[[1,3],[8,7]]'
            '],['
            '[[4,9],[6,9]],'
            '[[8,2],[7,3]]'
            ']]',
            Pair(
                Pair(
                    Pair(Pair(1, 3), Pair(5, 3)),
                    Pair(Pair(1, 3), Pair(8, 7)),
                ),
                Pair(
                    Pair(Pair(4, 9), Pair(6, 9)),
                    Pair(Pair(8, 2), Pair(7, 3)),
                ),
            ),
        ),
    ))
    def test_from_str(self, source_str: str, expected: Pair):
        obj = Pair.from_str(source_str)
        assert obj == expected
        assert str(obj) == source_str

    @pytest.mark.parametrize('source_str, output', (
        (
            '[[[[[9,8],1],2],3],4]',
            '[[[[  0  ,9],2],3],4]',
        ),
        (
            '[7,[6,[5,[4,[3,2]]]]]',
            '[7,[6,[5,[7,  0  ]]]]',
        ),
        (
            '[[6,[5,[4,[3,2]]]],1]',
            '[[6,[5,[7,  0  ]]],3]',
        ),
        (
            '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
            '[[3,[2,[8,  0  ]]],[9,[5,[4,[3,2]]]]]',
        ),
        (
            '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]',
            '[[3,[2,[8,0]]],[9,[5,[7,  0  ]]]]',
        ),
        (
            '[[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]',
            '[[[[4,0],[5,4]],[[  0,  [7,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]',
        )
    ))
    def test_single_explode(self, source_str: str, output: str):
        obj = Pair.from_str(source_str)
        assert obj.explode() is True
        assert str(obj) == output.replace(' ', '')

    @pytest.mark.parametrize('source_str, output', (
        (
            '[[[[0,7],4],[ 15  ,[0,13]]],[1,1]]',
            '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]',
        ),
        (
            '[[[[0,7],4],[[7,8],[0,  13 ]]],[1,1]]',
            '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]',
        ),
    ))
    def test_single_split(self, source_str: str, output: str):
        obj = Pair.from_str(source_str.replace(' ', ''))
        assert obj.split() is True
        assert str(obj) == output

    @pytest.mark.parametrize('source_str, magnitude', (
        ('[9,1]', 29),
        ('[[9,1],[1,9]]', 129),
        ('[[1,2],[[3,4],5]]', 143),
        ('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', 1384),
        ('[[[[1,1],[2,2]],[3,3]],[4,4]]', 445),
        ('[[[[3,0],[5,3]],[4,4]],[5,5]]', 791),
        ('[[[[5,0],[7,4]],[5,5]],[6,6]]', 1137),
    ))
    def test_magnitude(self, source_str: str, magnitude: int):
        assert Pair.from_str(source_str).magnitude == magnitude

    @pytest.mark.parametrize('a, b, expected', (
        ('[1,2]', '[[3,4],5]', '[[1,2],[[3,4],5]]'),
        ('[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'),
        (
            '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
            '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
            '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]',
        ),
    ))
    def test_add(self, a: str, b: str, expected: str):
        obj_a = Pair.from_str(a)
        obj_b = Pair.from_str(b)
        assert str(obj_a + obj_b) == expected
        assert str(obj_a) == a, 'modified original objects'
        assert str(obj_b) == b, 'modified original objects'

    @pytest.mark.parametrize('source_strings, expected', (
        (
            ['[1,1]', '[2,2]', '[3,3]', '[4,4]'],
            '[[[[1,1],[2,2]],[3,3]],[4,4]]',
        ),
        (
            ['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]'],
            '[[[[3,0],[5,3]],[4,4]],[5,5]]'
        ),
        (
            ['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]', '[6,6]'],
            '[[[[5,0],[7,4]],[5,5]],[6,6]]'
        ),
    ))
    def test_final_sum(self, source_strings: List[str], expected: str):
        assert str(Pair.final_sum([Pair.from_str(l) for l in source_strings])) == expected


def test_q1_example_1():
    rv = Pair.final_sum(Pair.from_file('example_1.txt'))
    assert str(rv) == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
    assert rv.magnitude == 3488


def test_q1_example_2():
    rv = Pair.final_sum(Pair.from_file('example_2.txt'))
    assert str(rv) == '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'
    assert rv.magnitude == 4140


def test_q2_example_2():
    rv = Pair.largest_magnitude(Pair.from_file('example_2.txt'))
    assert rv.magnitude == 3993
    assert str(rv) == '[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]'


def test_q1():
    assert Pair.final_sum(Pair.from_file('input.txt')).magnitude == 3816


def test_q2():
    assert Pair.largest_magnitude(Pair.from_file('input.txt')).magnitude == 4819

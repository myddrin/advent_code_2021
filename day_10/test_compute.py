import pytest

from day_10.compute import Delim, CorruptedLine, Parser


class TestDelim:
    @pytest.mark.parametrize('delim', list(Delim))
    def test_all(self, delim):
        if delim.is_closing:
            assert delim.corrupted_points != 0
            assert delim.autocomplete_points != 0
            assert delim.opening() is not None
            assert delim.closing() is None
            assert delim.opening().closing() == delim
        else:
            assert delim.corrupted_points == 0
            assert delim.opening() is None
            assert delim.closing() is not None
            assert delim.closing().opening() == delim


class TestParser:
    @pytest.mark.parametrize('value', (
        '()',
        '[]',
        '{}',
        '<>',
        '([])',
        '{()()()}',
        '<([{}])>',
        '[<>({}){}[([])<>]]',
        '(((((((((())))))))))',
    ))
    def test_valid_syntax(self, value):
        assert Parser.validate(value) == (value, 0)

    @pytest.mark.parametrize('value, exp_delim, exp_idx', (
        ('(]', Delim.CloseSquare, 1),
        ('{()()()>', Delim.CloseCompare, 7),
        ('(((()))}', Delim.CloseCurly, 7),
        ('<([]){()}[{}])', Delim.CloseRound, 13),
    ))
    def test_corrupted_lines(self, value, exp_delim, exp_idx):
        try:
            Parser.validate(value)
        except CorruptedLine as e:
            assert e.delim == exp_delim
            assert e.index == exp_idx
            assert e.line == value
        else:
            assert False, 'Should have raised'

    @pytest.mark.parametrize('value, exp_auto, exp_score', (
        ('[({(<(())[]>[[{[]{<()<>>', '}}]])})]', 288957),
        ('[(()[<>])]({[<{<<[]>>(', ')}>]})', 5566),
        ('(((({<>}<{<{<>}{[]{[]{}', '}}>}>))))', 1480781),
        ('{<[[]]>}<{[{[{[]{()[[[]', ']]}}]}]}>', 995444),
        ('<{([{{}}[<[[[<>{}]]]>[]]', '])}>', 294),
    ))
    def test_autocomplete(self, value, exp_auto, exp_score):
        line, score = Parser.validate(value)
        assert line == value + exp_auto
        assert score == exp_score


def test_example():
    parser = Parser.from_file('example.txt')
    assert parser.corruption_score == 26397, 'q1'
    assert parser.autocomplete_score == 288957, 'q2'


def test_answers():
    parser = Parser.from_file('input.txt')
    assert parser.corruption_score == 318081, 'q1'
    assert parser.autocomplete_score == 4361305341, 'q2'

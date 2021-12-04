import pytest

from day_04.compute import Game, Board


class TestBoard:
    @classmethod
    def make_board(cls) -> Board:
        rv = Board()
        rv.append((22, 13, 17, 11, 0))
        rv.append((8, 2, 23, 4, 24))
        rv.append((21, 9, 14, 16, 7))
        rv.append((6, 10, 3, 18, 5))
        rv.append((1, 12, 20, 15, 19))
        return rv

    @pytest.mark.parametrize('numbers, exp', (
        ([22, 8, 21, 6, 1], True),
        ([22, 2, 9, 10, 20], False),
    ))
    def test_col_bingo(self, numbers, exp):
        board = self.make_board()
        for n in numbers[:-1]:
            assert board.check(n) is None

        pos = board.check(numbers[-1])
        if exp:
            assert pos is not None
            assert board._col_bingo(pos[0])
            assert not board._row_bingo(pos[1])
        else:
            assert pos is None

    @pytest.mark.parametrize('numbers, exp', (
        ([22, 13, 17, 11, 0], True),
        ([22, 13, 17, 11, 24], False),
    ))
    def test_row_bingo(self, numbers, exp):
        board = self.make_board()
        for n in numbers[:-1]:
            assert board.check(n) is None

        pos = board.check(numbers[-1])
        if exp:
            assert pos is not None
            assert board._row_bingo(pos[1])
            assert not board._row_bingo(pos[0])
        else:
            assert pos is None


class TestGame:

    def test_load(self):
        game = Game.load_game('example.txt')

        assert game.numbers == [7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1]
        assert len(game.boards) == 3

        exp_board_0 = Board()
        exp_board_0.append((22, 13, 17, 11, 0))
        exp_board_0.append((8, 2, 23, 4, 24))
        exp_board_0.append((21, 9, 14, 16, 7))
        exp_board_0.append((6, 10, 3, 18, 5))
        exp_board_0.append((1, 12, 20, 15, 19))

        # TODO(tr) board 1

        exp_board_2 = Board()
        exp_board_2.append((14, 21, 17, 24, 4))
        exp_board_2.append((10, 16, 15, 9, 19))
        exp_board_2.append((18, 8, 23, 26, 20))
        exp_board_2.append((22, 11, 13, 6, 5))
        exp_board_2.append((2, 0, 12, 3, 7))

        assert game.boards[0] == exp_board_0
        assert game.boards[2] == exp_board_2

    def test_play_example(self):
        game = Game.load_game('example.txt')

        # score = game.play(end=5)
        # assert score is None
        #
        # score = game.play(st=5, end=6)
        # assert score is None

        score = game.play()
        assert score == (2, 4512)


def test_q1():
    game = Game.load_game('input.txt')
    assert game.play() == (48, 31424)

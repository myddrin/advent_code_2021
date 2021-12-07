import pytest

from day_07.compute import Crab, Swarm


class TestCrab:

    @pytest.mark.parametrize('crab, position, exp', (
        (Crab(16, 1), 2, 14),
        (Crab(1, 2), 2, 2),
        (Crab(2, 1), 2, 0),
    ))
    def test_cost_to_linear(self, crab, position, exp):
        assert crab.cost_to(position) == exp

    @pytest.mark.parametrize('crab, position, exp', (
            (Crab(16, 1), 5, 66),
            (Crab(1, 2), 2, 2),
            (Crab(2, 1), 2, 0),
    ))
    def test_cost_to_exponential(self, crab, position, exp):
        assert crab.cost_to(position, exponential=True) == exp


class TestSwarm:

    def test_from_str(self):
        swarm = Swarm.from_str('16,1,2,0,4,2,7,1,2,14')

        assert len(swarm.crabs) == 7
        assert swarm.count() == 10

    def test_linear_cost(self):
        swarm = Swarm.from_str('16,1,2,0,4,2,7,1,2,14')
        cost = swarm.compute_position_cost()
        assert len(cost) == 17  # 0 to 17 incl.

        assert cost[2] == 37
        assert cost[1] == 41
        assert cost[3] == 39
        assert cost[10] == 71

    def test_exponential_cost(self):
        swarm = Swarm.from_str('16,1,2,0,4,2,7,1,2,14')
        cost = swarm.compute_position_cost(exponential=True)
        assert len(cost) == 17  # 0 to 17 incl.

        assert cost[2] == 206
        assert cost[5] == 168

    def test_from_file(self):
        swarm = Swarm.from_file('example.txt')
        assert len(swarm.crabs) == 7
        assert swarm.count() == 10


def test_q1_example():
    best_position, cost = Swarm.from_file('example.txt').best_position()
    assert best_position == 2
    assert cost == 37


def test_q2_example():
    best_position, cost = Swarm.from_file('example.txt').best_position(exponential=True)
    assert best_position == 5
    assert cost == 168


def test_q1():
    best_position, cost = Swarm.from_file('input.txt').best_position()
    assert best_position == 339
    assert cost == 328318


def test_q2():
    best_position, cost = Swarm.from_file('input.txt').best_position(exponential=True)
    assert best_position == 467
    assert cost == 89791146

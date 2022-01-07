from typing import List

import pytest

from day_17.compute import World, Position, Velocity, Trajectory


class TestVelocity:

    @pytest.mark.parametrize('init, expected', (
        (Velocity(7, 2), Velocity(6, 1)),
        (Velocity(6, 1), Velocity(5, 0)),
        (Velocity(5, 0), Velocity(4, -1)),
        (Velocity(4, -1), Velocity(3, -2)),
        (Velocity(1, -4), Velocity(0, -5)),
        (Velocity(0, -5), Velocity(0, -6)),
    ))
    def test_update(self, init: Velocity, expected: Velocity):
        assert init.update() == expected


class TestTrajectory:

    @pytest.mark.parametrize('velocity, n, expected', (
        (Velocity(7, 2), 7, [
            Position(0, 0),
            Position(7, 2),
            Position(13, 3),
            Position(18, 3),
            Position(22, 2),
            Position(25, 0),
            Position(27, -3),
            Position(28, -7),
        ]),
        (Velocity(6, 3), 9, [
            Position(0, 0),
            Position(6, 3),
            Position(11, 5),
            Position(15, 6),
            Position(18, 6),
            Position(20, 5),
            Position(21, 3),
            Position(21, 0),
            Position(21, -4),
            Position(21, -9),
        ]),
    ))
    def test_update(self, velocity: Velocity, n: int, expected: List[Position]):
        obj = Trajectory(velocity)
        for _ in range(n):
            obj.update()
        assert obj._coordinates == expected


class TestWorld:

    @pytest.mark.parametrize('source_str, expected', (
        ('target area: x=20..30, y=-10..-5', World(
            Position(20, -10),
            Position(30, -5),
        )),
        ('target area: x=248..285, y=-85..-56', World(
            Position(248, -85),
            Position(285, -56),
        )),
    ))
    def test_from_str(self, source_str: str, expected: World):
        assert World.from_str(source_str) == expected

    @pytest.mark.parametrize('position, expected', (
        (Position(28, -7), True),
        (Position(21, -9), True),
        (Position(30, -6), True),
        (Position(24, -3), False),  # just above
        (Position(33, -9), False),  # on the right
        (Position(17, -7), False),  # on the left
        (Position(25, -11), False),  # bellow
    ))
    def test_example_in_area(self, position: Position, expected: bool):
        world = World.from_str('target area: x=20..30, y=-10..-5')
        assert world.in_area(position) is expected

    @pytest.mark.parametrize('velocity, expected', (
        (Velocity(7, 2), True),
        (Velocity(6, 3), True),
        (Velocity(9, 0), True),
        (Velocity(17, -4), False),
        (Velocity(30, -5), True),  # bug found with Q2
        (Velocity(30, -6), True),  # bug found with Q2
        (Velocity(30, -7), True),  # bug found with Q2
        (Velocity(30, -8), True),  # bug found with Q2
        (Velocity(30, -9), True),  # bug found with Q2
        (Velocity(30, -10), True),  # bug found with Q2
    ))
    def test_example_compute(self, velocity: Velocity, expected: bool):
        world = World.from_str('target area: x=20..30, y=-10..-5')
        trajectory, hit = world.compute(velocity)
        assert hit is expected


def test_q1_example():
    assert World.from_file('example.txt').simulate().highest == 45


def test_q2_example():
    expected = {
        (23, -10), (25, -9), (27, -5), (29, -6), (22, -6), (21, -7), (9, 0), (27, -7), (24, -5),
        (25, -7), (26, -6), (25, -5), (6, 8), (11, -2), (20, -5), (29, -10), (6, 3), (28, -7),
        (8, 0), (30, -6), (29, -8), (20, -10), (6, 7), (6, 4), (6, 1), (14, -4), (21, -6),
        (26, -10), (7, -1), (7, 7), (8, -1), (21, -9), (6, 2), (20, -7), (30, -10), (14, -3),
        (20, -8), (13, -2), (7, 3), (28, -8), (29, -9), (15, -3), (22, -5), (26, -8), (25, -8),
        (25, -6), (15, -4), (9, -2), (15, -2), (12, -2), (28, -9), (12, -3), (24, -6), (23, -7),
        (25, -10), (7, 8), (11, -3), (26, -7), (7, 1), (23, -9), (6, 0), (22, -10), (27, -6),
        (8, 1), (22, -8), (13, -4), (7, 6), (28, -6), (11, -4), (12, -4), (26, -9), (7, 4),
        (24, -10), (23, -8), (30, -8), (7, 0), (9, -1), (10, -1), (26, -5), (22, -9), (6, 5),
        (7, 5), (23, -6), (28, -10), (10, -2), (11, -1), (20, -9), (14, -2), (29, -7), (13, -3),
        (23, -5), (24, -8), (27, -9), (30, -7), (28, -5), (21, -10), (7, 9), (6, 6), (21, -5),
        (27, -10), (7, 2), (30, -9), (21, -8), (22, -7), (24, -9), (20, -6), (6, 9), (29, -5),
        (8, -2), (27, -8), (30, -5), (24, -7),
    }
    world = World.from_file('example.txt')
    world.simulate()
    found = {
        (t.initial_velocity.dx, t.initial_velocity.dy)
        for t in world.hit_trajectories
    }
    assert found == expected


def test_questions():
    world = World.from_file('input.txt')
    assert world.simulate().highest == 3570, 'q1 is wrong'
    assert len(world.hit_trajectories) == 1919, 'q2 is wrong'

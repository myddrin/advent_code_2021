import pytest

from day_12.compute import Map, Cave, Path


@pytest.fixture
def simplest_example() -> Map:
    """
        start
        /   \
    c--A-----b--d
        \   /
         end
    """
    data = Map({})
    for line in (
        'start-A',
        'start-b',
        'A-c',
        'A-b',
        'b-d',
        'A-end',
        'b-end',
    ):
        data.add_line(line)
    return data


class TestMap:
    def test_add_line(self, simplest_example):
        expected_links = {
            'start': ['A', 'b'],
            'end': ['A', 'b'],
            'c': ['A'],
            'd': ['b'],
            'A': ['b', 'c', 'end', 'start'],
            'b': ['A', 'd', 'end', 'start'],
        }

        assert len(simplest_example.store) == len(expected_links)
        for name, links in expected_links.items():
            assert sorted(simplest_example.store[name].links.keys()) == links


class TestPath:
    @classmethod
    def from_str(cls, map_data: Map, special_visits: int, *args: str) -> Path:
        p = Path.factory(map_data.store['start'], special_visits)[1]
        for n in args:
            p.add(map_data.store[n])
        return p

    def test_factory(self):
        st = Cave('start')
        path = Path.factory(st)[1]

        assert not path.can_visit(st)

    def test_special_visit(self, simplest_example):
        init_path = self.from_str(simplest_example, 1, 'b', 'A', 'c', 'A')
        assert init_path.special_visits == []

        # path to number of used special visits
        expected = {
            'start,b,A,c,A,end': 0,
            'start,b,A,c,A,c': 1,
            'start,b,A,c,A,b': 1,
        }
        next_paths = init_path.next_paths()
        assert len(next_paths) == len(expected), f'Found {next_paths}'
        for p in next_paths:
            assert str(p) in expected
            assert expected[str(p)] == len(p.special_visits)

    def test_q1_simplest_example(self, simplest_example):
        expected = {
            'start,A,b,A,c,A,end',
            'start,A,b,A,end',
            'start,A,b,end',
            'start,A,c,A,b,A,end',
            'start,A,c,A,b,end',
            'start,A,c,A,end',
            'start,A,end',
            'start,b,A,c,A,end',
            'start,b,A,end',
            'start,b,end',
        }
        paths = simplest_example.find_path('start', 'end')
        assert set(map(str, paths)) == expected

    def test_q1_example_1(self):
        expected = {
            'start,HN,dc,HN,end',
            'start,HN,dc,HN,kj,HN,end',
            'start,HN,dc,end',
            'start,HN,dc,kj,HN,end',
            'start,HN,end',
            'start,HN,kj,HN,dc,HN,end',
            'start,HN,kj,HN,dc,end',
            'start,HN,kj,HN,end',
            'start,HN,kj,dc,HN,end',
            'start,HN,kj,dc,end',
            'start,dc,HN,end',
            'start,dc,HN,kj,HN,end',
            'start,dc,end',
            'start,dc,kj,HN,end',
            'start,kj,HN,dc,HN,end',
            'start,kj,HN,dc,end',
            'start,kj,HN,end',
            'start,kj,dc,HN,end',
            'start,kj,dc,end',
        }
        paths = Map.from_file('example_1.txt').find_path('start', 'end')
        assert set(map(str, paths)) == expected

    def test_q1_example_2(self):
        assert len(Map.from_file('example_2.txt').find_path('start', 'end')) == 226

    def test_q2_simplest_example(self, simplest_example):
        expected = {
            'start,A,b,A,b,A,c,A,end',
            'start,A,b,A,b,A,end',
            'start,A,b,A,b,end',
            'start,A,b,A,c,A,b,A,end',
            'start,A,b,A,c,A,b,end',
            'start,A,b,A,c,A,c,A,end',
            'start,A,b,A,c,A,end',
            'start,A,b,A,end',
            'start,A,b,d,b,A,c,A,end',
            'start,A,b,d,b,A,end',
            'start,A,b,d,b,end',
            'start,A,b,end',
            'start,A,c,A,b,A,b,A,end',
            'start,A,c,A,b,A,b,end',
            'start,A,c,A,b,A,c,A,end',
            'start,A,c,A,b,A,end',
            'start,A,c,A,b,d,b,A,end',
            'start,A,c,A,b,d,b,end',
            'start,A,c,A,b,end',
            'start,A,c,A,c,A,b,A,end',
            'start,A,c,A,c,A,b,end',
            'start,A,c,A,c,A,end',
            'start,A,c,A,end',
            'start,A,end',
            'start,b,A,b,A,c,A,end',
            'start,b,A,b,A,end',
            'start,b,A,b,end',
            'start,b,A,c,A,b,A,end',
            'start,b,A,c,A,b,end',
            'start,b,A,c,A,c,A,end',
            'start,b,A,c,A,end',
            'start,b,A,end',
            'start,b,d,b,A,c,A,end',
            'start,b,d,b,A,end',
            'start,b,d,b,end',
            'start,b,end',
        }
        paths = simplest_example.find_path('start', 'end', 1)
        assert set(map(str, paths)) == expected

    def test_q2_example_1(self):
        assert len(Map.from_file('example_1.txt').find_path('start', 'end', 1)) == 103

    def test_q2_example_2(self):
        assert len(Map.from_file('example_2.txt').find_path('start', 'end', 1)) == 3509


def test_q1():
    assert len(Map.from_file('input.txt').find_path('start', 'end')) == 4970


def test_slow_q2():
    assert len(Map.from_file('input.txt').find_path('start', 'end', 1)) == 137948

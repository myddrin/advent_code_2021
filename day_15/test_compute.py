from day_15.compute import Map, Link, Node


class TestMap:

    def test_small_example_from_file(self):
        rv = Map.from_file('small_example.txt')

        expected_nodes = [
            Node(0, [
                Link(0 * rv.width + 1, 1),
                Link(1 * rv.width + 0, 1),
            ]),
            Node(1, [
                Link(0 * rv.width + 0, 1),
                Link(0 * rv.width + 2, 6),
                Link(1 * rv.width + 1, 3),
            ]),
            Node(2, [
                Link(0 * rv.width + 1, 1),
                Link(1 * rv.width + 2, 8),
            ]),
            Node(3, [
                Link(1 * rv.width + 1, 3),
                Link(0 * rv.width + 0, 1),
                Link(2 * rv.width + 0, 2),
            ]),
            Node(4, [
                Link(1 * rv.width + 0, 1),
                Link(1 * rv.width + 2, 8),
                Link(0 * rv.width + 1, 1),
                Link(2 * rv.width + 1, 1),
            ]),
            Node(5, [
                Link(1 * rv.width + 1, 3),
                Link(0 * rv.width + 2, 6),
                Link(2 * rv.width + 2, 3),
            ]),
            Node(6, [
                Link(2 * rv.width + 1, 1),
                Link(1 * rv.width + 0, 1),
            ]),
            Node(7, [
                Link(2 * rv.width + 0, 2),
                Link(2 * rv.width + 2, 3),
                Link(1 * rv.width + 1, 3),
            ]),
            Node(8, [
                Link(2 * rv.width + 1, 1),
                Link(1 * rv.width + 2, 8),
            ]),
        ]

        assert rv.width == 3
        assert rv.height == 3
        assert rv.nodes == expected_nodes

    def test_small_example_path(self):
        rv = Map.from_file('small_example.txt')
        assert rv.compute_distance(0) == 7
        assert rv.path_to(8) == [
            0,
            3,
            6, 7, 8,
        ]

    def test_small_example_weight(self):
        rv = Map.from_file('small_example.txt')
        assert rv.to_weight() == [
            [1, 1, 6],
            [1, 3, 8],
            [2, 1, 3],
        ]

    def test_small_example_multiply(self):
        rv = Map.from_file('small_example.txt', 5)

        assert rv.width == 3 * 5
        assert rv.height == 3 * 5

        assert rv.nodes[0] == Node(0, [
            Link(0 * rv.width + 1, 1),
            Link(1 * rv.width + 0, 1),
        ])
        # (2, 2) was 8 before multiplying the map, and it has more links too!
        assert rv.nodes[32] == Node(32, [
            Link(2 * rv.width + 1, 1),
            Link(2 * rv.width + 3, 3),
            Link(1 * rv.width + 2, 8),
            Link(3 * rv.width + 2, 7),
        ])

    def test_q1_example(self):
        rv = Map.from_file('example.txt')
        # the example on the website shows
        # 47, 57, 58
        # but they are equivalent in cost (1 or 1)
        assert len(rv.nodes) == 10*10
        assert rv.compute_distance() == 40
        assert rv.path_to(99) == [
            0,
            10,
            20, 21, 22, 23, 24, 25, 26,
                                    36, 37,
                                        47, 48,
                                            58,
                                            68,
                                            78,
                                            88, 89,
                                                99,
        ]
        assert rv.get_distance(99) == 40

    def test_example_multiply(self):
        rv = Map.from_file('example.txt', 5)
        assert rv.to_weight() == Map.weights_from_file('big_example.txt')

    def test_q2_example(self):
        rv = Map.from_file('example.txt', 5)

        assert len(rv.nodes) == 50*50
        assert rv.compute_distance() == 315
        # TODO(tr) Check the path (I'm too lazy... it's a long path)


def test_q1():
    assert Map.from_file('input.txt').compute_distance() == 720


def test_q2():
    assert Map.from_file('input.txt', 5).compute_distance() == 3025

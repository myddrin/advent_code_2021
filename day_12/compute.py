import dataclasses
from argparse import ArgumentParser
from copy import copy
from typing import List, Dict, Iterator, Tuple


@dataclasses.dataclass
class Cave:
    name: str
    links: Dict[str, "Cave"] = dataclasses.field(default_factory=dict, compare=False)

    def is_big(self) -> bool:
        return self.name.upper() == self.name

    def link_with(self, other: "Cave"):
        if other.name not in self.links:
            self.links[other.name] = other
            other.link_with(self)

    def neighbours(self) -> Iterator["Cave"]:
        for c in self.links.values():
            yield c

    def __str__(self):
        return self.name


@dataclasses.dataclass
class PathLeaf:
    cave: Cave
    visited: int = 0

    def __copy__(self):
        # do not copy the ref to cave
        return PathLeaf(self.cave, copy(self.visited))

    def __repr__(self):
        return f'{self.cave.name}({self.visited})'


@dataclasses.dataclass
class Path:
    path: List[PathLeaf] = dataclasses.field(default_factory=list)
    leaves: Dict[str, PathLeaf] = dataclasses.field(default_factory=dict)
    max_special_visits: int = dataclasses.field(default=0)
    special_visits: List[str] = dataclasses.field(default_factory=list)

    @classmethod
    def factory(cls, start: Cave, special_visits: int = 0) -> Tuple[str, "Path"]:
        p = cls(max_special_visits=special_visits)
        p.add(start)
        return str(p), p

    @classmethod
    def to_file(cls, filename: str, data: List["Path"]):
        with open(filename, 'w') as f:
            for p in data:
                f.write(str(p) + '\n')

    def can_visit(self, cave: Cave, exclude: List[str] = ()) -> bool:
        if cave.name not in self.leaves:
            return True
        # Visited before
        if not cave.is_big():
            if cave.name not in ('start', 'end'):
                return len(self.special_visits) != self.max_special_visits
            return False
        # Otherwise, we need to check if we visited all its neighbours
        if not exclude:
            exclude = []
        for n in cave.neighbours():
            if n.name not in exclude and self.can_visit(n, exclude + [cave.name]):
                return True  # one neighbours can be visited, let's go
        return False

    def add(self, cave: Cave):
        if cave.name not in self.leaves:
            self.leaves[cave.name] = PathLeaf(cave)
        self.path.append(self.leaves[cave.name])
        self.leaves[cave.name].visited += 1
        if not cave.is_big() and self.leaves[cave.name].visited > 1:
            self.special_visits.append(cave.name)

    def end(self) -> Cave:
        return self.path[-1].cave

    def __str__(self):
        return ','.join((p.cave.name for p in self.path))

    def __copy__(self):
        return Path(
            [copy(pl) for pl in self.path],
            {k: copy(v) for k, v in self.leaves.items()},
            max_special_visits=self.max_special_visits,
            special_visits=copy(self.special_visits),
        )

    def next_paths(self) -> List["Path"]:
        rv = []
        for c in self.end().neighbours():
            if self.can_visit(c):
                next_path = copy(self)
                next_path.add(c)
                rv.append(next_path)

        return rv

    @classmethod
    def find_paths(cls, start: Cave, end: Cave, special_visits: int = 0) -> List["Path"]:
        rv: Dict[str, Path] = dict((Path.factory(start, special_visits),))

        has_work = True
        while has_work:
            new_rv = {}
            has_work = False
            for p in rv.values():
                if p.end() != end:
                    i = 0
                    for i, next_path in enumerate(p.next_paths(), start=1):
                        new_rv[str(next_path)] = next_path
                    if i > 0:
                        has_work = True
                    # added = 0 Not path, we hit a place that is not "end" and has no passage
                else:
                    new_rv[str(p)] = p
            # has_work = len(rv) != len(new_rv)
            rv = new_rv

        return [p for p in rv.values() if p.end() == end]


@dataclasses.dataclass
class Map:
    store: Dict[str, Cave]

    def find_path(self, start: str = 'start', end: str = 'end', special_visits: int = 0) -> List[Path]:
        return Path.find_paths(
            self.store[start],
            self.store[end],
            special_visits,
        )

    def add_line(self, value: str):
        a, b = value.split('-')
        cave_a = self.store.get(a)
        cave_b = self.store.get(b)
        if cave_a is None:
            cave_a = Cave(a)
            self.store[a] = cave_a
        if cave_b is None:
            cave_b = Cave(b)
            self.store[b] = cave_b
        cave_a.link_with(cave_b)

    @classmethod
    def from_file(cls, filename: str) -> "Map":
        store = cls({})

        with open(filename, 'r') as f:
            for line in f:
                store.add_line(line.replace('\n', ''))

        return store


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    parser.add_argument('--output', type=str, default=None, help='Output file with all paths')
    parser.add_argument('--start', type=str, default='start', help='Where to start from')
    parser.add_argument('--end', type=str, default='end', help='Where to end to')
    parser.add_argument('--special-visits', type=int, default=0,
                        help='Number of double visits to small caves. For Q1 should be 0, for Q2 should be 1.')
    args = parser.parse_args()

    map_data = Map.from_file(args.input)
    print(f'Loaded {len(map_data.store)} entries from {args.input}')

    print(f'Computing paths from {args.start} to {args.end} with {args.special_visits} double visits')
    paths = map_data.find_path(args.start, args.end, args.special_visits)
    print(f'Found {len(paths)} paths from {args.start} to {args.end}')

    if args.output:
        print(f'Writing paths into {args.output}')
        Path.to_file(args.output, paths)

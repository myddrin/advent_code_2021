import dataclasses
from argparse import ArgumentParser
from operator import itemgetter
from time import time
from typing import List


@dataclasses.dataclass
class Node:
    position: int
    links: List["Link"] = dataclasses.field(default_factory=list)
    # used by shortest path in Map:
    visited: bool = False
    # Tentative distance between start and this node.
    # Initialised to 0 for initial node, and None (infinity) for others
    distance: int = None
    # The Node that was used to set the smallest distance is the previous node in the path
    previous: int = None

    @classmethod
    def from_weights(cls, x: int, y: int, weights: List[List[int]]) -> "Node":
        width = len(weights[0])
        height = len(weights)

        obj = cls(position=x + y * width)

        if x - 1 >= 0:
            new_p = (x - 1) + y * width
            obj.links.append(Link(new_p, weights[y][x - 1]))
        if x + 1 < width:
            new_p = (x + 1) + y * width
            obj.links.append(Link(new_p, weights[y][x + 1]))
        if y - 1 >= 0:
            new_p = x + (y - 1) * width
            obj.links.append(Link(new_p, weights[y - 1][x]))
        if y + 1 < height:
            new_p = x + (y + 1) * width
            obj.links.append(Link(new_p, weights[y + 1][x]))

        return obj


@dataclasses.dataclass
class Link:
    # end node
    end: int
    # density of "chiton"
    weight: int


@dataclasses.dataclass
class Map:
    width: int
    height: int
    nodes: List[Node] = dataclasses.field(default_factory=list)
    shortest_from: int = None

    @classmethod
    def weights_from_file(cls, filename: str) -> List[List[int]]:
        weights = []
        with open(filename, 'r') as f:
            for line in f:
                weights.append([
                    int(v)
                    for v in line.replace('\n', '')
                ])
        return weights

    @classmethod
    def from_file(cls, filename: str, multiplier: int = 1) -> "Map":
        weights = []
        with open(filename, 'r') as f:
            for line in f:
                weights.append([
                    int(v)
                    for v in line.replace('\n', '')
                ])

        if multiplier > 1:
            # we need to multiply the map `multiplier` times on the right and bottom
            #
            hor_stride = len(weights[0])
            ver_stride = len(weights)
            print(f'Expanding initial {hor_stride}x{ver_stride} grid {multiplier} times')

            # do the horizontal multiplication
            for y, row in enumerate(weights):
                for x in range(hor_stride, hor_stride * multiplier):
                    value = weights[y][x - hor_stride] + 1
                    if value > 9:
                        value = 1
                    row.append(value)

            # do the vertical multiplication
            for y in range(ver_stride, ver_stride * multiplier):
                row = []
                for x in range(hor_stride * multiplier):
                    value = weights[y - ver_stride][x] + 1
                    if value > 9:
                        value = 1
                    row.append(value)

                weights.append(row)

        width = len(weights[0])
        height = len(weights)
        obj = cls(
            width=width,
            height=height,
            nodes=[
                Node.from_weights(x, y, weights)
                for y in range(height)
                for x in range(width)
            ]
        )
        print(f'Loaded {obj.width}x{obj.height} grid from {filename}')
        return obj

    def to_weight(self) -> List[List[int]]:
        weights = []

        for y in range(1, self.height):
            d_y = y - 1
            row = []
            for x in range(self.width):
                # look for the link to the cell above
                target_position = d_y * self.width + x
                for link in self.nodes[y * self.width + x].links:
                    if link.end == target_position:
                        row.append(link.weight)
                        break
            weights.append(row)

        # still has to do the last row using the previous to last
        row = []
        for x in range(self.width):
            target_position = (self.height - 1) * self.width + x
            for link in self.nodes[(self.height - 2) * self.width + x].links:
                if link.end == target_position:
                    row.append(link.weight)
                    break
        weights.append(row)

        return weights

    def path_to(self, end: int) -> List[int]:
        """Assumes the shortest_path was computed"""
        assert self.shortest_from is not None, 'call `compute_distance` first'
        assert end < len(self.nodes)

        path = []
        current_p = end
        while current_p is not None:
            path.insert(0, current_p)
            current_p = self.nodes[current_p].previous

        return path

    def get_distance(self, end: int) -> int:
        """Assumes the shortest_path was computed"""
        assert self.shortest_from is not None, 'call `compute_distance` first'
        assert end < len(self.nodes)

        return self.nodes[end].distance

    def compute_distance(self, start: int = None, end: int = None) -> int:
        """Implementation of Dijkstra's algorithm"""
        if start is None:
            start = 0  # start top left
        if end is None:
            end = len(self.nodes) - 1  # end bottom right

        assert start < len(self.nodes)
        start_time = time()

        self.shortest_from = start
        # initialise the nodes
        for i, node in enumerate(self.nodes):
            node.visited = False
            node.previous = None
            if i == start:
                node.distance = 0
            else:
                node.distance = None  # infinity

        unvisited_no_distance = {
            n.position: n
            for n in self.nodes
            if n.position != start
        }
        unvisited_with_distance = {
            start: self.nodes[start]
        }
        current = self.nodes[start]

        # we can stop early when current.position == end because we do not need the distance to any node!
        visited = 0
        while current.position != end:
            if visited % 100 == 0:
                print(
                    f'Visited {visited}/{len(self.nodes)} '
                    f'({visited / float(len(self.nodes)):.0f}% in {time() - start_time:.0f} sec) '
                    f'current is ({current.position % self.width}, {current.position // self.width})     ',
                    end='\r'
                )
            for link in current.links:
                destination = self.nodes[link.end]
                if destination.visited:
                    continue  # skip visited
                distance = current.distance + link.weight
                if destination.distance is None or distance < destination.distance:
                    if destination.distance is None:
                        unvisited_no_distance.pop(destination.position)
                        unvisited_with_distance[destination.position] = destination
                    destination.distance = distance
                    destination.previous = current.position

            current.visited = True
            visited += 1
            unvisited_with_distance.pop(current.position)

            # Choose the next current: smallest distance in unvisited
            if unvisited_with_distance:
                current, _ = sorted(
                    (
                        (n, n.distance)
                        for n in unvisited_with_distance.values()
                    ),
                    key=itemgetter(1),
                )[0]

        print(
            f'Computed distances from {start} in {time() - start_time:.2f} sec'
            f' ({len(unvisited_no_distance)} left unvisited)'
        )
        return self.nodes[end].distance

    def to_file(self, filename: str, end: int):
        """Write the shortest path to file."""
        path = self.path_to(end)

        with open(filename, 'w') as f:
            f.write(f'cost: {self.nodes[end].distance}\n')
            f.write('path: ' + ', '.join(map(str, path)) + '\n')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt', help='Input file')
    parser.add_argument('--start', type=int, default=None,
                        help='Start location, default is top-left.')
    parser.add_argument('--end', type=int, default=None,
                        help='End location, default is bottom-right (len of loaded nodes).')
    parser.add_argument('--multiply', type=int, default=1,
                        help='Multiply the loaded map, use 1 for Q1, or 5 for Q2. Default is %(default)s')
    parser.add_argument('--output', type=str, default=None,
                        help='If provided write the path information to a file.')
    args = parser.parse_args()

    chiron_map = Map.from_file(args.input, args.multiply)

    end_location = args.end
    if end_location is None:
        end_location = len(chiron_map.nodes) - 1

    chiron_map.compute_distance(args.start, end_location)

    cost = chiron_map.get_distance(end_location)
    print(f'Q1: shortest distance between {args.start} and {end_location} is {cost}')

    if args.output:
        chiron_map.to_file(args.output, end_location)

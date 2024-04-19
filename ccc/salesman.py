from typing import Set, Callable
from loguru import logger as log

from .gridutils import move_to, points_to_direction, path_to_directions, point_distance


def exhaustive_salesman(
    cities: Set[complex],
    start: complex,
    successor_fn: Callable[[complex, complex], Set[complex]],
):
    # find any (not necessarily the shortest) path that visits all cities
    # use dfs, but with a stack instead of recursion

    stack = [(start, [start])]
    nsteps = 0
    while stack:
        xy, visited = stack.pop()
        if len(visited) == len(cities):
            log.debug(f"found path in {nsteps} steps")
            return visited

        for next_xy in successor_fn(xy, visited[-1]):
            if next_xy in visited:
                continue
            stack.append((next_xy, visited + [next_xy]))
            # log.debug(path_to_directions(visited))
            nsteps += 1
            if nsteps > 300_000:
                return None

    log.error("no solution found")
    return None


def _bounded_grid_successor(
    width: int, height: int, blocked: Set[complex], gravity_xy: complex
) -> Callable[[complex], Set[complex]]:
    def successor_fn(
        xy: complex, pre_xy: complex, recursive: bool = True
    ) -> Set[complex]:
        successors = list()

        # what was the last direction we moved in?
        pre_dir = points_to_direction(pre_xy, xy)

        for dir in "DASW":
            next_xy = move_to(xy, dir)
            if next_xy in blocked:
                continue

            if 0 <= next_xy.real < width and 0 <= next_xy.imag < height:

                # count how many successors this successor has
                priority = 0
                if recursive:
                    succsucc = successor_fn(next_xy, xy, recursive=False)
                    succsucc.remove(xy)
                    priority = len(succsucc)
                    if priority == 0:
                        priority = -1

                # compute distance to point of gravity
                priority = point_distance(next_xy, gravity_xy)

                # give the previous direction a slightly higher priority
                priority += 1 if dir == pre_dir else 0

                successors.append((next_xy, priority))

        # sort by priority
        successors = sorted(successors, key=lambda x: x[1], reverse=False)
        successors = [x[0] for x in successors]

        return successors

    return successor_fn

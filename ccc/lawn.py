from typing import List, Literal, Optional, Tuple, Set
from loguru import logger as log

from .salesman import exhaustive_salesman, _bounded_grid_successor
from .gridutils import Direction, move_to, path_to_directions


class Lawn:
    def __init__(self, width, height, grid):
        self.width: int = width
        self.height: int = height
        self.grid: List[List[str]] = grid

        self.tree: Optional[Tuple[complex]] = None
        self.init_lawn()

    def init_lawn(self):
        # find the tree position in the grid
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == "X":
                    self.tree = complex(x, y)
                    return

        raise ValueError(f"tree not found in grid: {self.grid}")

    def get_valid_positions(self) -> Set[Tuple[complex]]:
        positions = set()
        for h in range(self.height):
            for w in range(self.width):
                positions.add(complex(w, h))

        positions.remove(self.tree)
        return positions

    def find_path(self):
        cities = self.get_valid_positions()
        tl, br = Lawn._get_corners_of_cell_set(cities)
        succ = _bounded_grid_successor(self.width, self.height, {self.tree}, tl)
        path = exhaustive_salesman(cities=cities, start=0, successor_fn=succ)
        if path is None:
            path = exhaustive_salesman(cities=cities, start=self.tree+1j, successor_fn=succ)
        if path is None:
            path = exhaustive_salesman(cities=cities, start=self.tree-1j, successor_fn=succ)
        if path is None:
            path = exhaustive_salesman(cities=cities, start=self.tree+1, successor_fn=succ)
        if path is None:
            path = exhaustive_salesman(cities=cities, start=self.tree-1, successor_fn=succ)
        if path is None:
            path = exhaustive_salesman(cities=cities, start=br, successor_fn=succ)
        log.success(f"found path: {path}")
        directions = path_to_directions(path)
        log.info(f"transformed path to directions: {directions}")
        return directions

    def is_path_valid(self, path: List[Direction]) -> bool:
        # must fit the lawn size
        w, h = Lawn._get_enclosed_rectangle_size_of_path(path)
        if self.width != w or self.height != h:
            log.debug(f"lawn size mismatch: {self.width}x{self.height} != {w}x{h}")
            return False

        xy = 0
        visited = {xy}

        for dir in path:
            xy = move_to(xy, dir)

            # must not visit any cell twice
            if xy in visited:
                log.debug(f"visited cell twice: {xy}")
                return False
            visited.add(xy)

        # must only leave one cell free (the tree)
        empty_cells = Lawn._get_empty_cells_in_cell_set(visited)
        if len(empty_cells) != 1:
            log.debug(f"not exactly one unvisited cell: {empty_cells}")
            return False

        # assume that the empty cell is the tree and transform the coordinates
        # then check if we lawned all the cells in the origin grid
        to_be_lawn = self.get_valid_positions()
        tree_offset = self.tree - empty_cells.pop()
        for cell in visited:
            cell += tree_offset
            if cell not in to_be_lawn:
                log.debug(f"moved outside of grid: {cell}")
                return False
            to_be_lawn.remove(cell)

        if len(to_be_lawn) > 0:
            log.debug(f"not all cells lawned: {to_be_lawn}")
            return False

        return True

    @staticmethod
    def _get_empty_cells_in_cell_set(cells: Set[complex]) -> Set[complex]:
        tl, br = Lawn._get_corners_of_cell_set(cells)

        # within that bounding box, what cells are not in the set?
        empty = set()
        for y in range(int(tl.imag), int(br.imag) + 1):
            for x in range(int(tl.real), int(br.real) + 1):
                cell = complex(x, y)
                if cell not in cells:
                    empty.add(cell)

        return empty

    @staticmethod
    def _get_corners_of_cell_set(cells: Set[complex]) -> Tuple[complex, complex]:
        # given a set of cell points, return the top-left and bottom-right corners
        xmin, ymin = float("inf"), float("inf")
        xmax, ymax = float("-inf"), float("-inf")

        for cell in cells:
            xmin = min(xmin, cell.real)
            ymin = min(ymin, cell.imag)
            xmax = max(xmax, cell.real)
            ymax = max(ymax, cell.imag)

        return complex(xmin, ymin), complex(xmax, ymax)

    @staticmethod
    def _get_enclosed_rectangle_size_of_path(path: List[Direction]) -> complex:
        xy = 0
        xmin, ymin = 0, 0
        xmax, ymax = 0, 0

        for dir in path:
            xy = move_to(xy, dir)

            xmin = min(xmin, xy.real)
            ymin = min(ymin, xy.imag)
            xmax = max(xmax, xy.real)
            ymax = max(ymax, xy.imag)

        width = xmax - xmin + 1
        height = ymax - ymin + 1

        return width, height

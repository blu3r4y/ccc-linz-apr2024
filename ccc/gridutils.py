from typing import Literal, List

Direction = Literal["W", "A", "S", "D"]


def move_to(pos: complex, dir: Direction) -> complex:
    match dir:
        case "W":
            return pos - 1j
        case "A":
            return pos - 1
        case "S":
            return pos + 1j
        case "D":
            return pos + 1


def path_to_directions(path: List[complex]) -> List[Direction]:
    directions = []
    for i in range(1, len(path)):
        diff = path[i] - path[i - 1]
        if diff == 1:
            directions.append("D")
        elif diff == -1:
            directions.append("A")
        elif diff == 1j:
            directions.append("S")
        elif diff == -1j:
            directions.append("W")
    return "".join(directions)


def points_to_direction(a: complex, b: complex) -> Direction:
    diff = b - a
    if diff == 1:
        return "D"
    elif diff == -1:
        return "A"
    elif diff == 1j:
        return "S"
    elif diff == -1j:
        return "W"
    return "D"


def point_distance(a: complex, b: complex) -> float:
    return abs(a.real - b.real) + abs(a.imag - b.imag)

from typing import List, Literal


def solve(data):
    output = []
    for path in data["paths"]:
        w, h = enclosed_rectangle(path)
        output.append(f"{w} {h}")
    return "\n".join(output)


# a list of W, A, S, or D
def enclosed_rectangle(path: List[Literal["W", "A", "S", "D"]]) -> tuple[int, int]:
    x, y = 0, 0
    min_x, min_y = 0, 0
    max_x, max_y = 0, 0

    for dir in path:
        if dir == "W":
            y += 1
        elif dir == "A":
            x -= 1
        elif dir == "S":
            y -= 1
        elif dir == "D":
            x += 1

        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    return width, height

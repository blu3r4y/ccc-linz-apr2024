from .lawn import Lawn
from loguru import logger as log


def solve(data):
    output = []

    for lawn in data["lawns"]:
        print(lawn)
        lawn = Lawn(lawn.width, lawn.height, lawn.grid)
        path = lawn.find_path()
        assert lawn.is_path_valid(path)
        log.success(f"path is valid")
        output.append(path)

    return "\n".join(output)

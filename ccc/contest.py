from .lawn import Lawn


def solve(data):
    output = []

    for lawn in data["lawns"]:
        lawn = Lawn(lawn.width, lawn.height, lawn.grid, lawn.path)
        valid = lawn.is_path_valid(lawn.path)
        output.append("VALID" if valid else "INVALID")

    return "\n".join(output)

def solve(data):
    output = []
    for line in data["lines"]:
        num_w = line.count("W")
        num_d = line.count("D")
        num_s = line.count("S")
        num_a = line.count("A")
        output.append(f"{num_w} {num_d} {num_s} {num_a}")
    return "\n".join(output)
# Graf penerbangan: kota tujuan dan biaya tiket
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 2, 'E': 1, 'G': 12},
    'C': {'D': 2},
    'D': {'G': 3},
    'E': {'G': 6},
    'G': {}
}

# Estimasi biaya menuju Bali
heuristic = {
    'A': 10,
    'B': 8,
    'C': 6,
    'D': 3,
    'E': 5,
    'G': 0
}

start = 'A'
goal = 'G'


def search(node, cost, path, threshold):
    f = cost + heuristic[node]

    print(f"  Kunjungi {node}: g={cost}, h={heuristic[node]}, f={f}")

    if f > threshold:
        return f, None

    if node == goal:
        return f, (path, cost)

    min_exceeded = float('inf')

    for neighbor, edge_cost in graph[node].items():
        if neighbor in path:
            continue

        next_threshold, solution = search(
            neighbor,
            cost + edge_cost,
            path + [neighbor],
            threshold
        )

        if solution is not None:
            return next_threshold, solution

        min_exceeded = min(min_exceeded, next_threshold)

    return min_exceeded, None


def ida_star():
    threshold = heuristic[start]

    while True:
        print(f"\nThreshold = {threshold}")

        next_threshold, solution = search(
            start, 0, [start], threshold
        )

        if solution is not None:
            path, total_cost = solution
            return path, total_cost

        if next_threshold == float('inf'):
            return None, None

        threshold = next_threshold


path, total_cost = ida_star()

print("\n=== HASIL IDA* ===")

if path is not None:
    print("Jalur terbaik yang ditemukan:", " -> ".join(path))
    print("Total biaya:", total_cost)
else:
    print("Tidak ditemukan jalur menuju tujuan.")
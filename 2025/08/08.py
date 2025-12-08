
import numpy as np
from collections import defaultdict

def load(fname):
    with open(fname, "r") as file:
        grid = [
            [int(x) for x in row.strip("\n").split(",")]
            for row in file.readlines()
        ]

    return np.array(grid)


def connect_pairs(coords, n_to_connect=1000, n_largest_circuits=3):
    num_pts = len(coords)

    all_pairs = []
    ## Map each point to the index of the circuit which contains it
    circuit_index = {}
    ## Map each circuit index to the list of point it contains
    points_by_circuit = defaultdict(set)

    ## Compute the pairwise distance for each unique pair of points
    distances = np.zeros((num_pts, num_pts), dtype=float)
    for i in range(num_pts):
        p1 = coords[i]
        circuit_index[i] = i
        points_by_circuit[i].add(i)
        for j in range(i+1, num_pts):
            p2 = coords[j]
            all_pairs.append((i,j))
            distances[i,j] = np.linalg.norm(p1-p2, 2)
            distances[j,i] = distances[i][j]

    ## Get the list of paired coordinates, ordered by their pairwise distance
    pairs_sorted = sorted(all_pairs, key=lambda pt: distances[pt[0]][pt[1]])

    for i in range(min(n_to_connect, num_pts)):
        ## Connect the ith closest pair of points
        i1,i2 = pairs_sorted[i]
        c1_idx, c2_idx = circuit_index[i1], circuit_index[i2]
        circuit1, circuit2 = points_by_circuit[c1_idx], points_by_circuit[c2_idx]

        if len(circuit1) < len(circuit2):
            ## Merge c1 into c2
            for z in circuit1:
                circuit_index[z] = c2_idx
            points_by_circuit[c2_idx] = circuit1.union(circuit2)
        else:
            ## Merge c2 into c1
            for z in circuit2:
                circuit_index[z] = c1_idx
            points_by_circuit[c1_idx] = circuit2.union(circuit1)

    ## Get the size of each circuit
    circuit_sizes = [len(circuit) for circuit in points_by_circuit.values()]

    ## Multiply the k largest circuits
    circuit_sizes_sorted = sorted(circuit_sizes, reverse=True)
    n_circuits_to_pick = min(n_largest_circuits, len(circuit_sizes))
    return np.prod(circuit_sizes_sorted[:n_circuits_to_pick])
         



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    coordinates = load(fname)

    part_one = connect_pairs(coordinates, 1000, 3)
    print(f"Part 1: {part_one}")



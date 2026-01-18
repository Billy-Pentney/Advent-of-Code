
import numpy as np
from collections import defaultdict

def load(fname):
    with open(fname, "r") as file:
        grid = [
            [int(x) for x in row.strip("\n").split(",")]
            for row in file.readlines()
        ]

    return np.array(grid)


def connect_pairs(coords, n_to_connect, n_largest_circuits=1):
    num_pts = len(coords)

    ## Map each point to the index of the circuit which contains it
    circuit_index = {}
    ## Map each circuit index to the list of point it contains
    points_by_circuit = defaultdict(set)
    ## Store a list of (x,y) where x and y are the indices of two pairs
    unique_pairs = []

    ## Compute the pairwise distance for each unique pair of points
    distances = np.zeros((num_pts, num_pts), dtype=float)
    for i in range(num_pts):
        pt1 = coords[i]
        ## Add this point to a singleton circuit
        circuit_index[i] = i
        points_by_circuit[i].add(i)
        for j in range(i+1, num_pts):
            pt2 = coords[j]
            unique_pairs.append((i,j))
            ## L2-norm as a distance metric
            distances[i,j] = np.linalg.norm(pt1-pt2, 2)
            ## Symmetrical
            distances[j,i] = distances[i][j]

    ## Get the list of paired coordinates, ordered by their pairwise distance
    pairs_sorted = sorted(unique_pairs, key=lambda pt: distances[pt[0],pt[1]])

    find_last_pair = n_to_connect is None
    max_can_connect = len(unique_pairs) if find_last_pair else min(n_to_connect, len(unique_pairs)) 

    for i in range(max_can_connect):
        ## Connect the ith closest pair of points
        i1,i2 = pairs_sorted[i]
        c1_idx, c2_idx = circuit_index[i1], circuit_index[i2]

        if c1_idx == c2_idx:
            ## Skip the same circuit (nothing to connect)
            continue

        circuit1, circuit2 = points_by_circuit[c1_idx], points_by_circuit[c2_idx]

        ## ==== EARLY EXIT for PART 2! ====
        ## Check if this is the pair that connects the last two circuits
        if find_last_pair and len(points_by_circuit.keys()) == 2:
            ## Return the product of the X-coordinates of the final pair
            pt1, pt2 = coords[i1], coords[i2]
            return pt1[0] * pt2[0]

        ## Merge the smaller set into the larger
        if len(circuit1) < len(circuit2):
            ## Merge c1 into c2
            for z in circuit1:
                circuit_index[z] = c2_idx
            points_by_circuit[c2_idx] = circuit1.union(circuit2)
            points_by_circuit.pop(c1_idx)
        else:
            ## Merge c2 into c1
            for z in circuit2:
                circuit_index[z] = c1_idx
            points_by_circuit[c1_idx] = circuit2.union(circuit1)
            points_by_circuit.pop(c2_idx)

    ## Get the size of each circuit
    circuit_sizes = [len(circuit) for circuit in points_by_circuit.values()]

    ## Multiply the k largest circuits
    circuit_sizes_sorted = sorted(circuit_sizes, reverse=True)
    n_circuits_to_pick = 0 if n_largest_circuits is None else min(n_largest_circuits, len(circuit_sizes))
    return np.prod(circuit_sizes_sorted[:n_circuits_to_pick])
         



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    coordinates = load(fname)

    part_one = connect_pairs(coordinates, n_to_connect=1000, n_largest_circuits=3)
    print(f"Part 1: {part_one}")

    part_two = connect_pairs(coordinates, n_to_connect=None)
    print(f"Part 2: {part_two}")


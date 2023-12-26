import sys, os
import re


line_pattern = "(\w+):((?: \w+)+)\n?"
def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    edge_map = {}

    # Construct an adjacency list representation
    for line in lines:
        match = re.match(line_pattern, line)
        if match:
            source = match.group(1)
            dests = match.group(2)
            for dest in dests.split(" "):
                if len(dest) > 0:
                    # Add edges in both directions
                    if source not in edge_map.keys():
                        edge_map[source] = set()
                    edge_map[source].add(dest)
                    if dest not in edge_map.keys():
                        edge_map[dest] = set()
                    edge_map[dest].add(source)

    return edge_map


def find_connected_components(edge_map):
    queue = []
    nodes = list(edge_map.keys())

    groups = []

    # BFS starting at each unvisited node
    while len(nodes) > 0:
        queue.append(nodes[0])
        visited = set()
        seen = set()

        while len(queue) > 0:
            curr = queue[0]
            queue = queue[1:]
            visited.add(curr)
            for nb in edge_map[curr]:
                if nb in visited or nb in seen:
                    continue
                else:
                    seen.add(nb)
                    queue.append(nb)

        for node in visited:
            nodes.remove(node)
        
        groups.append(visited)

    return groups


# Identify edges whose endpoints do not share another common node
def find_key_edges(edge_map):
    candidate_edges = []
    for n1 in edge_map.keys():
        for n2 in edge_map[n1]:
            # Find all nodes which both n1 and n2 are incident to
            common_endpoints = edge_map[n1].intersection(edge_map[n2])

            # print(f"{n1} vs {n2} = {common_endpoints}")

            # If the two endpoints have no other incident edges in common
            # and we haven't already added the edge in the opposite direction
            if len(common_endpoints) == 0 and (n2, n1) not in candidate_edges:
                candidate_edges.append((n1, n2))

    return candidate_edges


## Deep copy an edge_map (allowing for elements to be changed without affecting original)
def copy_edge_map(edge_map):
    new_map = {}
    for name, edge_set in edge_map.items():
        new_map[name] = edge_set.copy()
    return new_map



## Input: an edge_map, and num_edges_to_remove = 3

## 1: Find all candidate edges (those whose endpoints are not incident to any common vertices)
## 2: For each candidate edge E=(u,v).
##  2.0: Remove edge E and decrement num_edges_to_remove by 1
##  2.1: Let Adj(u) be all nodes adjacent to u
##  2.2: Let Adj(v) be all nodes adjacent to v
##  2.5: Let B = A(u) intersect A(v).
##  2.7: If B is not empty, let b be any node in B. 
    ##       Let X be the set of nodes in A(u) incident to b. Let Y be the same for A(v).
    ##  2.8: If |X| < |Y| and |X| < num_edges_to_remove, then remove all edges {x,b} for x in X.
    ##          Else if |Y| < num_edges_to_remove, then remove all edges {y,b} for y in Y.
    ##          Else break (no solution for this original edge E).
##  2.9: Continue extending the adjacency until all nodes have been included

def find_groupings_for_edge(edge, new_edge_map, num_edges_to_remove, verbose=False):
    (a,b) = edge
    edges_removed = []
    edges_removed.append((a,b))

    A_queue, B_queue = [a],[b]
    A, B = set([a]), set([b])

    if verbose:
        print(f"\nRunning on ({a},{b})")

    while len(A_queue) > 0 and len(B_queue) > 0:
        new_A_queue = []
        for a in A_queue:
            new_A_queue.extend(new_edge_map[a].difference(A))
            A = A.union(new_edge_map[a])
            # print(" >> New A:", A)
        A_queue = new_A_queue
        
        new_B_queue = []
        for b in B_queue:
            new_B_queue.extend(new_edge_map[b].difference(B))
            B = B.union(new_edge_map[b])
            # print(" >> New B:", B)
        B_queue = new_B_queue

        # Find all nodes which appear in both A and B
        AB_intersect = A.intersection(B)

        # Not allowed to remove an edge from each node which needs it
        if len(AB_intersect) > num_edges_to_remove:
            if verbose:
                print("Early Exit: Insufficient edges to separate groups!")
            return None

        # We need to resolve the intersection by individually
        # disconnecting each node from one of the sets A or B.
        for P in AB_intersect:
            adj_in_A = new_edge_map[P].intersection(A)
            adj_in_B = new_edge_map[P].intersection(B)

            # Choose to disconnect side which has the fewest edges to remove
            if len(adj_in_A) < len(adj_in_B) and len(adj_in_A) <= num_edges_to_remove:
                # Separate A from P
                for a_ in adj_in_A:
                    new_edge_map[P].remove(a_)
                    new_edge_map[a_].remove(P)
                    edges_removed.append((P,a_))
                    if verbose:
                        print(f"Removed edge ({P},{a_})")

                A.remove(P)
                A_queue.remove(P)
                num_edges_to_remove -= len(adj_in_A)

            elif len(adj_in_B) <= num_edges_to_remove:
                # Separate P from B
                for b_ in adj_in_B:
                    new_edge_map[P].remove(b_)
                    new_edge_map[b_].remove(P)
                    edges_removed.append((P,b_))
                    if verbose:
                        print(f"Removed edge ({P},{b_})")

                B.remove(P)
                B_queue.remove(P)
                num_edges_to_remove -= len(adj_in_B)

            # Cannot remove any additional edges
            elif len(adj_in_B) > 0:
                return None
    
    return new_edge_map, edges_removed

def bfs_grouping(edge_map, num_edges_to_remove=3):
    candidate_edges = find_key_edges(edge_map)
    print(f"Found {len(candidate_edges)} suitable edges to test")
    # candidate_edges.sort(key=lambda e: e[0])

    # original_edges_to_remove = num_edges_to_remove

    # Check every candidate edge which is suitable
    for (a,b) in candidate_edges:
        # Duplicate the map, so changes can be discarded
        new_edge_map = copy_edge_map(edge_map)
        # Remove the edge from the copy only
        new_edge_map[a].remove(b)
        new_edge_map[b].remove(a)

        # Run on this edge, attempting to split the graph
        solution = find_groupings_for_edge((a,b), new_edge_map, num_edges_to_remove)

        if solution is not None:
            edge_map, edges_removed = solution 

            # Find the distinct groups when the required edges have been removed
            cc_groups = find_connected_components(edge_map)
            return cc_groups, edges_removed

    return None
        





## Solve Part One
def part_one(fileaddr):
    edge_map = read_file(fileaddr)
    result = bfs_grouping(edge_map, 3)

    if result is not None:
        components = result[0]
        removed_edges = result[1]
        print("Solution found by removing edges:", removed_edges)
        
        # Compute the product of the sizes of the components
        comp_prod = 1
        for i,comp in enumerate(components):
            # print(f"CC #{i}: {comp}")
            comp_prod *= len(comp) 
        return comp_prod

    return None


## Solve Part Two
def part_two(fileaddr):
    return










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if (part == '1'):
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    


import numpy as np


def load(fname):
    with open(fname, "r") as file:
        conns = [row.strip("\n") for row in file.readlines()]

    # Parse the connections to form an adjacency-list.
    adj_list = {}
    for conn in conns:
        splits = conn.split("-")
        comp_1 = splits[0]
        comp_2 = splits[1]
        if comp_1 not in adj_list.keys():
            adj_list[comp_1] = set()
        if comp_2 not in adj_list.keys():
            adj_list[comp_2] = set()
        adj_list[comp_1].add(comp_2)
        adj_list[comp_2].add(comp_1)

    return adj_list


def find_connected_triples(adj_list, required_prefix='t', verbose=False):
    """
        Solves Part 1, by computing all interconnected triples and counting those that start with the given prefix.
        An interconnected triple is a set of exactly three distinct nodes (x,y,z) such that edges (x,y), (x,z) and (y,z) all appear in the graph.

        Params
        ---
        adj_list: dict[str, list[str]]
            The adjacency-list representing the graph.
        required_prefix: str
            A string which must appear at the start of at least one node in each triple for it to be counted. 
            Pass the empty string to count all triples.
        verbose: bool, default=False
            If true, triples are printed.
    
        Returns
        ---
        The number of connected triples that start with the given prefix.
    """

    comps = list(adj_list.keys())
    n_comps = len(comps)

    n_selected_triples = 0 

    ## To avoid duplicate triples, we only check for j < i and k < j.

    for i in range(2, n_comps):
        c1 = comps[i]
        
        for j in range(1, i):
            c2 = comps[j]

            if c2 not in adj_list[c1]:
                continue

            for k in range(j):
                c3 = comps[k]
                
                if c3 not in adj_list[c1] or c3 not in adj_list[c2]:
                    continue

                if c1.startswith(required_prefix) or c2.startswith(required_prefix) or c3.startswith(required_prefix):
                    if verbose:
                        print(c1,c2,c3)
                    n_selected_triples += 1

    return n_selected_triples




def find_max_clique(adj_list, clique=set()):
    """
        Finds the largest clique on the given edge-list which contains the given clique.
        A clique is a set of nodes which are fully interconnected, i.e. for every pair of nodes x,y in the clique, there is an edge (x,y) in the graph.
        This method find the (unique) clique of maximum size which contains all nodes in the given clique.
        This implementation uses a backtracking Depth-First-Search to exhaustively find the largest clique.
        
        Params
        ----
        adj_list: dict[str, list[str]]
            The edge-list representing the graph.

        clique: set (of integer node/computer names)
            The starting point for the clique; all nodes in this set must be in the final returned set.

        Returns
        ----
        A clique of maximum size which contains all nodes in the `clique` parameter.
    """
    max_clique = clique.copy()    
    users = set(adj_list.keys())

    possible_new_users = users.difference(clique)

    for user in possible_new_users:
        ## Exclude any users that we know are in the current best
        ## as we would have found the largest clique including them.
        if user in max_clique:
            continue
        
        ## If this user is connected to the set so far...
        if len(adj_list[user].intersection(clique)) == len(clique):
            ## Try adding it
            connected_with_user = clique.copy()
            connected_with_user.add(user)

            ## Recursively find the largest set with that user
            clique_result = find_max_clique(adj_list, connected_with_user)
            if len(clique_result) > len(max_clique):
                max_clique = clique_result
                possible_new_users = possible_new_users.difference(clique_result)

    # print(f"New max clique! {max_clique}")
    return max_clique




def find_password(adj_list):
    """
        Solves part 2 by using backtracking search to find the maximum clique.
    """
    largest_interconnected = find_max_clique(adj_list, set())

    ## Sort alphabetically and concatenate the users with a comma
    password = ",".join(list(sorted(largest_interconnected)))
    return password




from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    adj_list = load(fname)

    n_triples_with_t = find_connected_triples(adj_list, 't', verbose=False)
    print(f"(Part 1) Num triples with 't' start: {n_triples_with_t}")

    password = find_password(adj_list)
    print(f"(Part 2) Password: {password}")
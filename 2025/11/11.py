
import numpy as np
from collections import defaultdict

def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    edges = defaultdict(set)
    rev_edges = defaultdict(set)

    for line in lines:
        splits = line.split(": ")
        pre = splits[0]
        for post in splits[1].split(" "):
            edges[pre].add(post)
            rev_edges[post].add(pre)

    return edges, rev_edges

from queue import Queue

def find_topo_sort(node, vis, adj, stack):
    vis[node] = 1
    for it in adj[node]:
        if vis[it] == 0:
            find_topo_sort(it, vis, adj, stack)
    
    # push the node after all its neighbours
    stack.append(node)


def topological_sort(edges):
    stack = []
    vis = defaultdict(lambda: 0)

    nodes = list(edges.keys())
    for node in nodes:
        if vis[node] == 0:
            find_topo_sort(node, vis, edges, stack)

    ordering = []

    ## Reverse the order
    while stack:
        ordering.append(stack.pop())

    # ordering.reverse()
    return ordering



def count_routes(edges, start, end):
    num_routes_to = defaultdict(lambda: 0)
    num_routes_to[start] = 1
    ts = topological_sort(edges)

    for curr in ts:
        for child in edges[curr]:
            num_routes_to[child] += num_routes_to[curr]

    # print(num_routes_to.items())
    return num_routes_to[end]

def count_routes_with_stops(edges, start, end, required_stops):
    total_paths = 1
    prev = start

    ## Find the number of paths between each pair of consecutive stops that have to be visited
    for req_stop in required_stops + [end]:
        hop_paths = count_routes(edges, prev, req_stop)
        print(f"Paths from {prev} to {req_stop}: {hop_paths}")
        if hop_paths == 0:
            print("No paths on this hop (exiting early!)")
            break
        ## Multiplicative, as we can take any combination of path segments
        total_paths *= hop_paths
        prev = req_stop

    return total_paths



from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    edges, rev_edges = load(fname)

    # n_routes_you_out = count_routes(edges, "you", "out")
    # print("Part 1:", n_routes_you_out)

    if fname == "example.txt":
        n_routes_part_2 = count_routes_with_stops(edges, "you", "out", ["ccc"])
    else:
        dac_then_fft = count_routes_with_stops(edges, "svr", "out", ["dac", "fft"])
        fft_then_dac = count_routes_with_stops(edges, "svr", "out", ["fft", "dac"])
        n_routes_part_2 = dac_then_fft + fft_then_dac

    print("Part 2:", n_routes_part_2)
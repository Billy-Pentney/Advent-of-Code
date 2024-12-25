


import regex as re
from os.path import exists

def load_file(fname, n_lists: int = 2):
    lists = [[] for _ in range(n_lists)]

    if not exists(fname):
        raise FileNotFoundError(f"'{fname}' not found!")
    
    print(f"Loading from {fname}...")

    with open(fname, "r") as file:
        for line in file.readlines():
            matches = re.findall("\d+", line)
            for i, match in enumerate(matches):
                lists[i].append(int(match))

    return lists

def part_one(lists):
    sorted_lists = [sorted(l) for l in lists]

    total_dist = 0
    for i in range(len(sorted_lists[0])):
        x = sorted_lists[0][i]
        y = sorted_lists[1][i]
        total_dist += abs(x - y)

    return total_dist


def part_two(lists):
    list2_counts = {}
    for num in lists[1]:
        list2_counts[num] = list2_counts.get(num, 0)+1
    
    total_sim = 0
    for num in lists[0]:
        total_sim += num * list2_counts.get(num, 0)

    return total_sim



from sys import argv

if __name__ == '__main__':
    
    if len(argv) < 1:
        print("No filename supplied")
        exit(1)

    fname = argv[1]
    lists = load_file(fname)
    # print(nums)

    print(f"(Part 1) Total Distance: {part_one(lists)}")
    print(f"(Part 2) Total Similarity: {part_two(lists)}")


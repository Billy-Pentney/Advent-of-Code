import sys, os
import re


class Mapping:
    def __init__(self, name, map_lines):
        self.name = name
        self.mappings = map_lines

    def __repr__(self):
        return f"(Mapping {self.name}, with {len(self.mappings)} maps)"

    def apply(self, source):
        for map in self.mappings:
            if map[1] <= source and source <= map[1]+map[2]:
                return map[0] + source-map[1]
        # otherwise no change
        return source


map_line_pattern = "(\d+) (\d+) (\d+)"


def parse_seeds(line):
    pattern = "seeds: (\d+(?: \d+)*)"
    match = re.match(pattern, line)
    if not match:
        return None

    seed_nums = match.group(1)
    seeds = [int(s) for s in seed_nums.split(" ")]
    return seeds


def convert_seed_ranges(seed_ranges):
    new_seeds = []

    # Convert the seed ranges to a list of seeds
    for i in range(0, len(seed_ranges), 2):
        seed_start = seed_ranges[i]
        seed_end = seed_ranges[i]+seed_ranges[i+1]
        new_seeds.extend(list(range(seed_start, seed_end)))
    
    return new_seeds



def parse_range_map_line(line):
    match = re.match(map_line_pattern, line)
    if not match:
        return None
    
    dest_start = int(match.group(1))
    source_start = int(match.group(2))
    source_len = int(match.group(3))
    v = (dest_start, source_start, source_len)
    return v



def parse_map(lines: [str]):
    map_names = ["seed-to-soil",
                 "soil-to-fertilizer",
                 "fertilizer-to-water",
                 "water-to-light",
                 "light-to-temperature",
                 "temperature-to-humidity",
                 "humidity-to-location"]

    map_name_i = 0
    maps = []
    curr_mappings = []

    for line in lines:
        if line.startswith("\n"):
            mapping = Mapping(map_names[map_name_i], curr_mappings)
            maps.append(mapping)
            curr_mappings = []
            map_name_i += 1
        else:
            map_line = parse_range_map_line(line)
            if (map_line != None):
                curr_mappings.append(map_line)

    mapping = Mapping(map_names[map_name_i], curr_mappings)
    maps.append(mapping)

    print(maps)
    return maps
            


def part_one(fileaddr, part='1'):
    lines=[]
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    seeds = parse_seeds(lines[0])
    if part == '2':
        seeds = convert_seed_ranges(seeds)
    print(seeds)
    maps = parse_map(lines[2:])

    min_location = None
    for seed in seeds:
        val = seed
        for map in maps:
            val = map.apply(val)
        
        if min_location is None or val < min_location:
            min_location = val

    return min_location



def part_two(fileaddr):
    ## Solve Part Two
    return











if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        result = part_one(fileaddr, part)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    

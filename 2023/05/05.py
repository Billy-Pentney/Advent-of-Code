import sys, os
import re


class Mapping:
    def __init__(self, dest_start, source_start, length):
        self.dest_start = dest_start
        self.source_start = source_start
        self.length = length
        self.source_end = source_start + length -1
        self.dest_end = dest_start + length - 1
    
    def apply_to_val(self, val):
        if self.source_start <= val and val <= self.source_end:
            return self.dest_start + val - self.source_start
        return val 
    
    def apply_to_range(self, range):
        start = range[0]
        end = range[1]

        # Case 1: All before or after the mapping
        if end < self.source_start or self.source_end < start:
            return [range]
        
        dest_ranges = []
        unmapped_ranges = []
        
        if start < self.source_start:
            unmapped_ranges.append((start, self.source_start-1))
        
        map_start = self.dest_start + max(start, self.source_start) - self.source_start
        map_end = self.dest_start + min(end, self.source_end) - self.source_start
        dest_ranges.append((map_start, map_end))

        if self.source_end < end:
            unmapped_ranges.append((self.source_end+1, end))

        return dest_ranges, unmapped_ranges
    
    def val_in_domain(self, val):
        # print(self.dest_start, self.dest_end)
        return self.dest_start <= val and val <= self.dest_end 
    
    def __repr__(self):
        return f"Mapping ({self.dest_start}, {self.source_start}, {self.length})"

        

class Function:
    def __init__(self, name, mappings):
        self.name = name
        self.mappings = sorted(mappings, key=lambda m: m.source_start)
        # Sort the mappings by source start, so we can apply Binary Search

    def __repr__(self):
        return f"(Mapping {self.name}, with {len(self.mappings)} maps)"

    def apply(self, source):
        for map in self.mappings:
            if map.source_start <= source and source <= map.source_end:
                return map.dest_start + source - map.source_start
        # otherwise no change
        return source

    def bin_search_for_mapping(self, val):
        l = 0
        r = len(self.mappings)-1

        while l <= r:
            m = int(l+(r-l)/2)
            mapping = self.mappings[m]
            if mapping.source_start <= val and val <= mapping.source_end:
                return mapping
            elif val < mapping.source_start:
                r = m-1
            else:
                l = m+1


    def bin_apply(self, source):
        mapping = self.bin_search_for_mapping(source)
        if mapping:
            return mapping.dest_start + source - mapping.source_start
        ## Otherwise, use default
        return source
    

    def get_source(self, dest_val):
        # print(f"Attempting to reverse {dest_val}")
        for map in self.mappings:
            if map.val_in_domain(dest_val):
                diff = dest_val - map.dest_start
                return map.source_start + diff
        # print("not in domain")
        return dest_val
    

    def apply_to_range(self, range):
        # range[0] = start, range[1] = end

        source_ranges = [range]
        dest_ranges = []

        # print(self, " on", range)

        for map in self.mappings:
            map_start = map.source_start
            map_end = map.source_end

            # print("Considering", map)

            range = source_ranges[0]

            if map_end < range[0]:
                # We are before any suitable mappings
                continue
            
            if range[1] < map_start:
                # Exceeded all suitable mappings
                dest_ranges.append(range)
                break 
            else:
                source_ranges = source_ranges[1:]
                # print("Mapping on", range)
                map_dest_ranges, map_unmapped_ranges = map.apply_to_range(range)
                # print(map_dest_ranges)
                # print(map_unmapped_ranges)

                for unmap_range in map_unmapped_ranges:
                    # Range is after the current mapping - may still be mapped by a subsequent mapping
                    if unmap_range[0] > map.source_end:
                        source_ranges.append(unmap_range)
                    # Range is before current mapping - was not previously mapped, so is fixed
                    else:
                        map_dest_ranges.append(unmap_range)

                dest_ranges.extend(map_dest_ranges)

            if len(source_ranges) == 0:
                break

        # Keep all unchanged regions
        dest_ranges.extend(source_ranges)
            
        return dest_ranges





map_line_pattern = "(\d+) (\d+) (\d+)"


def parse_seeds(line):
    pattern = "seeds: (\d+(?: \d+)*)"
    match = re.match(pattern, line)
    if not match:
        return None

    seed_nums = match.group(1)
    seeds = [int(s) for s in seed_nums.split(" ")]
    return seeds


def parse_seed_ranges(line):
    all_values = parse_seeds(line)
    ranges = []

    # Take each consecutive pair and make it into a range
    for i in range(0, len(all_values), 2):
        start = all_values[i]
        length = all_values[i+1]
        ranges.append((start, start+length-1))
    
    return ranges



def parse_range_map_line(line):
    match = re.match(map_line_pattern, line)
    if not match:
        return None
    
    dest_start = int(match.group(1))
    source_start = int(match.group(2))
    length = int(match.group(3))
    return Mapping(dest_start, source_start, length)



def parse_function_maps(lines: [str]):
    map_names = ["seed-to-soil",
                 "soil-to-fertilizer",
                 "fertilizer-to-water",
                 "water-to-light",
                 "light-to-temperature",
                 "temperature-to-humidity",
                 "humidity-to-location"]

    map_name_i = 0
    funcmaps = []
    curr_mappings = []

    for line in lines:
        if line.startswith("\n"):
            func = Function(map_names[map_name_i], curr_mappings)
            funcmaps.append(func)
            curr_mappings = []
            map_name_i += 1
        else:
            map_line = parse_range_map_line(line)
            if (map_line != None):
                curr_mappings.append(map_line)

    if len(curr_mappings) > 0:
        func = Function(map_names[map_name_i], curr_mappings)
        funcmaps.append(func)

    # print(funcmaps)
    return funcmaps
            


def part_one(fileaddr):
    lines=[]
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    seeds = parse_seeds(lines[0])
    print(seeds)
    maps = parse_function_maps(lines[2:])

    min_location = None
    for seed in seeds:
        val = seed
        for map in maps:
            val = map.bin_apply(val)

        if min_location is None or val < min_location:
            min_location = val

    return min_location



def part_two(fileaddr):
    lines=[]
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    ranges = parse_seed_ranges(lines[0])

    # print("Original ranges:", ranges)
    funcmaps = parse_function_maps(lines[2:])

    all_ranges = ranges

    min_location = None
    for funcmap in funcmaps:
        mapped_ranges = []
        # print(f"Applying {funcmap.name}:")
        for sd_range in all_ranges:
            new_ranges = funcmap.apply_to_range(sd_range)
            if new_ranges is not None:
                mapped_ranges.extend(new_ranges)
            # print(f" >> {sd_range} -> {new_ranges}")

        all_ranges = mapped_ranges

    min_location = min([range[0] for range in all_ranges])
    # print("Mapped ranges:", all_ranges)
    # print("Minimum location", min_location)

    # Reverse mapping to get source_value (unneeded)
    # min_val = min_location
    # for func in reversed(funcmaps):
    #     min_val = func.get_source(min_val)

    # min_seed = min_val
    # print(f"{min_location} is obtained from seed {min_seed}")

    return min_location











if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if part == '1':
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    

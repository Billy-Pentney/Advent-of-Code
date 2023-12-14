import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    for i in range(0, len(lines)):
        lines[i] = list(lines[i].replace("\n", ""))
    return lines


def print_map(lines):
    for line in lines:
        print("".join(line))


# Locate all round rocks (denoted 'O') in the given map
# Returns a list, where the ith element is a list of the columns c
# for which a round rock is found at position (i,c)
def identify_rocks(map):
    round_rocks = [[] for row in map]

    for row, line in enumerate(map):
        for col, cell in enumerate(line):
            if cell == 'O':
                round_rocks[row].append(col)

    return round_rocks




def tilt_lever_north(lines, rocks_by_row):
    num_moved = 0
    new_rocks = [[] for line in rocks_by_row]
    new_lines = lines.copy()

    # Left-to-right, top-to-bottom
    for row in range(0, len(rocks_by_row)):
        for col in rocks_by_row[row]:
            r = row
            while r > 0 and new_lines[r-1][col] == '.':
                new_lines[r][col] = '.'
                r -= 1
                num_moved += 1
            new_lines[r][col] = 'O'
            new_rocks[r].append(col)

    # Order the rocks in each row (so they can be read left-to-right)
    for i in range(0, len(new_rocks)):
        new_rocks[i].sort()
    
    return new_lines, new_rocks, num_moved

def tilt_lever_east(lines, rocks_by_row):
    num_moved = 0
    new_rocks = [[] for line in rocks_by_row]
    new_lines = lines.copy()

    # Top-to-bottom, right-to-left
    for row in range(0, len(rocks_by_row)):
        for col in reversed(rocks_by_row[row]):
            c = col
            while c < len(new_lines[0])-1 and new_lines[row][c+1] == '.':
                new_lines[row][c] = '.'
                c += 1
                num_moved += 1
            new_lines[row][c] = 'O'
            new_rocks[row].append(c)
    
    return new_lines, new_rocks, num_moved
        
def tilt_lever_south(lines, rocks_by_row):
    num_moved = 0
    new_rocks = [[] for line in rocks_by_row]
    new_lines = lines.copy()

    # Bottom-to-top, left-to-right
    for row in range(len(rocks_by_row)-1, -1, -1):
        for col in reversed(rocks_by_row[row]):
            r = row
            while r < len(new_lines)-1 and new_lines[r+1][col] == '.':
                new_lines[r][col] = '.'
                r += 1
                num_moved += 1

            new_lines[r][col] = 'O'
            new_rocks[r].append(col)
        
    # Order the rocks in each row (so they can be read left-to-right)
    for i in range(0, len(new_rocks)):
        new_rocks[i].sort()
    
    return new_lines, new_rocks, num_moved

def tilt_lever_west(lines, rocks_by_row):
    num_moved = 0
    new_rocks = [[] for line in rocks_by_row]
    new_lines = lines.copy()

    # Left-to-right, top-to-bottom
    for row in range(0, len(rocks_by_row)):
        for col in rocks_by_row[row]:
            c = col
            while c > 0 and new_lines[row][c-1] == '.':
                new_lines[row][c] = '.'
                c -= 1
                num_moved += 1

            new_lines[row][c] = 'O'
            new_rocks[row].append(c)
    
    return new_lines, new_rocks, num_moved





# Performs one cycle of North,West,South,East tilts
def tilt_cycle(map, rocks):

    new_map = map.copy()
    new_rocks = rocks.copy()
        
    north_map, north_rocks, n = tilt_lever_north(new_map, new_rocks)
    # print("", "*"*20, " North (^)")
    # print_map(north_map)    

    west_map, west_rocks, w = tilt_lever_west(north_map, north_rocks)
    # print("", "*"*20, " West (<-)")
    # print_map(west_map)

    south_map, south_rocks, s = tilt_lever_south(west_map, west_rocks)
    # print("", "*"*20, " South (v)")
    # print_map(south_map)

    east_map, east_rocks, e = tilt_lever_east(south_map, south_rocks)
    # print("", "*"*20, " East (->)")
    # print_map(east_map)
    # print("-----------------")

    return east_map, east_rocks, (n+e+s+w)
    

def are_rocks_identical(rocks, other_rocks):
    for row in range(0,len(rocks)):
        if len(rocks[row]) != len(other_rocks[row]):
            return False
        for col in range(0, len(rocks[row])):
            if rocks[row][col] != other_rocks[row][col]:
                return False

    return True


# Return the map and rock positions after performing n complete cycles
def tilt_n_cycles(map, rocks, n):
    history = []

    for i in range(0, n):
        history.append((map.copy(), rocks.copy()))

        map, rocks, moves = tilt_cycle(map, rocks)

        # If nothing moved this cycle, then nothing will move next cycle
        if moves == 0:
            print("Early exit! Nothing moved!")
            return map, rocks
        
        # Check if we've seen this configuration of rocks before
        for h, (old_map, old_rocks) in enumerate(history):
            if are_rocks_identical(rocks, old_rocks):
                # After i+1 cycles, we have the same configuration as after the hth cycle
                loop_len = (i+1) - h
                print(f"Early exit! ({h},{i+1}) is a loop of length {loop_len}") 
                
                # We only need to know where the nth cycle falls in the loop
                remainder = (n - h) % loop_len
                print(f"n={n} lies {remainder} cycles after the loop")
                           
                return history[h + remainder]

    return map, rocks



def compute_total_load(map, round_rocks):
    rocks_in_row = []
    for i, row in enumerate(round_rocks):
        rocks_in_row.append(len(row) * (len(map)-i))
    return sum(rocks_in_row)



## Solve Part One
def part_one(fileaddr):
    map = read_file(fileaddr)
    
    round_rocks = identify_rocks(map)
    print(round_rocks)

    map, round_rocks, num_moves = tilt_lever_north(map, round_rocks)
    print_map(map)

    return compute_total_load(map, round_rocks)



## Solve Part Two
def part_two(fileaddr):
    map = read_file(fileaddr)
    
    round_rocks = identify_rocks(map)

    # Number of cycles to be performed
    cycles = 1000000000

    map, round_rocks = tilt_n_cycles(map, round_rocks, cycles)

    print_map(map)

    return compute_total_load(map, round_rocks)











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
    

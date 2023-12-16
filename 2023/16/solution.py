import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return [line.replace("\n", "") for line in lines]


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


def get_next_cell_in_dir(lines, pos, dir):

    if dir == NORTH and pos[1] > 0:
        return (pos[0], pos[1]-1)
    elif dir == EAST and pos[0] < len(lines[0])-1:
        return (pos[0]+1, pos[1])
    elif dir == SOUTH and pos[1] < len(lines)-1:
        return (pos[0], pos[1]+1)
    elif dir == WEST and pos[0] > 0:
        return (pos[0]-1, pos[1])
    
    return None


def find_next_beam_states(lines, beam_state):
    # Coordinates of beam in the grid
    pos = beam_state[0]
    # Direction of travel (number 0-3)
    dir = beam_state[1]

    next_pos = get_next_cell_in_dir(lines, pos, dir)
    if next_pos is None:
        return []

    # Index by y, then x
    next_cell = lines[next_pos[1]][next_pos[0]]

    next_states = []

    if next_cell == '-':
        if dir == NORTH or dir == SOUTH:
            # Split horizontally
            next_states.append((next_pos, EAST))
            next_states.append((next_pos, WEST))
        elif dir == EAST or dir == WEST:
            # Continue parallel to the splitter
            next_states.append((next_pos, dir))
    elif next_cell == '|':
        if dir == EAST or dir == WEST:
            # Split vertically 
            next_states.append((next_pos, NORTH))
            next_states.append((next_pos, SOUTH))
        elif dir == NORTH or dir == SOUTH:
            # Continue parallel to splitter
            next_states.append((next_pos, dir))
    elif next_cell == '/':
        if dir == EAST:
            # Reflect Up
            next_states.append((next_pos, NORTH))
        elif dir == WEST:
            # Reflect Down
            next_states.append((next_pos, SOUTH))
        elif dir == NORTH:
            # Reflect Right
            next_states.append((next_pos, EAST))
        elif dir == SOUTH:
            # Reflect Left
            next_states.append((next_pos, WEST))
    elif next_cell == '\\':
        if dir == EAST:
            # Reflect down
            next_states.append((next_pos, SOUTH))
        elif dir == WEST:
            # Reflect Up
            next_states.append((next_pos, NORTH))
        elif dir == NORTH:
            # Reflect Left
            next_states.append((next_pos, WEST))
        elif dir == SOUTH:
            # Reflect Right
            next_states.append((next_pos, EAST))
    else:
        # Otheriwse, continue in the current direction
        next_states.append((next_pos, dir))

    return next_states



## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)

    beams = [((-1,0),EAST)]
    energized_states = set()
    
    num_energized = 0
    new_map = [list('.'*len(line)) for line in lines]

    while len(beams) > 0:
        beam_state = beams[0]
        beams = beams[1:]
        
        # Mark this (position, direction) combination as having been visited by the beam
        # This will prevent infinite loops if a beam revisits a cell from the same direction
        energized_states.add(beam_state)

        # Mark this cell as having been touched by the beam
        x,y = beam_state[0]
        if x >= 0 and new_map[y][x] == '.':
            new_map[y][x] = '#'
            num_energized += 1

        for state in find_next_beam_states(lines, beam_state):
            if state not in energized_states:
                # print("Beam visited", state)
                beams.append(state)

    
    print("Energized map:")
    for line in new_map:
        print("     ","".join(line))

    return num_energized


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
    

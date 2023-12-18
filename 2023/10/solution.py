import sys, os
import re


"""
    | = vertical pipe connecting north and south.
    - = horizontal pipe connecting east and west.
    L = 90-degree bend connecting north and east.
    J = 90-degree bend connecting north and west.
    7 = 90-degree bend connecting south and west.
    F = 90-degree bend connecting south and east.
    . = no pipe in this tile.
    S = starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""

# MOVEMENT
UP = 'UP'
RIGHT = 'RIGHT'
DOWN = 'DOWN'
LEFT = 'LEFT'

VPIPE = '|'
HPIPE = '-'
LD = '7'
LU = 'J'
RD = 'F'
RU = 'L'


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return [line.replace("\n", "") for line in lines]


def get_enterable_neighbours(lines, start_pos, prev_pos=(-1,-1)):
    nbs = []
    (row, col) = start_pos
    (prow, pcol) = prev_pos

    # Move North from current
    if row > 0 and lines[row-1][col] in [VPIPE, LD, RD]:
        nbs.append((row-1,col,UP))
    # Move East from current
    if col < len(lines[row])-1 and lines[row][col+1] in [HPIPE, LU, LD]:
        nbs.append((row,col+1,RIGHT))
    # Move South from current
    if row < len(lines)-1 and lines[row+1][col] in [VPIPE, LD, RD]:
        nbs.append((row+1,col,DOWN))
    # Move West from current
    if col > 0 and lines[row][col-1] in [HPIPE, RU, RD]:
        nbs.append((row,col-1,LEFT))
    
    return [nb for nb in nbs if nb[0] != prow or nb[1] != pcol]



def get_next_cell_on_path(curr, curr_pos, prev_pos=(-1,-1)):
    (row, col) = curr_pos
    (prow, pcol) = prev_pos
    candidates = []

    if curr == VPIPE:   candidates = [(row-1,col,UP), (row+1,col,DOWN)]
    elif curr == HPIPE: candidates = [(row,col-1,LEFT), (row,col+1,RIGHT)]
    elif curr == RD:    candidates = [(row,col+1,RIGHT), (row+1,col,DOWN)]
    elif curr == LD:    candidates = [(row,col-1,LEFT), (row+1,col,DOWN)]
    elif curr == RU:    candidates = [(row,col+1,RIGHT), (row-1,col,UP)]
    elif curr == LU:    candidates = [(row,col-1,LEFT), (row-1,col,UP)]        

    return [nb for nb in candidates if nb[0] != prow or nb[1] != pcol]


def find_start_pos(lines):
    for r, line in enumerate(lines):
        for c, cell in enumerate(line):
            if (cell == 'S'):
                start_pos = (r,c)
    return start_pos


def run_dfs_on_path(lines, start_pos):
    nbs = get_enterable_neighbours(lines, start_pos)
    # Stores tuples of (cell, distance, previous cell) which should be considered by DFS
    frontier = [((nx,ny), 1, start_pos) for nx, ny, move in nbs]
    # For each cell in the loop, store its shortest distance to S
    dist_map = { start_pos: 0 }

    moves = [move for nx,ny,move in nbs]
    # print(moves)

    start_char = None
    if 'RIGHT' in moves:
        if 'DOWN' in moves:
            start_char = RD
        elif 'UP' in moves:
            start_char = RU
        else:
            start_char = HPIPE
    elif 'LEFT' in moves:
        if 'DOWN' in moves:
            start_char = LD
        elif 'UP' in moves:
            start_char = LU
    else:
        start_char = VPIPE

    start_line = lines[start_pos[0]]
    print("SWITCHED S ->", start_char)
    lines[start_pos[0]] = list(str(start_line[:start_pos[1]]) + start_char + str(start_line[start_pos[1]+1:]))

    while len(frontier) > 0:
        # Remove the first element in the queue
        (curr, d, prev) = frontier[0]
        frontier = frontier[1:]

        # New cell (not seen in loop)
        if curr not in dist_map.keys():
            dist_map[curr] = d
        else:
            break

        curr_sym = lines[curr[0]][curr[1]]
        for (x, y, move) in get_next_cell_on_path(curr_sym, curr, prev):
            frontier.append(((x,y), d+1, curr))

    return dist_map


def part_one(fileaddr):
    lines = read_file(fileaddr)
    start_pos = find_start_pos(lines)
    print("Start:", start_pos)
    dist_map = run_dfs_on_path(lines, start_pos)
    return max(dist_map.values())



    
    
def in_bounds(pt, lines):
    return pt[0] >= 0 and pt[0] < len(lines[0]) and pt[1] >= 0 and pt[1] < len(lines)


def deduce_dir(path, lines):

    pt1 = path[0]
    pt2 = path[1]
    sym_1 = lines[pt1[0]][pt1[1]]
    sym_2 = lines[pt2[0]][pt2[1]]
    i = 1

    while sym_1 == sym_2:
        pt1 = pt2
        i += 1
        pt2 = path[i]
        sym_1 = lines[pt1[0]][pt1[1]]
        sym_2 = lines[pt2[0]][pt2[1]]

    print(f"P1: {sym_1}, P2: {sym_2}")

    # Assert: pt1 != pt2
    if sym_1 == HPIPE:
        if sym_2 == RD or sym_2 == RU:
            return LEFT
        else:
            return RIGHT
    elif sym_1 == VPIPE:
        if sym_2 == LD or sym_2 == RD:
            return UP
        else:
            return DOWN
    elif sym_1 == RD:
        if sym_2 == HPIPE or sym_2 == LU or sym_2 == LD:
            return RIGHT
        else:
            return DOWN
    elif sym_1 == LU:
        if sym_2 == VPIPE or sym_2 == LD or sym_2 == RD:
            return RIGHT
        else:
            return DOWN
    elif sym_1 == LD:
        if sym_2 == HPIPE or sym_2 == RU or sym_2 == RD:
            return LEFT
        else:
            return DOWN
    elif sym_1 == RU:
        if sym_2 == VPIPE or sym_2 == LD or sym_2 == RD:
            return UP
        else:
            return RIGHT 

    
        




def is_clockwise(path, lines, start_dir):
    r_turns = 0
    dir = start_dir

    for pos in path:
        cell = lines[pos[0]][pos[1]]
        if cell == RD:
            if dir == UP:
                r_turns += 1
                dir = RIGHT
            else:
                r_turns -= 1
                dir = DOWN
        elif cell == RU:
            if dir == DOWN:
                r_turns -= 1
                dir = RIGHT
            else:
                r_turns += 1
                dir = UP
        elif cell == LD:
            if dir == RIGHT:
                r_turns += 1
                dir = DOWN
            else:
                r_turns -= 1
                dir = LEFT
        elif cell == LU:
            if dir == RIGHT:
                r_turns -= 1
                dir = UP
            else:
                r_turns += 1
                dir = LEFT

    print(r_turns)
    return r_turns > 0


def find_inside_outside(lines, path):
    dir = deduce_dir(path, lines)
    print("Start:",dir)
    
    offset_path = path[1:]
    offset_path.append(path[0])

    clockwise = is_clockwise(offset_path, lines, dir)
    print("Clockwise:", clockwise)

    all_inside = set()
    all_outside = set()

    for pos in offset_path:
        cell = lines[pos[0]][pos[1]]

        W = (pos[0]-1, pos[1])
        E = (pos[0]+1, pos[1])
        N = (pos[0]  , pos[1]-1)
        S = (pos[0]  , pos[1]+1)
        NW = (pos[0]-1, pos[1]-1)
        NE = (pos[0]+1, pos[1]-1)
        SW = (pos[0]-1, pos[1]+1)
        SE = (pos[0]+1, pos[1]+1)

        inside = set()
        outside = set()

        print(cell)

        if cell == '|':
            if (dir == UP and clockwise) or (dir == DOWN and not clockwise):
                inside.add(E)
                outside.add(W)
            else:
                inside.add(W)
                outside.add(E)
        elif cell == '-':
            if (dir == RIGHT and clockwise) or (dir == LEFT and not clockwise):
                inside.add(S)
                outside.add(N)
            else:
                inside.add(N)
                outside.add(S)
            
        elif cell == 'F':
            if dir == LEFT:
                # Assume clockwise
                inside = inside.union(set([W,NW,N]))
                dir = DOWN
                if not clockwise:
                    inside, outside = outside, inside
            else: # UP
                outside = outside.union(set([W,NW,N]))
                dir = RIGHT
                if not clockwise:
                    inside, outside = outside, inside
        elif cell == 'J':
            if dir == RIGHT:
                inside = inside.union(set([S,SE,E]))
                dir = UP
                if not clockwise:
                    inside, outside = outside, inside
            else: # DOWN
                outside = outside.union(set([S,SE,E]))
                dir = LEFT
                if not clockwise:
                    inside,outside = outside,inside
        elif cell == '7':
            if dir == RIGHT:
                outside = set([N,NE,E])
                dir = DOWN
                if not clockwise:
                    inside, outside = outside, inside
            else: # UP
                inside = set([N,NE,E])
                dir = LEFT
                if not clockwise:
                    inside,outside = outside,inside
        elif cell == 'L':
            if dir == DOWN:
                inside = set([W,SW,S])
                dir = RIGHT
                if not clockwise:
                    inside, outside = outside, inside
            else: # LEFT
                outside = set([W,SW,S])
                dir = UP
                if not clockwise:
                    inside,outside = outside,inside

        all_inside = all_inside.union([a for a in inside if in_bounds(a, lines) and a not in path])
        all_outside = all_outside.union([b for b in outside if in_bounds(b, lines) and b not in path])

        print("In:", all_inside)
        print("Out:", all_outside)

    print("In:", all_inside)
    print("Out:", all_outside)

    return all_inside, all_outside




def part_two(fileaddr):
    lines = read_file(fileaddr)
    start_pos = find_start_pos(lines)
    print("Start:", start_pos)
    dist_map = run_dfs_on_path(lines, start_pos)
    # for line in lines:
    #     print("".join(line))

    unordered_path = list(dist_map.keys())
    # print(path_alt)

    path = [unordered_path[0]] 
    path.extend(unordered_path[1::2])
    path.extend(reversed(unordered_path[2::2]))
    print(path)

    inside, outside = find_inside_outside(lines, path)

    new_grid = [['.' for i in range(0,len(line))] for line in lines]
    for pt in inside:
        new_grid[pt[0]][pt[1]] = 'I'
    for pt in outside:
        new_grid[pt[0]][pt[1]] = 'O'

    print("Result:")
    for line in new_grid:
        print("".join(line))

    return len(inside)









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
    

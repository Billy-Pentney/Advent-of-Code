import sys, os
import re
from queue import PriorityQueue
from math import sqrt


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        for line in file.readlines():
            line_numbers = [int(num) for num in line.replace("\n", "")]
            lines.append(line_numbers)
    return lines

def print_grid(grid, as_string=False):
    for row in grid:
        if as_string:
            print("".join([str(x) for x in row]))
        else:
            print(row)


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


def get_enterable_neighbours(lines, curr, last_dir, last_dir_count):
    nbs = []
    (row, col) = curr

    # Move North from current
    if row > 0 and (last_dir_count < 3 or last_dir != NORTH):
        nbs.append(((row-1, col), NORTH))
    # Move East from current
    if col < len(lines[row])-1 and (last_dir_count < 3 or last_dir != EAST):
        nbs.append(((row, col+1), EAST))
    # Move South from current
    if row < len(lines)-1 and (last_dir_count < 3 or last_dir != SOUTH):
        nbs.append(((row+1, col), SOUTH))
    # Move West from current
    if col > 0 and (last_dir_count < 3 or last_dir != WEST):
        nbs.append(((row, col-1), WEST))
    
    return nbs




class State:
    def __init__(self, new_cell, new_dir, last_state):
        if last_state is not None:
            self.path = last_state.path.copy()
        else:
            self.path = []
        self.path.append(new_cell)

        # Join with previous move
        if last_state is not None and last_state.last_move == new_dir:
            self.last_move = new_dir
            self.last_move_count = last_state.last_move_count + 1
        # Discard previous move, we've changed direction
        elif new_dir is not None:
            self.last_move = new_dir
            self.last_move_count = 1
        else:
            self.last_move = None
            self.last_move_count = 0

    def endpoint(self):
        if self.path is None:
            return None
        return self.path[-1]

    def gen_move_to(self, next_cell, dir):
        return State(next_cell, dir, self)

    def __repr__(self):
        return f"(Path: ..{self.path[-1]}, last_move: {self.last_move})"


# Calculate square of L2-Norm (square of Pythagorean Distance)
def calc_direct_distance(pos1, pos2):
    return sqrt((pos1[0] - pos2[0])**2 + (pos1[1]-pos2[1])**2)


def last_move_to_symbol(dir):
    if dir == EAST:
        return '-'
    elif dir == NORTH:
        return '|'
    elif dir == SOUTH:
        return '|'
    elif dir == WEST:
        return '-'
    else:
        return 'X'

## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)
    # print(lines)

    # Coordinates in y-x form
    source = (0,0)
    dest = (len(lines)-1, len(lines[0])-1)

    # min_cost[r][c][d] is the minimum heat-loss in any path from the start
    # to cell at row r, column c, entering via direction d (0-3)
    min_cost = [[[0,0,0,0] for x in line] for line in lines]
    moves_used = [[[0,0,0,0] for x in line] for line in lines]

    frontier = PriorityQueue()
    frontier.put((calc_direct_distance(source, dest), 0, State(source, None, None)))

    seen = set()
    iters = 0

    prev_state = {}

    while not frontier.empty(): # and dest not in seen:
        (_, _, curr_state) = frontier.get()
        curr = curr_state.endpoint()

        if curr_state.last_move is not None:
            curr_cost = min_cost[curr[0]][curr[1]][curr_state.last_move]
            curr_moves = moves_used[curr[0]][curr[1]][curr_state.last_move]
        else:
            curr_cost = 0
            curr_moves = 10

        seen.add(curr)

        for nb, dir in get_enterable_neighbours(lines, curr, curr_state.last_move, curr_state.last_move_count):
            # Compare the heat-loss required to reach nb, entering via direction dir
            old_cost = min_cost[nb[0]][nb[1]][dir]
            new_cost = curr_cost + lines[nb[0]][nb[1]]

            new_state = curr_state.gen_move_to(nb, dir)
            priority = new_cost + calc_direct_distance(nb, dest) + curr_state.last_move_count

            # Compare the number of consecutive moves (in dir) required to reach nb
            old_moves = moves_used[nb[0]][nb[1]][dir]
            new_moves = curr_state.last_move_count
            
            print(f"Considering {new_state} with priority {priority}")

            if nb not in seen or old_cost == 0 or new_cost < old_cost or new_moves < old_moves:
                iters += 1
                prev_state[(nb,dir)] = curr_state
                min_cost[nb[0]][nb[1]][dir] = new_cost
                moves_used[nb[0]][nb[1]][dir] = new_moves
                frontier.put((priority, iters, new_state))
                seen.add(nb)

    print_grid(min_cost)

    cost_to_goal = min_cost[dest[0]][dest[1]]
    dir = 0
    for d in [NORTH, EAST, SOUTH, WEST]:
        if cost_to_goal[dir] == 0 or (cost_to_goal[d] > 0 and cost_to_goal[d] < cost_to_goal[dir]):
            dir = d

    # Generate path from the visited cells
    # path = []
    # curr_state = State(dest, None, None)
    # while curr_state.cell != source:
    #     curr = curr_state.cell
    #     path.append(curr)
    #     lines[curr[0]][curr[1]] = last_move_to_symbol(curr_state.last_move)
    #     curr_state = prev_state[curr]
    path = prev_state[(dest,dir)].path
    for cell in path:
        lines[cell[0]][cell[1]] = 'X'

    print_grid(lines, as_string=True)
    return cost_to_goal[dir]


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
    

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
DIRS = [NORTH, EAST, SOUTH, WEST]


def get_enterable_neighbours(lines, curr, last_dir, last_dir_count):
    nbs = []
    (row, col) = curr

    # Move North from current
    if row > 0 and (last_dir_count < 3 or last_dir != NORTH) and last_dir != SOUTH:
        nbs.append(((row-1, col), NORTH))
    # Move East from current
    if col < len(lines[row])-1 and (last_dir_count < 3 or last_dir != EAST) and last_dir != WEST:
        nbs.append(((row, col+1), EAST))
    # Move South from current
    if row < len(lines)-1 and (last_dir_count < 3 or last_dir != SOUTH) and last_dir != NORTH:
        nbs.append(((row+1, col), SOUTH))
    # Move West from current
    if col > 0 and (last_dir_count < 3 or last_dir != WEST) and last_dir != EAST:
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
        return f"(Path: ..{self.path[-2:]}, last_move: {last_move_to_symbol(self.last_move)})"


# Calculate square of L2-Norm (square of Pythagorean Distance)
def calc_direct_distance(pos1, pos2):
    return sqrt((pos1[0] - pos2[0])**2 + (pos1[1]-pos2[1])**2)


def last_move_to_symbol(dir):
    if dir == EAST:
        return '>'
    elif dir == NORTH:
        return '^'
    elif dir == SOUTH:
        return 'v'
    elif dir == WEST:
        return '<'
    else:
        return 'X'


INF = 100000000


## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)
    # print(lines)

    # Coordinates in y-x form
    source = (0,0)
    dest = (len(lines)-1, len(lines[0])-1)

    # min_cost[r][c][d] is the minimum heat-loss in any path from the start
    # to cell at row r, column c, entering via direction d (0-3)
    min_cost = [[[[INF,INF,INF,INF] for dir in DIRS] for x in line] for line in lines]
    moves_used = [[[INF,INF,INF,INF] for x in line] for line in lines]

    frontier = PriorityQueue()
    frontier.put((calc_direct_distance(source, dest), 0, State(source, None, None)))
    min_cost[source[0]][source[1]] = [[0,0,0] for dir in DIRS]

    seen = set()
    iters = 0

    prev_state = {}

    while not frontier.empty(): # and dest not in seen:
        (_, _, curr_state) = frontier.get()
        curr = curr_state.endpoint()

        # Compare the number of consecutive moves (in dir) required to reach nb
        new_moves = curr_state.last_move_count


        if curr_state.last_move is not None:
            curr_cost = min([
                # by the same direction with up to the same number of moves
                min(min_cost[curr[0]][curr[1]][curr_state.last_move][0:curr_state.last_move_count]),
                # by a perpendicular direction with any number of moves
                min(min_cost[curr[0]][curr[1]][(curr_state.last_move+1)%4]),
                min(min_cost[curr[0]][curr[1]][(curr_state.last_move+3)%4])
                # don't check the opposite direction [ (dir+2)%4 ], since the box can't move back on itself
            ])
        else:
            curr_cost = 0

        print(curr_cost)

        seen.add(curr)

        for nb, dir in get_enterable_neighbours(lines, curr, curr_state.last_move, curr_state.last_move_count):
            new_state = curr_state.gen_move_to(nb, dir)

            # Find the previous lowest-cost to reach this neighbour
            old_cost = min([
                # by the same direction with no more moves
                min(min_cost[nb[0]][nb[1]][dir][0:new_state.last_move_count]),
                # by a perpendicular direction with any number of moves
                min(min_cost[nb[0]][nb[1]][(dir+1)%4]),
                min(min_cost[nb[0]][nb[1]][(dir+3)%4])
                # don't check the opposite direction [ (dir+2)%4 ], since the box can't move back on itself
            ])

            new_cost = curr_cost + lines[nb[0]][nb[1]]

            priority = new_cost
            
            print(f"Considering {new_state} with cost: {new_cost} vs old_cost: {old_cost}")

            if nb not in seen or old_cost == INF or new_cost < old_cost:
                iters += 1
                if nb in prev_state.keys():
                    prev_state[nb][dir] = curr_state
                else:
                    prev_state[nb] = { dir: curr_state }

                # min_cost[c][d][m] is the minimum heat-loss required to enter cell c, with at most m
                # consecutive movements in direction d immediately before entering
                for m in range(new_moves, 3):
                    min_cost[nb[0]][nb[1]][dir][m] = min(new_cost, min_cost[nb[0]][nb[1]][dir][m])
                
                for m in range(0, 3):
                    min_cost[nb[0]][nb[1]][(dir+1)%4][m] = min(new_cost, min_cost[nb[0]][nb[1]][(dir+1)%4][m])
                    min_cost[nb[0]][nb[1]][(dir+3)%4][m] = min(new_cost, min_cost[nb[0]][nb[1]][(dir+3)%4][m])

                frontier.put((priority, iters, new_state))
                seen.add(nb)

    # print_grid(min_cost)

    cost_to_goal = min_cost[dest[0]][dest[1]]
    print(cost_to_goal)
    dir = -1
    min_cost = INF
    for d in DIRS:
        goal_cost = min(cost_to_goal[d])
        if goal_cost < min_cost and d in prev_state[dest]:
            dir = d
            min_cost = goal_cost

    path = prev_state[dest][dir].path
    for cell in path:
        lines[cell[0]][cell[1]] = '-'

    print_grid(lines, as_string=True)
    return min(cost_to_goal[dir])












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
    

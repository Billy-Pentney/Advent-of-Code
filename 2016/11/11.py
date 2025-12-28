
import numpy as np
# import regex as re
from collections import defaultdict, namedtuple
from queue import PriorityQueue

State = namedtuple('State', ['microchips', 'generators', 'elevator'])
Move = namedtuple('Move', ['microchips', 'generators', 'direction'])


def is_move_reverse(move: Move, other: Move):
    """
    Returns true if these moves cancel each other out (one performs the opposite move to the other).
    """
    return move.generators == other.generators and move.microchips == other.microchips and move.direction == -other.direction


def copy(state: State):
    """
    Deep-copies the content of this game state to a new state.
    """
    microchips_copy = defaultdict(list)
    generators_copy = defaultdict(list)
    for floor in state.microchips.keys():
        microchips_copy[floor].extend(state.microchips[floor])
    for floor in state.generators.keys():
        generators_copy[floor].extend(state.generators[floor])
    return State(microchips_copy, generators_copy, state.elevator)


class IllegalMoveException(Exception):
    pass

## ===============================================

def load(fname):
    with open(fname, "r") as file:
        grid = [
            [cell for cell in row.strip("\n").split(" ") if len(cell) > 0]
            for row in file.readlines()
        ]

    return grid

## ## Rules ##
## If a chip is left in the same area as another Generator (and it's not connected to its own Generator) then the chip will be fried. 

def show(grid):
    """ Displays a game grid """
    n_rows = len(grid)
    for y in range(len(grid)):
        print(f"F{n_rows-y}:", " ".join(grid[y]))



def make_state(grid) -> State:
    """
    Converts a game grid to a state, describing the locations of the chips, generators and elevator.
    """
    microchips = defaultdict(list)
    generators = defaultdict(list)
    elevator = 1

    n_rows = len(grid)
    for y, row in enumerate(grid):
        for _, cell in enumerate(row):
            if cell == '.':
                continue
            element = cell[:-1]
            floor = n_rows - y
            if cell == 'E':
                elevator = floor
            elif cell[-1] == 'G':
                ## Generator
                generators[floor].append(element)
            else:
                ## Microchip
                microchips[floor].append(element)

    return State(microchips, generators, elevator)



def transport(state: State, move: Move, verbose=True) -> State:
    """
    Moves the specified microchips and generators up/down a certain number of floors
    """
    state = copy(state)
    floor_start = state.elevator
    microchips = state.microchips
    generators = state.generators

    chosen_microchips = move.microchips
    chosen_generators = move.generators
    floor_change = move.direction

    if len(chosen_microchips) + len(chosen_generators) == 0:
        raise IllegalMoveException("Cannot move elevator with 0 Microchips and 0 Generators!") 

    # non_conn_microchips = set(chosen_microchips).difference(chosen_generators)
    # if non_conn_microchips and len(chosen_generators) > 0:
    #     raise IllegalMoveException(f"Cannot move microchips {non_conn_microchips} without their generators! (attempted to move {chosen_generators})")

    ## Constrain the floor after moving to be between 1-4
    new_floor = min(4, max(floor_start+floor_change, 1))
    
    if verbose:
        print(f"Move microchips {chosen_microchips} and generators {chosen_generators} to floor {new_floor}")

    for mc in chosen_microchips:
        if mc not in microchips[floor_start]:
            raise Exception(f"Microchip {mc} is not on floor {floor_start}!")
        microchips[floor_start].remove(mc)
        microchips[new_floor].append(mc)

    for gen in chosen_generators:
        if gen not in generators[floor_start]:
            raise Exception(f"Generator {gen} is not on floor {floor_start}!")
        generators[floor_start].remove(gen)
        generators[new_floor].append(gen)

    return State(microchips, generators, new_floor)


def show_state(state: State):
    """ Displays a state, by constructing a grid and showing it. """
    grid = defaultdict(list)
    grid[state.elevator].append('E')
    for floor, mcs in state.microchips.items():
        grid[floor].extend([mc + 'M' for mc in mcs])
    for floor, gens in state.generators.items():
        grid[floor].extend([gen + 'G' for gen in gens])
    max_floors = 4
    final_grid = [[] for i in range(max_floors)]
    for floor in sorted(grid.keys()):
        final_grid[max_floors-floor] = grid[floor]
    show(final_grid)


def is_valid(state: State):
    """ Checks if a state doesn't violate any rules of the game. """
    nonempty_floors = set(state.microchips.keys()).union(state.generators.keys())
    for floor in nonempty_floors:
        micros = state.microchips[floor]
        gens = state.generators[floor]
        without_gen = set(micros).difference(gens)
        ## If there's a microchip that doesn't have its generator and there's at least one generator
        ## then that microchip gets fried
        if len(gens) > 0 and len(without_gen) > 0:
            return False
        
    return True

def check_complete(state: State, top_floor: int = 4):
    """ Checks if a state has all its microchips and generators on the top floor """
    if not is_valid(state):
        return False

    total_microchips = sum([len(state.microchips[floor]) for floor in state.microchips.keys()])
    total_generators = sum([len(state.generators[floor]) for floor in state.generators.keys()])
    all_microchips_at_top = len(state.microchips[top_floor]) == total_microchips
    all_generators_at_top = len(state.generators[top_floor]) == total_generators
    return all_generators_at_top and all_microchips_at_top 


def serialise(state: State):
    st = str(state.elevator)
    for floor in range(1,4):
        st += "/"
        items = [f"{g}G" for g in sorted(state.generators[floor])] + [f"{mc}M" for mc in sorted(state.microchips[floor])]
        st += " ".join(items)
    return st



def find_all_moves(state: State):
    """
    Returns a list of all unique moves from this game state to a new game state.
    """
    curr_floor = state.elevator
    possible_moves = []

    microchips = state.microchips[curr_floor]
    generators = state.generators[curr_floor]

    for change in [1,-1]:
        floor = curr_floor + change
        if floor < 1 or floor > 4:
            continue

        new_floor_microchips = state.microchips[floor]
        new_floor_generators = state.generators[floor]

        movable_single_chips = []

        for mc1 in microchips:
            ## First check if we can move this microchip on its own

            ## If the generator is in the above floor, or the above floor doesn't have any 
            ## generators then we can move this chip up one floor.
            if len(new_floor_generators) == 0 or mc1 in new_floor_generators:
                movable_single_chips.append(mc1)
                ## Move a single microchip
                possible_moves.append(Move([mc1],[],change))

            ## Next check if we can move it WITH its generator
            if mc1 in generators:
                unmatched_microchips_on_next = set(new_floor_microchips).difference(new_floor_generators)
                ## We can only move it if moving the generator wouldn't break any chips on the destination floor
                if len(unmatched_microchips_on_next) == 0:
                    # print(f"Can move {mc}-M and {mc}-G to F{floor}")
                    possible_moves.append(Move([mc1],[mc1],change))


        ## Check if we can move a PAIR of microchips (note: these must *BOTH* be movable independently)
        for i, mc1 in enumerate(movable_single_chips):
            for mc2 in movable_single_chips[i+1:]:
                ## Move both microchips in the same step
                possible_moves.append(Move([mc1,mc2],[], change))


        for i,gen in enumerate(generators):
            ## First check if there are any microchips on the destination floor that don't have
            ## their corresponding generator. (Moving this generator would cause them to fry!)
            unmatched_microchips_on_next = set(new_floor_microchips).difference(new_floor_generators)
            unmatched_microchips_on_next = unmatched_microchips_on_next.difference([gen])

            if len(unmatched_microchips_on_next) == 0:
                ## If this is the only generator on this floor OR it's not protecting the microchip here,
                ## then we can move it.
                if len(generators) == 1 or gen not in microchips:
                    move = Move([], [gen], change)
                    # print(f"Can move {gen}-G to F{floor}")
                    possible_moves.append(move)
            
            ## Check if we can move two generators together
            for gen2 in generators[i+1:]:
                unmatched_microchips_2 = unmatched_microchips_on_next.difference([gen2])
                if len(unmatched_microchips_2) == 0:
                    move = Move([], [gen,gen2], change)
                    # print(f"Can move {gen}-G, {gen2}-G to F{floor}")
                    possible_moves.append(move)

    return possible_moves

from time import sleep
    

def calculate_heuristic(state: State, target_floor=4):
    steps_req = 0
    for floor in set(state.generators.keys()).union(state.microchips.keys()):
        n_gens = len(state.generators[floor])
        n_mcs = len(state.microchips[floor])
        n_items = n_gens + n_mcs
        steps_req += 2 * n_items * abs(target_floor - floor)
        # if floor == target_floor:
        #     steps_req -= n_items
        # else:
    return steps_req


def solve_with_astar(init_state: State) -> int:

    ## Stores triples (h, S, M) where:
    ##  * h is the heuristic distance to the solved state
    ##  * S is (the index of) the current state
    ##  * M is the list of moves required to reach state S
    frontier = PriorityQueue()

    ## Distance from start (i.e. num moves required)
    f = 0
    ## Estimated distance to goal
    g = calculate_heuristic(init_state)
    ## Combined heuristic
    h = f+g

    ## Use a state list to handle ties with PriorityQueue keys
    init_serial = serialise(init_state)
    state_by_serial = { init_serial: init_state }
    min_moves_to_reach = { init_serial: 0 }

    frontier.put((h, init_serial, []))

    ## Count the number of states evaluated (for diagnostics)
    n_checked = 0

    ## Store the min cost of any solution which reaches the goal
    best_known_solution = None

    while not frontier.empty():
        h, curr_serial_code, moves_list = frontier.get()
        curr = state_by_serial[curr_serial_code]
        f = len(moves_list)

        if best_known_solution and f > best_known_solution:
            continue

        ## Skip if we've seen a better list of moves to reach this cell
        if f > min_moves_to_reach[curr_serial_code]:
            continue

        if n_checked > 0 and n_checked % 5000 == 0:
            print(f"Checked {n_checked}, progress f={f} / h={h}")

        n_checked += 1
        # print(f"Current State (total moves={len(moves_list)}, f={f}, g={g}):")
        # show_state(curr)
        # print()

        if check_complete(curr):
            ## The state meets the required conditions (and is the optimal path)
            print(f"Checked: {n_checked}")
            best_known_solution = f
            return moves_list

        # sleep(1)

        ## Get all moves we could make from this state
        candidate_moves = find_all_moves(curr)
        
        for move in candidate_moves:
            new_state = transport(curr, move, verbose=False)
            if not is_valid(new_state):
                continue

            f_ = len(moves_list) + 1

            new_serial_code = serialise(new_state)
            ## Check if we've seen this state before
            if new_serial_code not in state_by_serial:
                state_by_serial[new_serial_code] = new_state

            if check_complete(new_state) and (best_known_solution is None or f_ < best_known_solution):
                best_known_solution = f_
                print(f" > Found new best solution with {f_} moves!")

            if new_serial_code not in min_moves_to_reach or f_ < min_moves_to_reach[new_serial_code]:
                min_moves_to_reach[new_serial_code] = f_
                new_moves_list = moves_list + [move]
                g_ = calculate_heuristic(new_state)
                h_ = f_ + g_
                frontier.put((h_, new_serial_code, new_moves_list))
        
    ## All possible moves exhausted
    return None




from typing import List


def play_moves(state: State, moves: List[Move], verbose=True):
    state2 = copy(state)
    valid = True
    for i,move in enumerate(moves):
        state2 = transport(state2, move, verbose=verbose)
        valid = valid & is_valid(state2)
        if verbose:
            show_state(state2)
        if not valid:
            print(f"Not valid after move {i+1}/{len(moves)}!")
            return False
    return check_complete(state2)



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    grid = load(fname)
    new_state = make_state(grid)
    print("-- Initial State --")
    show_state(new_state)
    print("-------------------")

    ## Example solution
    # moves = [
        # (['H'], [], 1),
        # (['H'], ['H'], 1),
        # (['H'], [], -1),
        # (['H'], [], -1),
        # (['H', 'L'], [], 3),
        # (['H'], [], -1),
        # ([], ['H', 'L'], 1),
        # (['L'], [], -1),
        # (['H','L'], [], 1)
    # ]

    ## Display the result of following a list of moves
    # moves = [Move(it[0], it[1], it[2]) for it in moves]
    # is_complete = play_moves(new_state, moves)
    # print(is_complete)

    move_list = solve_with_astar(new_state)
    total_moves = len(move_list)

    if total_moves is not None:
        state = copy(new_state)
        print("Replay solution:")
        for i,move in enumerate(move_list):
            assert isinstance(move, Move)
            ## Display the solution as tuples, for use with the move display function
            print(f"    ({move.microchips}, {move.generators}, {move.direction})")
            state = transport(state, move, verbose=False)
            if not is_valid(state):
                print("Invalid state!")

        is_complete = check_complete(state)
        print("Complete?", is_complete)
        print("Total moves:", total_moves)

    else:
        print("No solution found!")

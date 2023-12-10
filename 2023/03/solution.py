import os, sys
from Position import Position, Symbol, Number


def is_adjacent_to_symbol(num, sym_row):
    for sym in sym_row:
        # Symbol is after the number (and all subsequent symbols in the row are too)
        if num.end_col + 1 < sym.col:
            break

        # Find the horizontal distance from the number to the symbol
        start_dist = abs(num.start_col - sym.col)
        end_dist = abs(num.end_col - sym.col)

        # Less than 1 unit from either end of the word
        if min(start_dist, end_dist) <= 1:
            # print(f"{num} due to {sym}")
            return True
        
    return False



def find_adjacents(target: Position, pos_row: [Position], count = 1):
    adj = []

    for other in pos_row:
        # Symbol is after the number (and all subsequent symbols in the row are too)
        if other.start_col - 1 > target.end_col:
            break

        # Find the horizontal distance from the number to the symbol
        start_dist = abs(other.start_col - target.start_col)
        end_dist = abs(other.end_col - target.end_col)

        # Less than 1 unit from either end of the word
        if min(start_dist, end_dist) <= 1:
            # print(f"{target} adj to {other}")
            adj.append(other)
            if count > -1 and len(adj) >= count:
                break
        
    return adj



def read_schematic(fileaddr):
     # Read the schematic
    file = open(fileaddr, "r")
    lines = file.readlines()
    file.close()

    all_symbols = []
    all_numbers = []

    # Identify positions of all numbers and symbols
    for row, line in enumerate(lines):
        start_col = None

        for col, char in enumerate(line):
            if char.isdigit():
                # A number starts on this cell
                if start_col is None:
                    start_col = col
            else:
                # A number ended on the previous cell
                if not start_col is None:
                    num = Number(row, start_col, col-1, line[start_col:col])
                    all_numbers.append(num)
                    start_col = None

                # New Symbol
                if char != '.' and char != '\n':
                    all_symbols.append(Symbol(row, col, char))
    
    return all_numbers, all_symbols, len(lines)


def group_by_row(all_pos, num_lines):
    by_row = [[] for _ in range(num_lines)]
    for pos in all_pos:
        r = pos.row
        by_row[r].append(pos)
    return by_row


def sum_of_part_numbers(fileaddr):
    valid_nums = []
    all_numbers, all_symbols, num_lines = read_schematic(fileaddr)
    all_symbols = group_by_row(all_symbols, num_lines)

    for num in all_numbers:
        # Consider the three rows which have a vertical distance <= 1 from the symbol 
        row_above = max(0, num.row-1)
        row_below = min(num.row+1, num_lines-1)

        for row_num in range(row_above, row_below+1):
            if len(find_adjacents(num, all_symbols[row_num])) > 0:
                valid_nums.append(int(num.val))
                break
            
    return sum(valid_nums)


def sum_of_gear_ratios(fileaddr):
    all_numbers, all_symbols, num_lines = read_schematic(fileaddr)
    all_numbers = group_by_row(all_numbers, num_lines)

    gear_ratios = []

    for sym in all_symbols:
        if sym.val != '*':
            continue

        # Consider the three rows which have a vertical distance <= 1 from the symbol 
        row_above = max(0, sym.row-1)
        row_below = min(sym.row+1, num_lines-1)

        num_adj = []
        for row_num in range(row_above, row_below+1):
            num_adj.extend(find_adjacents(sym, all_numbers[row_num], -1))
            if len(num_adj) > 2:
                break
        
        if len(num_adj) == 2:
            gear_ratios.append(int(num_adj[0].val) * int(num_adj[1].val))

    return sum(gear_ratios)            




if __name__ == '__main__':
    args = sys.argv[1:]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if (part == '1'):
            result = sum_of_part_numbers(fileaddr)
        else:
            result = sum_of_gear_ratios(fileaddr)

        print("Result:", result)
    else:
        print(f"Could not find file at location {fileaddr}")
    


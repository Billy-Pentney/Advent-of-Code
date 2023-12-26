import sys, os
import re

RIGHT = "R"
UP = "U"
DOWN = "D"
LEFT = "L"

def dir_vector(dir):
    if dir == DOWN:
        return [0,1]
    if dir == UP:
        return [0,-1]
    if dir == LEFT:
        return [-1,0]
    if dir == RIGHT:
        return [1,0]



class Move:
    def __init__(self, line):
        splits = line.replace("\n", "").split(" ")
        self.dir = splits[0]
        self.count = int(splits[1])
        self.color_parens = splits[2]


class Line:
    def __init__(self, start, dir, length):
        self.start = start
        self.dir = dir

        dv = dir_vector(dir)
        self.length = length
        self.length_vect = [dv[0]*length, dv[1]*length]
        self.end = [self.start[0]+self.length_vect[0], self.start[1]+self.length_vect[1]]

    def __repr__(self):
        return f"({self.start}: {self.end}, by {self.dir}, length: {self.length})"
    
    def extend(self, vector):
        self.length_vect[0] += vector[0]
        self.length_vect[1] += vector[1]
        self.end[0] += vector[0]
        self.end[1] += vector[1]
        self.length = abs(self.length_vect[0]) + abs(self.length_vect[1])

    def reduce(self, vector):
        opp_vector = [-1*vector[0], -1*vector[1]]
        self.extend(opp_vector)



def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    return [Move(line) for line in lines]


def trace_path(moves):
    cell = [0,0]
    pivots = []
    history = [cell]
    lines = []

    min_x, max_x = 0,0
    min_y, max_y = 0,0

    curr_dir = None

    for move in moves:
        dir = move.dir
        count = move.count

        if dir == RIGHT:
            vect = [1,0]
        elif dir == UP:
            vect = [0,-1]
        elif dir == LEFT:
            vect = [-1,0]
        elif dir == DOWN:
            vect = [0,1]

        # Rotate at this cell, from curr_dir to dir
        pivots.append((cell, curr_dir, dir))
        curr_dir = dir

        for i in range(1,count+1):
            new_cell = [cell[0]+i*vect[0], cell[1]+i*vect[1]]
            history.append(new_cell)
        
        lines.append(Line(cell, dir, count))
        cell = new_cell
        
        min_x = min(cell[0], min_x)
        max_x = max(cell[0], max_x)
        min_y = min(cell[1], min_y)
        max_y = max(cell[1], max_y)

    print("X:",min_x, max_x)
    print("Y:",min_y, max_y)

    width = max_x+1 - min_x
    height = max_y+1 - min_y
    
    return width, height, history, lines

def print_grid(grid):
    for row in grid:
        print("".join(row))


def opposite_dir(dir):
    if dir == UP:
        return DOWN
    if dir == DOWN:
        return UP
    if dir == RIGHT:
        return LEFT
    if dir == LEFT:
        return RIGHT
    return None

## Solve Part One
def part_one(fileaddr):
    line_splits = read_file(fileaddr)
    width, height, history, lines = trace_path(line_splits)
 
    area = 0
    stack = []

    grid = [['.' for col in range(width)] for row in range(height)]

    for cell in history:
        grid[cell[1]][cell[0]] = '#'

    # Strategy: evaluate the area by "cordoning" off rectangles and removing them from the grid
    for line in lines:
        print("\nStack before:",stack)
        print("LINE:",line)

        if len(stack) > 1 and stack[-2].dir == opposite_dir(line.dir):
            prev: Line = stack[-1]
            prevprev: Line = stack[-2]

            # The number of cells dug between this line and prevprev
            # i.e. the "height" of the box being drawn
            box_span = prev.length - 1
            # The breadth of the box
            box_width = 0

            print("Box found!")

            if line.dir == LEFT:
                box_width = line.start[0] - max(prevprev.start[0], line.end[0])
                """
                        ->                           ->
                      #######         or             ### |
                            # |                        # v
                         #### v                   ######
                          <-                         <-
                """  

            elif line.dir == RIGHT:
                box_width = min(prevprev.start[0], line.end[0]) - line.start[0]
                """
                          ->
                      #######         or          ###
                    ^ #                           #
                    | ####                        ######
                        <-
                """    

            if line.dir == DOWN:
                box_width = min(line.end[1], prevprev.start[1]) - line.end[1]
                """
                         -->
                        #### |        or      ####
                      ^ #  # v                #  #
                      | #                     #
                """
            if line.dir == UP:
                box_width = line.start[1] - max(line.end[1], prevprev.start[1])
                """  
                      | #    ^        or         #
                      v #  # |                #  #
                        ####                  ####
                         ->
                """

            print(f"Found a box of size {box_span} * {box_width}")

            box_area = box_span * box_width
            if box_area > 0:
                area += box_area
                print(f"Added {box_area} area to make total {area}")

                # Find the new end position of the penultimate stack entry
                prevprev.length_vect[0] += line.length_vect[0]
                prevprev.length_vect[1] += line.length_vect[1]

                length_after_contraction = prevprev.length - line.length

                # The original line remains
                if length_after_contraction > 0:    
                    prevprev.length -= line.length
                
                    prevprev.end[0] += line.length_vect[0]
                    prevprev.end[1] += line.length_vect[1]

                    # Replace the previous stack entry with a line to the current position
                    prev = Line(prevprev.end, prev.dir, prev.length)
                    stack[-1] = prev
                    print(f"Amended {prevprev} and {prev}")
                else:
                    print("Discarding box")
                    # The original line is empty, so we discard this box 
                    stack.remove(prevprev)
                    stack.remove(prev)

                    # Move the last line to finish at the start of the current line
                    if len(stack) > 0:
                        stack[-1].extend(prev.length_vect)

                    stack.append(Line(stack[-1].end, line.dir, line.length - prevprev.length))

            else:
                stack.append(line)

        elif len(stack) > 0 and stack[-1].dir == line.dir:
            # Merge with the previous line in the same direction
            stack[-1].extend(line.length_vect)

        elif len(stack) > 0 and stack[-1].dir == opposite_dir(line.dir):
            # Reduce from the previous line in the opposite direction
            stack[-1].reduce(line.length_vect)
        
        else:
            stack.append(line)

        print("Stack After:", stack)

    print_grid(grid)
    return area


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
    

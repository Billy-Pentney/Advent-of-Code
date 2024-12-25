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
        return f"\n({self.start}:{self.end} by {self.dir}, len={self.length})"
    
    def extend(self, num):
        dv = dir_vector(self.dir)
        self.length_vect[0] += num*dv[0]
        self.length_vect[1] += num*dv[1]
        self.end[0] += num*dv[0]
        self.end[1] += num*dv[1]
        self.length = abs(self.length_vect[0]) + abs(self.length_vect[1])



def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    return [Move(line) for line in lines]


def trace_path(moves):
    cell = [0,0]
    pivots = []
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

        lines.append(Line(cell, dir, count))
        cell = lines[-1].end
        
        min_x = min(cell[0], min_x)
        max_x = max(cell[0], max_x)
        min_y = min(cell[1], min_y)
        max_y = max(cell[1], max_y)

    # print("X:",min_x, max_x)
    # print("Y:",min_y, max_y)

    width = max_x+1 - min_x
    height = max_y+1 - min_y
    
    return width, height, lines




def mark_on_grid(grid, line, highlight=False):
    start = line.start
    end = line.end
    for x in range(min(start[0], end[0]), max(start[0], end[0])+1):
        for y in range(min(start[1], end[1]), max(start[1], end[1])+1):
            if highlight:
                grid[y][x] = 'X'
            else:
                grid[y][x] = '#'
    return grid


def print_grid(grid):
    print("\n   " + " ".join([str(i) for i in range(0,len(grid[0]))]))
    for i,row in enumerate(grid):
        print(f" {i} " + " ".join(row))


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

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def plot_on_grid(lines, shape):
    width,height = shape
    grid = [['.' for col in range(width)] for row in range(height)]
    for i,line in enumerate(lines):
        mark_on_grid(grid, line, highlight=(i==0))
    print_grid(grid)


def contract(i, stack):
    line = stack[i]
    stack.remove(line)

    prev = stack[i-1]
    prevprev = stack[i-2]

    length_vect = [line.length_vect[0], line.length_vect[1]]
    length = line.length

    # Find the new end position of the penultimate stack entry
    prevprev.length_vect[0] += length_vect[0]
    prevprev.length_vect[1] += length_vect[1]

    length_after_contraction = prevprev.length - length

    # The original line is not completely collapsed
    if length_after_contraction > 0:    
        prevprev.length = length_after_contraction
    
        prevprev.end[0] += length_vect[0]
        prevprev.end[1] += length_vect[1]

        # Replace the previous stack entry with a line to the current position
        prev = Line(prevprev.end, prev.dir, prev.length)
        stack[i-1] = prev
        print(f"Amended {prevprev} and {prev}")
    else:
        print(f"Discarding box from {prevprev.start} to {line.end}")
        # The original line is empty, so we discard this box 
        stack.remove(prevprev)
        stack.remove(prev)

        if i >= 2:
            i -= 2
        elif i == 1:
            i -= 1

        # Move the last line to finish at the start of the current line
        if len(stack) > 0:
            # print(f"Extending {stack[i-1]}")
            if stack[i-1].dir == prev.dir:
                stack[i-1].extend(prev.length)
            else:
                stack[i-1].extend(-1*prev.length)

        if length_after_contraction != 0:
            if len(stack) < 2 or stack[i-1].dir != opposite_dir(line.dir):
                print("Inserting")
                stack.insert(i, Line(stack[i-1].end, line.dir, -length_after_contraction))
            else:
                stack[i-1].extend(-1*line.length)



## Solve Part One
def part_one(fileaddr):
    line_splits = read_file(fileaddr)
    width, height, lines = trace_path(line_splits)
 
    area = 0
    stack = []

    grid = [['.' for col in range(width)] for row in range(height)]


    for line in lines:
        stack.append(line)

    # Strategy: evaluate the area by "cordoning" off rectangles and removing them from the grid
    while len(stack) > 4:
        i = 0

        while i < len(stack) and len(stack) >= 4:
            line = stack[i]

            plot_on_grid(stack, (width,height))

            if len(stack) > 1 and stack[i-2].dir == opposite_dir(line.dir):
                prev: Line = stack[i-1]
                prevprev: Line = stack[i-2]

                # The number of cells dug between this line and prevprev
                # i.e. the "height" of the box being drawn
                box_span = prev.length+1
                # The breadth of the box
                box_width = 0

                # print("Box found!")

                if line.dir == LEFT:
                    box_width = line.start[0] - max(prevprev.start[0], line.end[0])
                    """
                            ->                           ->
                          #######         or             ### |
                                # |                        # v
                            #### v                   ######
                            <-                         <-
                    """  

                if line.dir == RIGHT:
                    box_width = min(prevprev.start[0], line.end[0]) - line.start[0]
                    """
                            ->
                          #######         or          ###
                        ^ #                           #
                        | ####                        ######
                            <-
                    """    

                if line.dir == DOWN:
                    box_width = min(line.end[1], prevprev.start[1]) - line.start[1]
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

                box_area = box_span * box_width

                if box_area > 0:
                    print(f"\nBox found at line {i}: {stack[i]}")
                    print("Stack before contraction:",stack)

                    if len(stack) == 4:
                        # Add the last box
                        if stack[0].dir == RIGHT or stack[0].dir == LEFT:
                            width = abs(stack[0].end[0] - stack[0].start[0])+1
                            height = abs(stack[1].end[1] - stack[1].start[1])+1
                        else:
                            height = abs(stack[0].end[1] - stack[0].start[1])+1
                            width = abs(stack[1].end[0] - stack[1].start[0])+1
                        print(f"Adding final box of size {height} * {width}")
                        box_area = height * width

                    # Do the contraction
                    area += box_area
                    print(f"Adding {box_area} area to make total {area}")
                    contract(i, stack)
                    i = 0
                else:
                    i += 1

            elif len(stack) > 0 and stack[i-1].dir == line.dir:
                # Merge with the previous line in the same direction
                print(f"Extending by {line.dir} * {line.length}")
                stack[i-1].extend(line.length)
                stack.remove(stack[i])

            elif len(stack) > 0 and stack[i-1].dir == opposite_dir(line.dir):
                # Reduce from the previous line in the opposite direction
                print(f"Reducing by {line.dir} * {line.length} (adding area)")
                area += line.length
                stack[i-1].extend(-1*line.length)
                stack.remove(stack[i])
            
            else:
                i+=1

    

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
    

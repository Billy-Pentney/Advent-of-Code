

def load(fname):
    with open(fname, "r") as file:
        line = file.readline().strip("\n")
    return line


def parse_layout(line):
    num = 0    
    n = len(line)
    layout = []

    for i in range(0,n+1,2):
        bits = int(line[i])
        layout += [num]*bits
        
        if i+1 < n:
            gap = int(line[i+1])
            layout += [None]*gap
        
        num += 1
    
    return layout

def defrag(layout):
    l = 0
    r = len(layout)-1

    while l < r:
        if layout[r] == None:
            r -= 1
        elif layout[l] != None:
            l += 1
        else:
            layout[l] = layout[r]
            layout[r] = None
            l += 1
            r -= 1

    return layout 



def compute_checksum(defragged):
    checksum = 0

    for i, bit in enumerate(defragged):
        if bit == None:
            continue
        num = bit
        checksum += num * i

    return checksum
        


def part_one(line):
    layout = parse_layout(line)
    # print(layout)
    # return 0
    defragged = defrag(layout)
    print("Defragged:", defragged[:100])
    return compute_checksum(defragged)





from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    line = load(fname)
    part_one_checksum = part_one(line)
    print(f"(Part 1) Defragged Checksum: {part_one_checksum}")
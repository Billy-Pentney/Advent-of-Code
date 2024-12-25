
import numpy as np


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
    
    return np.array(layout)

def defrag(layout):
    l = 0
    r = len(layout)-1

    while l < r:
        if layout[r] is None:
            r -= 1
        elif layout[l] is not None:
            l += 1
        else:
            layout[l] = layout[r]
            layout[r] = None
            l += 1
            r -= 1

    return layout 


def defrag_blocks(layout):

    ## Find all free regions

    ## Stores (idx,len) tuples
    ## where idx is the index of the start of the block and len is the length of the block 
    free_blocks = []
    free_len = 0
    for l, val in enumerate(layout):
        if val is None:
            free_len += 1
        elif free_len > 0:
            free_blocks.append((l-free_len, free_len))
            free_len = 0

    # print(free_blocks)

    ## Backward pass, moving blocks to the first free space if possible

    r = len(layout)-1
    block_len = 0

    while r > 0:
        if len(free_blocks) > 0 and free_blocks[0][0] > r:
            ## Stop when we've passed the first free block
            break

        if layout[r] is None:
            r -= 1
            block_len = 0
        else:
            ## Found an occupied cell on the right side
            block_len += 1

            ## Step through the block on the right
            while r > 0 and layout[r-1] == layout[r]:
                block_len += 1
                r -= 1

            # print(f"\nBlock: {r}-{r+block_len-1} with value {layout[r]}")
            # print(f"Free: {free_blocks}")

            ## Check if we've seen a free region that can take the block
            for i, blk in enumerate(free_blocks):
                free_idx, free_len = blk

                if free_idx >= r:
                    # We can't move the block to its right
                    break
                if free_len < block_len:
                    # Free space is not big enough
                    continue

                ## Copy the same value to the free region
                layout[free_idx:free_idx+block_len] = layout[r]
                ## Clear the value in the old block
                layout[r:r+block_len] = None

                print(f" >> Moved block {r}-{r+block_len} to {free_idx}-{free_idx+block_len}")
                # print(layout)
                
                if block_len < free_len:
                    ## Update the free space if we didn't use it all
                    new_free_idx = free_idx + block_len
                    new_free_len = free_len - block_len
                    free_blocks[i] = (new_free_idx, new_free_len)
                else:
                    # Occupy this block
                    free_blocks.remove(blk)

                break

            block_len = 0
            ## Step to the next block
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
    defragged = defrag(layout)
    print("Defragged:", defragged[:100])
    return compute_checksum(defragged)



def part_two(line):
    layout = parse_layout(line)
    # print(layout)
    defragged = defrag_blocks(layout)
    print("Defragged:", defragged[:100])
    return compute_checksum(defragged)




from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    line = load(fname)
    part_one_cs = part_one(line)
    print(f"(Part 1) Defragged Checksum: {part_one_cs}")

    print()
    part_two_cs = part_two(line)
    print(f"(Part 2) Block-Defragged Checksum: {part_two_cs}")
import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    # Drop the newline characters
    # Return the first line only
    return lines[0].replace("\n", "")


def hash_mod(s: str, div: int):
    val = 0
    for char in s:
        # val += ord(char)
        val = (((val * 17) % div + ord(char) * 17) % div) % div
    return val



## Solve Part One
def part_one(fileaddr):
    line = read_file(fileaddr)
    # Split into instruction steps
    instructions = line.split(",")

    print(instructions)

    hashes = [hash_mod(inst, 256) for inst in instructions]
    print(hashes)

    return sum(hashes)


def equals_op(inst_splits, box):
    # 2-tuple of (Label, Focal Length)
    new_lens = (inst_splits[0], int(inst_splits[1]))

    # Look for a lens with the same label
    for i,lens in enumerate(box):
        if lens[0] == new_lens[0]:
            # Replace the focal length (same label)
            box[i] = new_lens
            return box
        
    # Lens is not in box
    box.append(new_lens)
    return box

def dash_op(lens_label, box):
    # Check for a lens with same label
    for i, lens in enumerate(box):
        if lens[0] == lens_label:
            # If found, remove it
            box.remove(lens)
            return box
        
    # Not found, no changes to the box
    return box


# Display only the boxes with at least one lens
def print_nonempty_boxes(boxes):
    for i,box in enumerate(boxes):
        if len(box) > 0:
            print(f"Box {i}: {box}")



def compute_box_focal_power(box, box_num):
    focal_power = sum([(i+1) * lens[1] for i, lens in enumerate(box)])    
    # Common factor is multipled at end
    return box_num * focal_power



## Solve Part Two
def part_two(fileaddr):
    line = read_file(fileaddr)
    # Split into instruction steps
    instructions = line.split(",")

    num_boxes = 256

    boxes = [[] for x in range(0, num_boxes)]

    for inst in instructions:
        if '=' in inst:
            inst_splits = inst.split('=')
            label = inst_splits[0]
            box_num = hash_mod(label, num_boxes)
            boxes[box_num] = equals_op(inst_splits, boxes[box_num])
        elif '-' in inst:
            inst_splits = inst.split('-')
            lens_label = inst_splits[0]
            box_num = hash_mod(lens_label, num_boxes)
            boxes[box_num] = dash_op(lens_label, boxes[box_num])

        # print_nonempty_boxes(boxes)
        # print("-------")

    box_focal_power = [compute_box_focal_power(box, i+1) for i, box in enumerate(boxes)]
    # print(box_focal_power)
    return sum(box_focal_power)










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
    

import sys, os
import re

num_regex = re.compile("(\-?\d+)")


def read_file(fileaddr):
    text = []
    with open(fileaddr, "r") as file:
        text = file.read()
    return text




## Solve Part One
def part_one(fileaddr):
    text = read_file(fileaddr)
    total = 0

    for match in num_regex.findall(text):
        num = int(match)
        # print(num)
        total += num

    return total



import json


def sum_json_nums(json_obj):
    total = 0
    # print("Summing", json_obj)

    if isinstance(json_obj, str):
        return 0
    elif isinstance(json_obj, bool):
        return 0

    if isinstance(json_obj, dict):
        if 'red' in json_obj.values():
            print(f"Skipping {json_obj} with value 'red'")
            return 0
        for attr, val in json_obj.items():
            total += sum_json_nums(val)
    elif isinstance(json_obj, list):
        for obj in json_obj:
            total += sum_json_nums(obj)
    elif isinstance(json_obj, int) or isinstance(json_obj, float):
        total += json_obj
    
    return total


## Solve Part Two
def part_two(fileaddr):
    text = read_file(fileaddr)

    json_dict = json.loads(text)
    print(json_dict)
    
    return sum_json_nums(json_dict)
    # return 0










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    # part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(1)

    part_one_ans = part_one(fileaddr)
    print(f"(Part 1) Solution: {part_one_ans}")
    
    part_two_ans = part_two(fileaddr)
    print(f"(Part 2) Solution: {part_two_ans}")


import numpy as np


def load(fname):
    with open(fname, "r") as file:
        ids = file.readlines()[0].split(",")
    
    ids_parsed = []
    for id in ids:
        splits = id.split("-")
        if len(splits) > 0:
            # A range of ids
            start = splits[0]
            end = splits[1]
        else:
            start = id
            end = id
        ids_parsed.append((int(start), int(end)))

    return ids_parsed


cache_is_invalid = {}

def is_string_made_of(number, segment):
    """
    Returns true if and only if number can be made solely from concatenating segment
    """
    
    ## Blank string is tail-case; can always be made from a string
    if number == "":
        return True

    ## If the same length or longer, the string must be the segment itself.
    ## Also if the number is not divisible by the segment length, it cannot be split.
    if len(segment) >= len(number) or len(number) % len(segment) != 0:
        return number == segment
    
    ## Otherwise, split off the first k characters
    head = number[:len(segment)]
    tail = number[len(segment):]
    
    ## Check that they match the segment and recurse to check the rest of the string
    return head == segment and is_string_made_of(tail,segment)


def is_num_invalid(num: int, part=2):
    """
    Check if a product id is invalid according.
    In part one, an id is invalid if it can be split into two identical halves.
        e.g. 1212, 98769876 and 99 are invalid but 929292 is valid
    In part two, an id is invalid if it can be constructed solely by repeating one number.
        e.g. 11, 21212121, 98779877 are invalid but 123451234 is valid
    """

    if num in cache_is_invalid.keys():
        return cache_is_invalid[num]
    
    chars = str(num)
    l = len(chars)
    h = l // 2

    if part == 1:
        ## Check if the string is formed from two equal halves
        cache_is_invalid[num] = chars[:h] == chars[h:]
    else:
        cache_is_invalid[num] = False

        ## Check up to half the string
        for d in range(1, h+1):
            ## Check if the id is *only* concatenations of the first d characters
            if is_string_made_of(chars, chars[:d]):
                cache_is_invalid[num] = True
                # print("Invalid:", num)
                break
            
    return cache_is_invalid[num]


def is_num_duplicated(num: int):
    """ Returns true if num is formed from one number repeated exactly once. """
    return is_num_invalid(num, part=1)



def sum_invalid_ids(nums: list, part=1):
    """
    Calculate the sum of all the invalid ids in the given list.
    Parameter 'part' specifies if the validity function should be according to Part 1 or Part 2 of the question.
    """

    all_invalid_nums = set()

    # Reset the cache from previous runs
    cache_is_invalid.clear()

    ## Question part alters which validity function is used
    invalid_func = is_num_duplicated if part == 1 else is_num_invalid
    invalid_func_vect = np.vectorize(invalid_func)
    
    for start, end in nums:
        ## Check all ids in this range
        nums_to_check = np.arange(start, end+1)
        ## Apply the function to determine which are invalid ids
        idx_of_invalid = np.argwhere(invalid_func_vect(nums_to_check))

        if len(idx_of_invalid) > 0:
            ## Get the invalid ids as a list
            invalid_nums = list(nums_to_check[idx_of_invalid].flatten())
            # print(invalid_ids)
            all_invalid_nums = all_invalid_nums.union(invalid_nums)


    all_invalid_nums = np.array(sorted(all_invalid_nums))
    print(all_invalid_nums)
    return np.sum(all_invalid_nums, dtype=np.int64)




from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    ids = load(fname)

    part_one = sum_invalid_ids(ids, part=1)
    print(f"Part 1: {part_one}")
    print()
    part_two = sum_invalid_ids(ids, part=2)
    print(f"Part 2: {part_two}")

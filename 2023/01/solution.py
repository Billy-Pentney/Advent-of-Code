
# File-Handling
import os
import sys
# Regex
import re


mapping = {'one': 1,'two': 2,'three': 3,'four': 4,'five': 5,'six': 6,'seven': 7,'eight': 8,'nine': 9}
re_pattern = "(" + "|".join(list(mapping.keys())) + ")"
numword_regex_start = re.compile(f"({re_pattern}|\d)(.*)")
numword_regex_end = re.compile(f"(.*)({re_pattern}|\d)")
digit_regex_start = re.compile("(\d)(.*)")
digit_regex_end = re.compile("(.*)(\d)")




def find_first_digit_in(row: str, include_words):
    if include_words:
        match = numword_regex_start.search(row)
    else:
        match = digit_regex_start.search(row)

    if match:
        match_word = match.group(1)
        if len(match_word) == 1:
            return match_word
        return str(mapping[match_word])



def find_last_digit_in(row: str, include_words):
    if include_words:
        match = numword_regex_end.search(row)
    else:
        match = digit_regex_end.search(row)

    if match:
        match_word = match.group(2)
        if len(match_word) == 1:
            return match_word
        return str(mapping[match_word])



def row_calibration_val(row: str, part):
    first_digit = find_first_digit_in(row, part=='2')
    last_digit = find_last_digit_in(row, part=='2')
    return int(first_digit + last_digit)



def total_of_file(filename, part):
    file = open(filename, "r")
    total = 0

    for line in file.readlines():
        total += row_calibration_val(line, part)

    return total



def run_on_file(fileaddr, part='1'):
    if os.path.exists(fileaddr):
        total = total_of_file(fileaddr, part)
        print(total)
    else:
        print(f"Could not find file at location {fileaddr}")




if __name__ == '__main__':
    args = sys.argv[1:]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]
    part = args[1]
    run_on_file(fileaddr, part)


""" Answers 
    Part 1: 55607
    Part 2: 55291
"""
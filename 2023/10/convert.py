import sys

replacement = {
    'F': '┌',
    'J': '┘',
    'L': '└', 
    '7': '┐',
    '-': '─',
    '|': '│' 
}


def apply_replacement(line):
    for char in replacement.keys():
        line = line.replace(char, replacement[char])
    return line


if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    input_name = filename + ".txt"
    output_name = filename + "_edit.txt"

    lines = []
    with open(input_name, "r") as input:
        lines = input.readlines()

    new_lines = [apply_replacement(line) for line in lines]

    with open(output_name, "w", encoding="utf-8") as output:
        output.writelines(new_lines)

    print("Done!")
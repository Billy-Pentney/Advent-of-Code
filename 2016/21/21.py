
import numpy as np
import regex as re
from abc import ABC

REGEX_SWAP_POS = r"swap position (\d+) with position (\d+)"
REGEX_SWAP_LETTER = r"swap letter (\w+) with letter (\w+)"
REGEX_REVERSE = r"reverse positions (\d+) through (\d+)"
REGEX_ROTATE = r"rotate (left|right) (\d+)"
REGEX_MOVE_POS = r"move position (\d+) to position (\d+)"
REGEX_ROTATE_BY_POS = r"rotate based on position of letter (\w+)"

class Operation(ABC):
    def __init__(self, self_inverse=False):
        self.inverse=None
        if self_inverse:
            self.inverse = self
    def apply(self, text: str) -> str:
        return text
    def get_inverse(self):
        return self.inverse
    def undo(self, text: str) -> str:
        inverse = self.get_inverse()
        if inverse:
            return self.get_inverse().apply(text)
        else:
            raise Exception("Operation has no inverse!")
    
class Rotate(Operation):
    def __init__(self, direction, amount):
        super().__init__()
        self.left = direction == "left"
        self.amount = amount

    def get_inverse(self):
        direction = "right" if self.left else "left"
        return Rotate(direction, self.amount)
    
    def apply(self, text):
        ## A full rotation is the length of the text
        amount = self.amount % len(text)
        if self.left:
            pre = text[:amount]
            suf = text[amount:]
        else:
            pre = text[:-amount]
            suf = text[-amount:]
        return suf + pre
    
    def __repr__(self):
        return f"Rotate({self.amount}, left={self.left})"

class Rotate_By_Position(Rotate):
    def __init__(self, letter: str, **kwargs):
        super().__init__("right", 0)
        self.letter = letter

    def get_inverse(self):
        return Rotate_By_Position_Inverse(self.letter)

    def __repr__(self):
        return f"RotateByPos({self.letter})"

    def apply(self, text):
        # Once the index is determined, rotate the string to the right one time, 
        # plus a number of times equal to that index, plus one additional time if the index was at least 4.
        idx = text.index(self.letter)
        self.amount = 1 + idx + (1 if idx >= 4 else 0)  
        return super().apply(text)

    def undo(self, text):
        idx = text.index(self.letter)
        self.amount = 0
        for original_idx in range(len(text)):
            original_amt = original_idx + 1 + (1 if original_idx >= 4 else 0)
            if (original_idx + original_amt) % len(text) == idx:
                self.amount = len(text) - original_amt
        return super().apply(text)
    
class Rotate_By_Position_Inverse(Rotate):
    def __init__(self, letter: str, **kwargs):
        super().__init__("left", 0)
        self.letter = letter

    def get_inverse(self):
        return Rotate_By_Position(self.letter)

    def __repr__(self):
        return f"RotateByPosInverse({self.letter})"

    def apply(self, text):
        # Once the index is determined, rotate the string to the right one time, 
        # plus a number of times equal to that index, plus one additional time if the index was at least 4.
        idx = text.index(self.letter)
        self.amount = 0
        ## Find the index which moved the letter to its current position
        for original_idx in range(len(text)):
            original_amt = original_idx + 1 + (1 if original_idx >= 4 else 0)
            if (original_idx + original_amt) % len(text) == idx:
                self.amount = original_amt
        return super().apply(text)

class Move_Pos(Operation):
    def __init__(self, from_pos: int, to_pos: int):
        super().__init__()
        self.from_pos = from_pos
        self.to_pos = to_pos

    def get_inverse(self):
        return Move_Pos(from_pos=self.to_pos, to_pos=self.from_pos)

    def apply(self, text):
        from_pos = self.from_pos
        to_pos = self.to_pos
        letter = text[self.from_pos]
        result = ""

        if from_pos < to_pos:
            ## Move right
            if from_pos > 0:
                result += text[:from_pos]
            result += text[from_pos+1:to_pos+1]
            result += letter
            if to_pos+1 < len(text):
                result += text[to_pos+1:]
        else:
            ## Move left
            if to_pos > 0:
                result += text[:to_pos]
            result += letter
            result += text[to_pos:from_pos]
            if from_pos+1 < len(text):
                result += text[from_pos+1:]
        return result
    
    def __repr__(self):
        return f"MovePos({self.from_pos} -> {self.to_pos})"
    
class Swap_Pos(Operation):
    def __init__(self, from_pos: int, to_pos: int):
        super().__init__(self_inverse=True)
        self.from_pos = from_pos
        self.to_pos = to_pos

    def __repr__(self):
        return f"SwapPos({self.from_pos} -> {self.to_pos})"

    def apply(self, text):
        text_list = list(text)
        t = text_list[self.from_pos]
        text_list[self.from_pos] = text_list[self.to_pos]
        text_list[self.to_pos] = t
        return "".join(text_list)
    
class Swap_Letter(Operation):
    def __init__(self, from_letter: str, to_letter: str):
        super().__init__(self_inverse=True)
        self.from_letter = from_letter
        self.to_letter = to_letter

    def apply(self, text):
        text2 = text.replace(self.from_letter, "$")
        text3 = text2.replace(self.to_letter, self.from_letter)
        return text3.replace("$", self.to_letter)
    
    def __repr__(self):
        return f"SwapLetter({self.from_letter}, {self.to_letter})"
    
class Reverse(Operation):
    def __init__(self, from_idx: int, to_idx: int):
        super().__init__(self_inverse=True)
        self.from_idx = from_idx
        self.to_idx = to_idx

    def apply(self, text):
        result = ""
        if self.from_idx > 0:
            result += text[:self.from_idx]
        mid = text[self.from_idx:self.to_idx+1]
        result += mid[::-1]
        if self.to_idx < len(text):
            result += text[self.to_idx+1:]
        return result
        
    def __repr__(self):
        return f"Reverse({self.from_idx}, {self.to_idx})"



map_regex_to_operation = {
    REGEX_ROTATE_BY_POS: Rotate_By_Position,
    REGEX_ROTATE: Rotate,
    REGEX_MOVE_POS: Move_Pos,
    REGEX_SWAP_LETTER: Swap_Letter,
    REGEX_SWAP_POS: Swap_Pos,
    REGEX_REVERSE: Reverse
}

def parse_line(line: str) -> Operation:
    if line.startswith("reverse"):
        regex = REGEX_REVERSE
    elif line.startswith("move"):
        regex = REGEX_MOVE_POS
    elif line.startswith("rotate based"):
        regex = REGEX_ROTATE_BY_POS
    elif line.startswith("rotate"):
        regex = REGEX_ROTATE
    elif line.startswith("swap position"):
        regex = REGEX_SWAP_POS
    elif line.startswith("swap letter"):
        regex = REGEX_SWAP_LETTER
    else:
        return None
    
    match = re.match(regex, line)
    if not match:
        return None
    Op = map_regex_to_operation[regex]
    
    groups = []
    for i, group in enumerate(match.groups()):
        groups.append(group)
        if group.isnumeric():
            groups[i] = int(group)

    if len(groups) > 1:
        return Op(groups[0], groups[1])
    else:
        return Op(groups[0])


def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    input_text = lines[0]
    operations = []
    for line in lines[1:]:
        op = parse_line(line)
        if op:
            operations.append(op)

    return input_text, operations


def apply_operations(text:str, operations, verbose=False):
    texts = [text]
    for instruction in operations:
        new_text = instruction.apply(texts[-1])
        if verbose:
            print(f"{instruction}: {texts[-1]} -> {new_text}")
        texts.append(new_text)
    return texts


from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    input_text, operations = load(fname)
    print(input_text)
    verbose = True

    texts = apply_operations(input_text, operations, verbose=verbose)
    print("Part one:", texts[-1])

    print("\n")
    # part_two_input = texts[-1]
    part_two_input = "fbgdceah"
    reverse_operations = reversed([op.get_inverse() for op in operations])
    rev_texts = apply_operations(part_two_input, reverse_operations, verbose=verbose)
    print("Part two:", rev_texts[-1])
    
    ## Debugging: show the pairs from forward and backward runs 
    # for i, (t1, t2) in enumerate(zip(texts, reversed(rev_texts))):
    #     print(f" > {t1} vs {t2}   {t1 == t2}")
    #     if i < len(operations):
    #         print(operations[i])

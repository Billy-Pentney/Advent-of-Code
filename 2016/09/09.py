
import numpy as np
import regex as re


def load(fname):
    with open(fname, "r") as file:
        input_text = [row.strip("\n") for row in file.readlines()]

    return input_text

## Matches a bracketed "(AxB)" describing a compressed segment 
# * Group 1: the width of the repeated section (A)
# * Group 2: the num of repetitions (B)
re_pattern = re.compile(r"\((\d+)x(\d+)\)")

def decompress(text: str):
    """
    Decompresses by expanding all terms, ignoring any compressed states within the expanded regions.
    e.g. "X(8x2)(3x3)ABCY" -> "X(3x3)ABC(3X3)ABCY"
    Returns the decompressed string.
    """
    i = 0
    decompressed = ""
    while i < len(text):
        match = re_pattern.search(text, pos=i)
        if not match:
            break
        j = match.start(0)
        if i < j:
            ## Append everything since the last repeated section
            decompressed += text[i:j]
            i = j
        code_len = len(match.group(0))
        width = int(match.group(1))
        n_repetitions = int(match.group(2))
        start = i + code_len
        end = start + width
        if width > 0 and n_repetitions > 0:
            # print(" > \'" + text[start:end] + "\' *", n_repetitions)
            decompressed += text[start:end]*n_repetitions
            # print(text[end:end+20])
        i = end

    if i < len(text):
        decompressed += text[i:]

    return decompressed

def decompress_v2_for_length(text: str):
    """
    Decompresses by repeating all subsequent characters (including multiplication markers).
    e.g. "X(8x2)(3x3)ABCY" -> "X(3x3)ABC(3x3)ABCY" -> "XABCABCABCABCABCABCY" -> 20
    Returns the number of characters in the decompressed string. 
    """
    match = re_pattern.search(text)
    if not match:
        ## Nothing to expand
        return len(text)
    
    width = int(match.group(1))
    n_repetitions = int(match.group(2))
    before_match = text[:match.start(0)]
    start = match.end(0)
    end = start + width
    repeated = text[start:end]
    # print(f" > \'{repeated}\' x {n_repetitions}")
    ## Add the repeated section, plus the non-repeated characters since the last repetition

    ## Decompress the segment which is duplicated
    nested_len = decompress_v2_for_length(repeated)
    len_repeated = nested_len * n_repetitions
    ## Decompress the non-repeated segment
    len_suffix = decompress_v2_for_length(text[end:])
    # print(f"Expanding \'{text[:end]}\', with: {nested_len}*{n_repetitions}, and suffix: \'{text[end:]}\'")
    ## Get the length of the bit which isn't repeated
    len_prefix = len(before_match)
    # print(len_prefix, len_repeated, len_suffix)
    ## Calculate the actual length of the decompressed string
    total_length = len_prefix + len_repeated + len_suffix
     
    return total_length


def count_decompressed_length(texts:str):
    for text in texts:
        decompressed = decompress(text)
        length = len(decompressed.replace(" ", ""))
        print(f"\'{text}\' -> \'{decompressed}\' ({length})")

def count_decompressed_length_v2(texts:str):
    for text in texts:
        print(f"\'{text}\'")
        decompressed_length = decompress_v2_for_length(text)
        print(f" -> {decompressed_length}")



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    if len(argv) > 2:
        part = argv[2]
    else:
        part = '1'
    input_texts = load(fname)

    if part == '1':
        count_decompressed_length(input_texts)
    else:
        count_decompressed_length_v2(input_texts)
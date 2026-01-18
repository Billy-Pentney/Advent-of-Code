
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    rooms = []
    for line in lines:
        splits = line.strip("]").split("[")
        segments = splits[0].split("-")
        room = segments[:-1]
        sector_id = int(segments[-1])
        checksum = splits[1]
        rooms.append((room,sector_id,checksum))

    return rooms

from collections import defaultdict

def is_room_valid(codes, checksum):
    letters_by_frequency = defaultdict(lambda: 0)
    for segment in codes:
        for l in segment:
            letters_by_frequency[l] += 1

    ## Sort by descending count, then by alphabetical letter
    letters_sorted = sorted(letters_by_frequency.keys(), key=lambda l: (-letters_by_frequency[l], l))

    if len(letters_sorted) < len(checksum):
        return False
    
    new_checksum = "".join(letters_sorted[:len(checksum)])
    ## Check that the checksum matches
    return new_checksum == checksum

def find_valid_sectors(rooms):
    sum_valid_sectors = 0

    for segments, sector_id, checksum in rooms:
        # print(segments, sector_id, checksum)
        if is_room_valid(segments, checksum):
            # print(" > Valid")
            sum_valid_sectors += sector_id
        # else:
            # print(" > Not valid")

    return sum_valid_sectors

def find_sector_with_cipher(rooms, keyword='northpole', write_to=None):
    """
    Decipher the room-code segments reversing the Caeser cipher.
    Return a list of sector ids for those rooms whose decoded form contains the given keyword.
    If 'write_to' is true, then the output for each room will be written to a local file 'output.txt'.
    """

    output = []
    sector_ids = []

    for segments, sector_id, checksum in rooms:
        # print(segments, sector_id, checksum)
        shift = sector_id % 26
        text = ""
        for segment in segments:
            for letter in segment:
                offset = (ord(letter) - ord('a') + shift) % 26
                text += chr(ord('a') + offset)
            text += " "

        output.append(f"{text} > {sector_id}\n")
        if keyword in text:
            sector_ids.append(sector_id)
    
    if write_to:
        output = sorted(output)
        filename = "output.txt"
        with open(filename, "w") as file:
            file.writelines(output)
        print(f"Saved to {filename}")

    return sector_ids
    


from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    rooms = load(fname)

    sum_valid_sectors = find_valid_sectors(rooms)
    print(f"Part one: {sum_valid_sectors}")

    northpole_sectors = find_sector_with_cipher(rooms, 'northpole')
    print(f"Part two: {northpole_sectors}")
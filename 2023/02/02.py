import re
import os, sys

from BoxColors import BoxColors
from Game import Game

def parse_color_count(full_text, pattern_to_find):
    match = re.search(pattern_to_find, full_text)
    if (match):
        return int(match.group(1))
    return 0

def parse_cycles(text: str):
    green_pattern = "(\d+) green"
    red_pattern = "(\d+) red"
    blue_pattern = "(\d+) blue"

    cycles = []
    for cycle in text.split(";"):
        green_count = parse_color_count(cycle, green_pattern)
        blue_count = parse_color_count(cycle, blue_pattern)
        red_count = parse_color_count(cycle, red_pattern)
        cycles.append(BoxColors(r=red_count, b=blue_count, g=green_count))

    return cycles


def parse_row(row: str):
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    game_pattern = "Game (\d+): (.+)$"
    game_regex = re.compile(game_pattern)
    match = game_regex.search(row)

    if (match):
        game_id = int(match.group(1))
        cycles = parse_cycles(match.group(2))
        game = Game(game_id, cycles)
        return game

    return None
    

def parse_games(fileaddr):
    games = []
    with open(fileaddr, "r") as file:
        for line in file.readlines():
            games.append(parse_row(line))
    return games


def sum_of_possible_ids(games, max_box_colors: BoxColors):
    possible_game_id_sum = 0
    for game in games:
        if game.is_possible(max_box_colors):
            possible_game_id_sum += game.id
        else:
            print(f"{game} is impossible!")

    return possible_game_id_sum


def sum_of_game_powers(games):
    sum_of_powers = 0
    for game in games:
        sum_of_powers += game.compute_power()
    return sum_of_powers


if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        games = parse_games(fileaddr)
        if (part == '1'):
            max_box_colors = BoxColors(r=12, g=13, b=14)
            result = sum_of_possible_ids(games, max_box_colors)
        else:
            result = sum_of_game_powers(games)
        print(result)
    else:
        print(f"Could not find file at location {fileaddr}")
    


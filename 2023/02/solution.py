import re
import os, sys

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

class BoxColors:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def __repr__(self):
        return f"({self.r}R, {self.g}G, {self.b}B)"
    
    def exceeds(self, other):
        return self.r > other.r or self.g > other.g or self.b > other.b
    
    def max_with(self, other):
        self.r = max(self.r, other.r)
        self.g = max(self.g, other.g)
        self.b = max(self.b, other.b)

    def power(self):
        return self.r * self.g * self.b


class Game:
    def __init__(self, id, cycles):
        self.id = id
        self.cycles = cycles
    
    def __str__(self):
        return f"Game #{self.id}: {self.cycles}"
    
    def is_possible(self, max_box_colors):
        for colors in self.cycles:
            if colors.exceeds(max_box_colors):
                return False
            
        return True

    def compute_power(self):
        req_colors = BoxColors(0,0,0)
        for cycle in self.cycles:
            req_colors.max_with(cycle)
        power = req_colors.power()
        # print(self, "has power:", power)
        return power


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
    fileaddr = get_script_path() + "\\" + args[0]

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
    


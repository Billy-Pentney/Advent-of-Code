import sys, os
import re

from Scratchcard import Scratchcard

list_nums_pattern = "((?: *\d+)+)"

scratchcard_pattern = f"Card  *(\d+): *{list_nums_pattern} \| *{list_nums_pattern}"
scratchcard_re = re.compile(scratchcard_pattern)


def parse_scratchcard(line):
    match = scratchcard_re.match(line)
    if not match:
        return None
    
    splitNums = lambda arr: [int(x) for x in arr.split(" ") if len(x) > 0 and x.isdigit()]
    
    id = int(match.group(1))
    win_nums = splitNums(match.group(2))
    act_nums = splitNums(match.group(3))
    return Scratchcard(id, win_nums, act_nums)


def load_cards(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    cards = []
    for line in lines:
        card = parse_scratchcard(line)
        if card is not None:
            cards.append(card)    
    
    return cards


## Part 1
def calculate_total_score(fileaddr):
    cards = load_cards(fileaddr)
    score = 0
    for card in cards:
        print(card)
        score += card.score

    print("Total Scratchcards:", str(len(cards)))
    return score  
    

## Part 2
def count_cards_incrementing(fileaddr):
    cards = load_cards(fileaddr)
    total_cards = 0

    # Evaluate each card, updating its subsequent cards
    for i,card in enumerate(cards):
        # Increment the counts of the next j cards
        for j in range(0, card.num_wins):
            if i+j+1 >= len(cards):
                break
            # Each card with id i adds a new card j steps below it
            cards[i+j+1].count += card.count
            
        print(f"Card #{i+1} has count={card.count}")
        # This card's count won't be updated again
        total_cards += card.count

    return total_cards


if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if (part == '1'):
            result = calculate_total_score(fileaddr)
        else:
            result = count_cards_incrementing(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    


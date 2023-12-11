import sys, os
import re


max_card_value = 20
card_value = {
   'A': 14,'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,'2': 2
}


# Five of a kind, where all five cards have the same label: AAAAA
FIVE_KIND = 10
# Four of a kind, where four cards have the same label and one card has a different label: AA8AA
FOUR_KIND = 9
# Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
FULL_HOUSE = 8
# Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
THREE_KIND = 7
# Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
TWO_PAIR = 6
# One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
ONE_PAIR = 5
# High card, where all cards' labels are distinct: 23456
HIGH_CARD = 4

descending_types = reversed([FIVE_KIND, FOUR_KIND, FULL_HOUSE, THREE_KIND, TWO_PAIR, ONE_PAIR, HIGH_CARD])


def identify_hand(hand: str):
    hand_counts = {}
    for card in hand:
        if card in hand_counts.keys():
            hand_counts[card] += 1
        else:
            hand_counts[card] = 1

    # Get the counts of each card in descending order e.g. [2,2,1]
    counts = sorted(list(hand_counts.values()), reverse=True)
    
    if counts[0] == 5:
        return FIVE_KIND
    elif counts[0] == 4:
        return FOUR_KIND
    elif counts[0] == 3 and counts[1] == 2:
        return FULL_HOUSE
    elif counts[0] == 3:
        return THREE_KIND
    elif counts[0] == 2 and counts[1] == 2:
        return TWO_PAIR
    elif counts[0] == 2:
        return ONE_PAIR
    elif counts[0] == 1:
        return HIGH_CARD   

    return None


class Hand:
    def __init__(self, hand: str, bid: int):
        self.cards = hand
        self.bid = bid
        self.type = identify_hand(hand)

    def __repr__(self):
        return f"(Hand={self.cards}, Type={self.type}, Bid={self.bid})"
    
    def to_value(self):
        val = 0
        for card in self.cards:
            val = val * max_card_value + card_value[card]
        return val

# For sorting comparison
def compare_hands(H1, H2):
    if H1.type != H2.type:
        return H1.type - H2.type

    for i in range(0, len(H1.cards)):
        card_1 = card_value[H1.cards[i]]
        card_2 = card_value[H2.cards[i]]
        # H1 is stronger than H2
        if card_2 < card_1:
            return 1
        # H1 is weaker than H2
        elif card_1 < card_2:
            return -1

    # Equal hand strengths
    return 0


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return lines


def parse_hands(lines):
    # For key T, store a list of hands of type T
    hands = {}

    for line in lines:
        splits = line.split(" ")
        hand = splits[0]
        bid = splits[1]
        h = Hand(hand, int(bid))

        if h.type in hands.keys():
            hands[h.type].append(h)
        else:
            hands[h.type] = [h]
                 
    return hands



## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)
    grouped_hands = parse_hands(lines)
    # print(grouped_hands)

    all_hands = []

    for type in grouped_hands.keys():
        # Sort all hands of a given type by increasing hand order
        grouped_hands[type].sort(key=lambda h: h.to_value())

    for type in descending_types:
        if type in grouped_hands.keys():
            all_hands.extend(grouped_hands[type])
        
    # print(all_hands)

    sum_winnings = 0
    for i, hand in enumerate(all_hands):
        rank = i+1
        sum_winnings += rank * hand.bid

    return sum_winnings


## Solve Part Two
def part_two(fileaddr):
    return










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if (part == '1'):
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    

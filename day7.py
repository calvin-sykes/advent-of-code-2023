from collections import Counter
from functools import cmp_to_key
from itertools import combinations_with_replacement

cards = "23456789TJQKA"
cards_jokers = "J23456789TQKA"

HIGH_CARD = 1
ONE_PAIR = 2
TWO_PAIR = 3
THREE_KIND = 4
FULL_HOUSE = 5
FOUR_KIND = 6
FIVE_KIND = 7

def hand_type(hand):
    counts = Counter(hand).most_common()
    match counts[0][1]:
        case 5:
            return FIVE_KIND
        case 4:
            return FOUR_KIND
        case 3:
            if counts[1][1] == 2:
                return FULL_HOUSE
            else:
                return THREE_KIND
        case 2:
            if counts[1][1] == 2:
                return TWO_PAIR
            else:
                return ONE_PAIR
        case 1:
            return HIGH_CARD

def hand_type_jokers(hand):
    best_type = hand_type(hand)
    if "J" not in hand:
        return best_type
    else:
        nj = hand.count("J")
        unique_cards = set(c for c in hand if c != "J")
        # Generate every permutation of jokers turned into other cards, and check each for score
        for combi in combinations_with_replacement(unique_cards, nj):
            wild_hand = hand.replace("J", "{}").format(*combi)
            wild_type = hand_type(wild_hand)
            if wild_type > best_type:
                best_type = wild_type
    return best_type

def compare_hand_value(h1, h2, wild_jokers=False):
    type_fn = hand_type_jokers if wild_jokers else hand_type
    card_order = cards_jokers if wild_jokers else cards
        
    t1 = type_fn(h1)
    t2 = type_fn(h2)

    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    else:
        for c1, c2 in zip(h1, h2):
            i1 = card_order.index(c1)
            i2 = card_order.index(c2)
            return (i1 > i2) - (i1 < i2)
    return 0

compare_hand_key = cmp_to_key(compare_hand_value)
compare_hand_key_jokers = cmp_to_key(lambda h1, h2: compare_hand_value(h1, h2, wild_jokers=True))

def day7_part1(filename):
    with open(filename) as f:
        lines = f.readlines()

    games = []
    for l in lines:
        hand, bid = l.split()
        games.append((hand, int(bid)))

    sorted_games = sorted(games, key=lambda g: compare_hand_key(g[0]))
    winnings = sum(r * g[1] for r, g in enumerate(sorted_games, 1))    
    return winnings

def day7_part2(filename):
    with open(filename) as f:
        lines = f.readlines()

    games = []
    for l in lines:
        hand, bid = l.split()
        #print(hand_type(hand), "->", hand_type_jokers(hand))
        games.append((hand, int(bid)))

    sorted_games = sorted(games, key=lambda g: compare_hand_key_jokers(g[0]))
    winnings = sum(r * g[1] for r, g in enumerate(sorted_games, 1))    
    return winnings

if __name__ == "__main__":
    print("Part 1 example", day7_part1("input/day7_example.txt"))
    print("Part 1 extra", day7_part1("input/day7_extra.txt"))
    print("Part 1", day7_part1("input/day7.txt"))
    print("Part 2 example", day7_part2("input/day7_example.txt"))
    print("Part 2 extra", day7_part2("input/day7_extra.txt"))
    print("Part 2", day7_part2("input/day7.txt"))

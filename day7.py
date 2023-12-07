from collections import Counter
from functools import cmp_to_key
from itertools import combinations_with_replacement

cards = "23456789TJQKA"
cards_jokers = "J23456789TQKA"

type_score = {"high_card": 1, "one_pair": 2, "two_pair": 3,
              "three_kind": 4, "full_house": 5, "four_kind": 6, "five_kind": 7}

def hand_type(hand):
    counts = Counter(hand).most_common()
    match counts[0][1]:
        case 5:
            return "five_kind"
        case 4:
            return "four_kind"
        case 3:
            if counts[1][1] == 2:
                return "full_house"
            else:
                return "three_kind"
        case 2:
            if counts[1][1] == 2:
                return "two_pair"
            else:
                return "one_pair"
        case 1:
            return "high_card"

def hand_type_jokers(hand):
    best_type = hand_type(hand)
    if "J" not in hand:
        return best_type
    else:
        nj = hand.count("J")
        unique_cards = Counter(hand)
        del unique_cards["J"]
        unique_cards = "".join([c * cnt for c, cnt in unique_cards.items()])
        # Generate every permutation of jokers turned into other cards, and check each for score
        for combi in combinations_with_replacement(unique_cards, nj):
            wild_hand = unique_cards + "".join(combi)
            wild_type = hand_type(wild_hand)
            if type_score[wild_type] > type_score[best_type]:
                best_type = wild_type
    return best_type

def compare_hand_value(h1, h2, wild_jokers=False):
    type_fn = hand_type_jokers if wild_jokers else hand_type
    card_order = cards_jokers if wild_jokers else cards
        
    t1 = type_score[type_fn(h1)]
    t2 = type_score[type_fn(h2)]

    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    else:
        for c1, c2 in zip(h1, h2):
            i1 = card_order.index(c1)
            i2 = card_order.index(c2)
            if i1 < i2:
                return -1
            elif i1 > i2:
                return 1
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
    print("Part 1", day7_part1("input/day7.txt"))
    print("Part 2 example", day7_part2("input/day7_example.txt"))
    print("Part 2", day7_part2("input/day7.txt"))

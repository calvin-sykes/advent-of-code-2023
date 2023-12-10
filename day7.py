from collections import Counter
from functools import cmp_to_key

cards = "23456789TJQKA"
cards_jokers = "J23456789TQKA"

def hand_score(hand):
    counts = Counter(hand).most_common()
    score = 10 * counts[0][1]
    # Special cases:
    # Two pair better than one pair
    # Full house better than three-of-a-kind
    if score in {20, 30}:
        score += counts[1][1]
    return score

def hand_score_jokers(hand):
    if "J" not in hand:
        return hand_score(hand)
    else:
        counts = Counter(hand.replace("J", ""))
        if len(counts) > 0:
            best_card = counts.most_common()[0][0]
        else:
            best_card = "A"
        wild_hand = hand.replace("J", best_card)
        return hand_score(wild_hand)

def compare_hand_value(h1, h2, wild_jokers=False):
    type_fn = hand_score_jokers if wild_jokers else hand_score
    card_order = cards_jokers if wild_jokers else cards
        
    t1 = type_fn(h1)
    t2 = type_fn(h2)

    if t1 != t2:
        return t1 - t2
    else:
        for c1, c2 in zip(h1, h2):
            i1 = card_order.index(c1)
            i2 = card_order.index(c2)
            if i1 != i2:
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
        #print(hand_score(hand), "->", hand_score_jokers(hand))
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

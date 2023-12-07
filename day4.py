class Card:
    def __init__(self, number, winning, present):
        self.num = number
        self.winning = set(winning)
        self.present = set(present)

    def __repr__(self):
        return f"Card(num={self.num})"

    def matched(self):
        if not hasattr(self, "_matched"):
            self._matched = self.winning.intersection(self.present)
        return self._matched
    
    def num_matched(self):
        return len(self.matched())

    def points(self):
        nmatch = self.num_matched()
        if nmatch > 0:
            return 2**(nmatch - 1)
        else:
            return 0

def parse_cards(lines):
    cards = []
    for card in lines:
        number, card = card.split(":")
        number = int(number.strip("Card"))
        winning, present = card.split("|")
        winning = set(map(int, winning.split()))
        present = set(map(int, present.split()))
        cards.append(Card(number, winning, present))
    return cards

def day4_part1(filename):
    with open(filename) as f:
        l = f.readlines()

    cards = parse_cards(l)
    total_points = 0
    for card in cards:
        total_points += card.points()
    return total_points

def day4_part2(filename):
    with open(filename) as f:
        l = f.readlines()

    cards = parse_cards(l)
    card_stack = cards.copy()

    for card in card_stack:
        number = card.num
        nmatch = card.num_matched()
        winnings = []
        for i in range(nmatch):
            winnings.append(cards[number + i])
        card_stack.extend(winnings)
    return len(card_stack)

if __name__ == "__main__":
    print("Part 1 example", day4_part1("input/day4_example.txt"))
    print("Part 1", day4_part1("input/day4.txt"))
    print("Part 2 example", day4_part2("input/day4_example.txt"))
    print("Part 2", day4_part2("input/day4.txt"))

    

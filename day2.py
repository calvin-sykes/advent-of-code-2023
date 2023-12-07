colours = ["red", "green", "blue"]

class Game:
    def __init__(self, id, cube_sets):
        self.id = id
        self.cubes = cube_sets

    def is_possible(self, cube_counts):
        for cube_set in self.cubes:
            for c in cube_set:
                if cube_set[c] > cube_counts[c]:
                    return False
        return True

    def minimum_possible(self):
        minimum = {c: 0 for c in colours}
        for cube_set in self.cubes:
            for c in cube_set:
                minimum[c] = max(minimum[c], cube_set[c])
        return minimum

def parse_game(game_str):
    id_str, cubes_str = game_str.split(":")
    id_str = id_str.strip("Game")

    id = int(id_str)
    cube_set_strs = cubes_str.split(";")
    cube_sets = []
    for set_str in cube_set_strs:
        set_dict = {}
        count_strs = set_str.split(",")
        for count_str in count_strs:
            count, colour = count_str.split()
            set_dict[colour] = int(count)
        cube_sets.append(set_dict)
    return Game(id, cube_sets)

def cube_power(cube_set):
    power = 1
    for c in cube_set:
        power *= cube_set[c]
    return power

def day2_part1(filename):
    with open(filename) as f:
        l = f.readlines()

    games = list(map(parse_game, l))
    contents = {"red": 12, "green": 13, "blue": 14}
    possible_games = filter(lambda g: g.is_possible(contents), games)
    sum_possible_ids = sum(g.id for g in possible_games)
    return sum_possible_ids

def day2_part2(filename):
    with open(filename) as f:
        l = f.readlines()

    games = list(map(parse_game, l))    
    sum_power = sum(cube_power(g.minimum_possible()) for g in games)
    return sum_power

if __name__ == "__main__":
    print("Part 1 example", day2_part1("input/day2_example.txt"))
    print("Part 1", day2_part1("input/day2.txt"))
    print("Part 2 example", day2_part2("input/day2_example.txt"))
    print("Part 2", day2_part2("input/day2.txt"))

def distance(hold_time, race_time):
    return hold_time * (race_time - hold_time)

def solve_quad(a, b, c):
    disc = (b**2 - 4 * a * c)**0.5
    return [(-b + disc) / (2 * a), (-b - disc) / (2 * a)]

def day6_part1(filename):
    with open(filename) as f:
        l = f.readlines()

    times = list(map(int, l[0].split(":")[1].split()))
    distances = list(map(int, l[1].split(":")[1].split()))

    nwin_prod = 1
    for race_time, winning_dist in zip(times, distances):
        nwin = 0
        for hold_time in range(1, race_time):
            dist = distance(hold_time, race_time)
            if dist > winning_dist:
                nwin += 1
        nwin_prod *= nwin
    return nwin_prod

def day6_part2(filename):
    with open(filename) as f:
        l = f.readlines()

    race_time = int("".join(l[0].split(":")[1].split()))
    winning_dist = int("".join(l[1].split(":")[1].split()))

    # solving hold_time * (race_time - hold_time) = winning_dist
    # -hold_time**2 + race_time*hold_time - winning_dist = 0
    # quadratic with a=-1, b=race_time, c = -winning_dist
    min_win, max_win = solve_quad(-1, race_time, -winning_dist)
    # time must be integer between min_win and max_win
    # so round min up and max down
    # print(min_win, max_win)
    min_win = int(min_win + (1 - (min_win - int(min_win))))
    max_win = int(max_win - (max_win - int(max_win)))
    # print(min_win, max_win)

    # nwin = 0
    # for hold_time in range(1, race_time):
    #     dist = distance(hold_time, race_time)
    #     if dist > winning_dist:
    #         nwin += 1
    # assert nwin == (max_win - min_win + 1)
    return max_win - min_win + 1

if __name__ == "__main__":
    print("Part 1 example", day6_part1("input/day6_example.txt"))
    print("Part 1", day6_part1("input/day6.txt"))
    print("Part 2 example", day6_part2("input/day6_example.txt"))
    print("Part 2", day6_part2("input/day6.txt"))

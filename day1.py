def day1_part1(filename):
    with open(filename) as f:
        lines = f.readlines()

    result = 0
    for l in lines:
        nums = filter(lambda c: c.isdigit(), l)
        numstr = "".join(nums)
        num = int(numstr[0] + numstr[-1])
        result += num
    return result

def day1_part2(filename):
    with open(filename) as f:
        lines = f.readlines()

    digits = "0123456789"
    digit_words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    result = 0
    for l in lines:
        first_pos = len(l)
        last_pos = -1
        first_digit = ""
        last_digit = ""

        for digit in digits:
            if (pos := l.find(digit)) != -1 and pos < first_pos:
                first_pos = pos
                first_digit = digit
            if (pos := l.rfind(digit)) != -1 and pos > last_pos:
                last_pos = pos
                last_digit = digit

        for iword, word in enumerate(digit_words):
            if (pos := l.find(word)) != -1 and pos < first_pos:
                first_pos = pos
                first_digit = digits[iword]
            if (pos := l.rfind(word)) != -1 and pos > last_pos:
                last_pos = pos
                last_digit = digits[iword]

        num = int(first_digit + last_digit)
        result += num
    return result

if __name__ == "__main__":
    print("Part 1 example", day1_part1("input/day1_example.txt"))
    print("Part 1", day1_part1("input/day1.txt"))
    print("Part 2 example", day1_part2("input/day1_example_part2.txt"))
    print("Part 2", day1_part2("input/day1.txt"))

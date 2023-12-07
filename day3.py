def find_parts_symbols(engine_str):
    parts = []
    symbols = []

    start = 0
    current_number = None

    for i, c in enumerate(engine_str):
        if c.isdigit():
            if current_number:
                current_number += c
            else:
                start = i
                current_number = c
        else:
            if current_number:
                parts.append((current_number, start))
                current_number = None
            if c not in ".\n":
                symbols.append((c, i))
    return parts, symbols

def get_parts_symbols(engine):
    parts = []
    symbols = []
    for iline, l in enumerate(engine):
        pp, ss = find_parts_symbols(l)
        spos = [s[1] for s in ss]
        parts.append(pp)
        symbols.append(ss)
    return parts, symbols

def symbol_positions(ss):
    return [s[1] for s in ss]

def is_valid_part(p, i_p, spos_seq):
    valid = False
    for spos in spos_seq:
        valid |= any(map(lambda sp: (sp >= i_p - 1) and (sp <= i_p + len(p)), spos))
    return valid

def is_valid_gear(i_g, vp_seq):
    valid = 0
    parts = []
    for vpp in vp_seq:
        for (vp, vp_pos) in vpp:
            if (vp_pos >= i_g - len(vp)) and (vp_pos <= i_g + 1):
                valid += 1
                parts.append(int(vp))
    if valid == 2:
        ratio = parts[0] * parts[1]
        return True, ratio
    else:
        return False, None

def get_valid_parts(parts, symbols):
    valid_parts = []
    for iline, pp in enumerate(parts):
        spos_seq = [symbol_positions(symbols[iline])]
        if iline > 0:
            spos_seq.append(symbol_positions(symbols[iline-1]))
        if iline < len(parts) - 1:
            spos_seq.append(symbol_positions(symbols[iline+1]))
        valid_parts.append([(p, i_p) for (p, i_p) in pp if is_valid_part(p, i_p, spos_seq)])
    return valid_parts

def day3_part1(filename):
    with open(filename) as f:
        parts, symbols = get_parts_symbols(f.readlines())

    valid_parts = get_valid_parts(parts, symbols)
    sum_valid = sum(int(pp[0]) for pp_line in valid_parts for pp in pp_line)
    return sum_valid

def day3_part2(filename):
    with open(filename) as f:
        parts, symbols = get_parts_symbols(f.readlines())

    valid_parts = get_valid_parts(parts, symbols)
    valid_gears = []
    for iline, ss in enumerate(symbols):
        vp_seq = [valid_parts[iline]]
        if iline > 0:
            vp_seq.append(valid_parts[iline-1])
        if iline < len(parts) - 1:
            vp_seq.append(valid_parts[iline+1])
        for (s, i_s) in ss:
            if s != "*":
                continue
            valid, ratio = is_valid_gear(i_s, vp_seq)
            if valid:
                valid_gears.append(ratio)
    sum_gear_ratios = sum(valid_gears)
    return sum_gear_ratios

if __name__ == "__main__":
    print("Part 1 example", day3_part1("input/day3_example.txt"))
    print("Part 1", day3_part1("input/day3.txt"))
    print("Part 2 example", day3_part2("input/day3_example.txt"))
    print("Part 2", day3_part2("input/day3.txt"))

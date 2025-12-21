def solve_part1(input_text):
    """
    Part 1: Count how many times dial lands on 0 at END of rotations.
    """
    lines = input_text.strip().split('\n')
    position = 50
    zerocount = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        direction = line[0]
        distance = int(line[1:])
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
        if position == 0:
            zerocount += 1
    return zerocount


def solve_part2(input_text):
    """
    Part 2: Count EVERY click where dial points at 0 (during rotations too).
    For Left rotation from position P by D clicks:
      - We hit 0 at clicks: P, P+100, P+200, ... (if P > 0)
      - If P == 0, we hit at clicks: 100, 200, ...
    For Right rotation from position P by D clicks:
      - We hit 0 at clicks: (100-P), (200-P), ... (if P > 0)
      - If P == 0, we hit at clicks: 100, 200, ...
    """
    lines = input_text.strip().split('\n')
    position = 50
    zerocount = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        direction = line[0]
        distance = int(line[1:])        
        if direction == 'L':
            first_hit = position if position > 0 else 100
        else:  
            first_hit = (100 - position) if position > 0 else 100
        if distance >= first_hit:
            zerocount += (distance - first_hit) // 100 + 1
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
    return zerocount


with open('input1.txt', 'r') as f:
    puzzle_input = f.read()

print(f"{solve_part1(puzzle_input)}")
print(f"{solve_part2(puzzle_input)}")

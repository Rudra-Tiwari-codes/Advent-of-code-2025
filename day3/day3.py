def max_joltage_part1(bank):
    """
    Part 1: Find the maximum joltage by selecting exactly 2 batteries.
    """
    max_val = 0
    n = len(bank)
    
    for i in range(n):
        for j in range(i + 1, n):
            joltage = int(bank[i] + bank[j])
            max_val = max(max_val, joltage)
    
    return max_val


def max_joltage_part2(bank, num_digits=12):
    """
    Part 2: Find the maximum joltage by selecting exactly 12 batteries.
    Uses greedy algorithm: at each position, pick the largest digit
    that still leaves enough digits for remaining positions.
    """
    n = len(bank)
    if n < num_digits:
        return int(bank)  # Not enough digits
    
    result = []
    start_idx = 0
    
    for i in range(num_digits):
        # Need to leave (num_digits - i - 1) digits after this one
        remaining_needed = num_digits - i - 1
        end_idx = n - remaining_needed
        
        # Find the maximum digit in the valid range
        best_digit = '0'
        best_idx = start_idx
        
        for j in range(start_idx, end_idx):
            if bank[j] > best_digit:
                best_digit = bank[j]
                best_idx = j
        
        result.append(best_digit)
        start_idx = best_idx + 1
    
    return int(''.join(result))


def solve_part1(input_text):
    """Sum of maximum joltages (2 batteries) from all banks."""
    lines = input_text.strip().split('\n')
    total = 0
    
    for line in lines:
        line = line.strip()
        if line:
            total += max_joltage_part1(line)
    
    return total


def solve_part2(input_text):
    """Sum of maximum joltages (12 batteries) from all banks."""
    lines = input_text.strip().split('\n')
    total = 0
    
    for line in lines:
        line = line.strip()
        if line:
            total += max_joltage_part2(line)
    
    return total


# Read puzzle input from file
with open('input3.txt', 'r') as f:
    puzzle_input = f.read()

print(f"Part 1: {solve_part1(puzzle_input)}")
print(f"Part 2: {solve_part2(puzzle_input)}")

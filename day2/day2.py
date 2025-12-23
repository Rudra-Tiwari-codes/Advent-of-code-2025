def is_invalid_part1(n):
    """Part 1: Check if number is a pattern repeated exactly twice."""
    s = str(n)
    if len(s) % 2 != 0:
        return False
    half = len(s) // 2
    return s[:half] == s[half:]

def is_invalid_part2(n):
    """Part 2: Check if number is a pattern repeated 2+ times."""
    s = str(n)
    length = len(s)
    # Try each possible pattern length (from 1 to length//2)
    for pat_len in range(1, length // 2 + 1):
        if length % pat_len == 0:
            pattern = s[:pat_len]
            repetitions = length // pat_len
            if repetitions >= 2 and pattern * repetitions == s:
                return True
    return False

def find_invalid_ids_in_range(start, end, part2=False):
    """
    Find all invalid IDs in the given range [start, end].
    """
    invalid_ids = set()
    max_len = len(str(end))
    
    # For each possible pattern length
    for pat_len in range(1, max_len + 1):
        # For each possible number of repetition
        max_reps = max_len // pat_len if pat_len > 0 else 0
        min_reps = 2
        
        if not part2:
            max_reps = 2  #exactly 2 repetitions
        
        for reps in range(min_reps, max_reps + 1):
            result_len = pat_len * reps
            if result_len > max_len + 1:
                break
                
            # Generate patterns
            pattern_start = 10 ** (pat_len - 1) if pat_len > 1 else 1
            pattern_end = 10 ** pat_len - 1      
            for pattern in range(pattern_start, pattern_end + 1):
                invalid_id = int(str(pattern) * reps)        
                if start <= invalid_id <= end:
                    invalid_ids.add(invalid_id)
    return list(invalid_ids)


def solve(input_text, part2=False):
    """Parse ranges and sum all invalid IDs."""
    ranges = input_text.strip().split(',')
    total = 0
    all_invalid = set()
    
    for r in ranges:
        r = r.strip()
        if not r:
            continue
        start, end = map(int, r.split('-'))
        invalid_ids = find_invalid_ids_in_range(start, end, part2=part2)
        all_invalid.update(invalid_ids)
        total += sum(invalid_ids)
    
    # Return sum of unique IDs (to avoid double counting)
    return sum(all_invalid), list(all_invalid)

# Read puzzle input from file
with open('input2.txt', 'r') as f:
    puzzle_input = f.read(
result1, _ = solve(puzzle_input, part2=False)
result2, _ = solve(puzzle_input, part2=True)
print(f"Part 1: {result1}")
print(f"Part 2: {result2}")

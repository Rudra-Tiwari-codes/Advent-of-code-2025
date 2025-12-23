def parse_input(input_text):
    """Parse the database into ranges and ingredient IDs."""
    parts = input_text.strip().split('\n\n')
    
    # Parse ranges
    ranges = []
    for line in parts[0].strip().split('\n'):
        if '-' in line:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))
    
    ingredients = []
    if len(parts) > 1:
        for line in parts[1].strip().split('\n'):
            if line.strip():
                ingredients.append(int(line.strip()))
    
    return ranges, ingredients


def is_fresh(ingredient_id, ranges):
    """Check if an ingredient ID is fresh (falls within any range)."""
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def merge_ranges(ranges):
    """Merge overlapping ranges and return non-overlapping ranges."""
    if not ranges:
        return []
    
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged = [sorted_ranges[0]]
    
    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    
    return merged


def solve_part1(input_text):
    """Count how many available ingredient IDs are fresh."""
    ranges, ingredients = parse_input(input_text)
    count = sum(1 for ing in ingredients if is_fresh(ing, ranges))
    return count


def solve_part2(input_text):
    """Count total unique fresh ingredient IDs across all ranges."""
    ranges, _ = parse_input(input_text)
    merged = merge_ranges(ranges)
    
    total = sum(end - start + 1 for start, end in merged)
    return total


with open('input5.txt', 'r') as f:
    puzzle_input = f.read()

print(f"Part 1: {solve_part1(puzzle_input)}")
print(f"Part 2: {solve_part2(puzzle_input)}")

def count_adjacent_rolls(grid, row, col):
    """Count how many paper rolls are in the 8 adjacent positions."""
    count = 0
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Check all 8 directions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == '@':
                    count += 1
    
    return count


def find_accessible_rolls(grid):
    """Find all rolls that can be accessed (fewer than 4 adjacent rolls)."""
    accessible = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@':
                adjacent = count_adjacent_rolls(grid, row, col)
                if adjacent < 4:
                    accessible.append((row, col))
    return accessible


def solve_part1(input_text):
    """
    Count rolls that can be accessed by a forklift.
    A roll is accessible if it has fewer than 4 adjacent rolls.
    """
    grid = [list(line.strip()) for line in input_text.strip().split('\n') if line.strip()]
    return len(find_accessible_rolls(grid))


def solve_part2(input_text):
    """
    Simulate removing accessible rolls until no more can be removed.
    Count total rolls removed.
    """
    grid = [list(line.strip()) for line in input_text.strip().split('\n') if line.strip()]
    total_removed = 0
    
    while True:
        accessible = find_accessible_rolls(grid)
        if not accessible:
            break
        
        # Remove all accessible rolls
        for row, col in accessible:
            grid[row][col] = '.'
        
        total_removed += len(accessible)
    
    return total_removed


# Read puzzle input from file
with open('input4.txt', 'r') as f:
    puzzle_input = f.read()

print(f"Part 1: {solve_part1(puzzle_input)}")
print(f"Part 2: {solve_part2(puzzle_input)}")

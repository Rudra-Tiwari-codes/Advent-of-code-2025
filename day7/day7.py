def solve_part1(input_text):
    """
    Simulate tachyon beams and count total splits.
    Beams move downward. When hitting ^, the beam splits into left and right.
    """
    lines = input_text.strip().split('\n')
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Find starting position S
    start_col = None
    for col in range(cols):
        if grid[0][col] == 'S':
            start_col = col
            break
    
    if start_col is None:
        return 0
    
    # Track active beams as (row, col) - all moving downward
    beams = {(0, start_col)}
    split_count = 0
    current_row = 0
    
    while beams and current_row < rows - 1:
        next_row = current_row + 1
        new_beams = set()
        
        for row, col in beams:
            if row == current_row:
                if next_row < rows and 0 <= col < len(grid[next_row]):
                    cell = grid[next_row][col]
                    
                    if cell == '^':
                        split_count += 1
                        if col - 1 >= 0:
                            new_beams.add((next_row, col - 1))
                        if col + 1 < cols:
                            new_beams.add((next_row, col + 1))
                    elif cell == '.' or cell == 'S':
                        new_beams.add((next_row, col))
        
        beams = new_beams
        current_row = next_row
    
    return split_count


def solve_part2(input_text):
    """
    Count total timelines (many-worlds interpretation).
    Each split doubles the timeline for that particle.
    Track how many timelines are at each position.
    """
    lines = input_text.strip().split('\n')
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Find starting position S
    start_col = None
    for col in range(cols):
        if grid[0][col] == 'S':
            start_col = col
            break
    
    if start_col is None:
        return 0
    
    # Track number of timelines at each position: {col: timeline_count}
    # Start with 1 timeline at the starting column
    timelines = {start_col: 1}
    current_row = 0
    
    while timelines and current_row < rows - 1:
        next_row = current_row + 1
        new_timelines = {}
        
        for col, count in timelines.items():
            if next_row < rows and 0 <= col < len(grid[next_row]):
                cell = grid[next_row][col]
                
                if cell == '^':
                    # Each timeline splits into two
                    if col - 1 >= 0:
                        new_timelines[col - 1] = new_timelines.get(col - 1, 0) + count
                    if col + 1 < cols:
                        new_timelines[col + 1] = new_timelines.get(col + 1, 0) + count
                elif cell == '.' or cell == 'S':
                    # Timeline continues
                    new_timelines[col] = new_timelines.get(col, 0) + count
        
        timelines = new_timelines
        current_row = next_row
    
    # Total timelines is sum of all timeline counts
    return sum(timelines.values())


# Read puzzle input from file
with open('input7.txt', 'r') as f:
    puzzle_input = f.read()

print(f"Part 1: {solve_part1(puzzle_input)}")
print(f"Part 2: {solve_part2(puzzle_input)}")

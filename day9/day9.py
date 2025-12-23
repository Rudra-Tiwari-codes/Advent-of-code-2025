import sys
sys.setrecursionlimit(100000)

def parse_input(input_text):
    """Parse red tile coordinates."""
    tiles = []
    for line in input_text.strip().split('\n'):
        line = line.strip().rstrip('.')
        if line and ',' in line:
            parts = line.split(',')
            x, y = int(parts[0]), int(parts[1])
            tiles.append((x, y))
    return tiles


def solve_part1(input_text):
    """Find the largest rectangle area using two red tiles as opposite corners."""
    tiles = parse_input(input_text)
    n = len(tiles)
    
    max_area = 0
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            max_area = max(max_area, area)
    
    return max_area


def solve_part2(input_text):
    """Find largest rectangle using only red/green tiles."""
    red_tiles = parse_input(input_text)
    n = len(red_tiles)
    
    # Build the polygon boundary (edges between consecutive red tiles)
    # For each row y, find the min and max x values that are inside/on the polygon
    
    # First, collect all edges
    edges = []
    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]
        edges.append(((x1, y1), (x2, y2)))
    
    # Find all unique y values
    all_y = set()
    for (x1, y1), (x2, y2) in edges:
        all_y.add(y1)
        all_y.add(y2)
        if y1 != y2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                all_y.add(y)
    
    # For each row, find the coverage (min_x, max_x) of colored tiles
    row_coverage = {}
    
    for y in all_y:
        x_values = set()
        
        # Find all x values at this y from edges
        for (x1, y1), (x2, y2) in edges:
            if y1 == y2 == y:  # Horizontal edge at this y
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    x_values.add(x)
            elif y1 != y2:  # Vertical edge
                if min(y1, y2) <= y <= max(y1, y2):
                    x_values.add(x1)  # x1 == x2 for vertical edge
        
        if x_values:
            row_coverage[y] = (min(x_values), max(x_values))
    
    # For a rectangle to be valid, for every row in the rectangle,
    # the entire row segment [min_x, max_x] of the rectangle must be covered
    
    max_area = 0
    red_set = set(red_tiles)
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            
            rect_min_x, rect_max_x = min(x1, x2), max(x1, x2)
            rect_min_y, rect_max_y = min(y1, y2), max(y1, y2)
            
            # Check if rectangle is valid (all rows fully covered)
            valid = True
            for y in range(rect_min_y, rect_max_y + 1):
                if y not in row_coverage:
                    valid = False
                    break
                cov_min, cov_max = row_coverage[y]
                if cov_min > rect_min_x or cov_max < rect_max_x:
                    valid = False
                    break
            
            if valid:
                width = rect_max_x - rect_min_x + 1
                height = rect_max_y - rect_min_y + 1
                area = width * height
                max_area = max(max_area, area)
    
    return max_area


# Read puzzle input from file
with open('input9.txt', 'r') as f:
    puzzle_input = f.read()

print(f"Part 1: {solve_part1(puzzle_input)}")
print(f"Part 2: {solve_part2(puzzle_input)}")

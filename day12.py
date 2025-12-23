import re

def parse_input(input_text):
    """Parse shapes and regions from input."""
    shapes = {}
    regions = []
    lines = input_text.strip().split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        match = re.match(r'^(\d+):$', line)
        if match:
            shape_idx = int(match.group(1))
            shape_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^\d+x\d+:', lines[i].strip()) and not re.match(r'^\d+:$', lines[i].strip()):
                shape_lines.append(lines[i].rstrip())
                i += 1
            # Count cells in shape
            cells = sum(1 for row in shape_lines for c in row if c == '#')
            shapes[shape_idx] = cells
            continue
        
        match = re.match(r'^(\d+)x(\d+):\s*(.+)$', line.rstrip('.'))
        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            quantities = [int(x) for x in match.group(3).split()]
            regions.append((width, height, quantities))
        
        i += 1
    
    return shapes, regions


def solve(input_text):
    """Count regions where presents can fit based on area matching."""
    shapes, regions = parse_input(input_text)
    
    count = 0
    for width, height, quantities in regions:
        area = width * height
        used = sum(qty * shapes.get(idx, 0) for idx, qty in enumerate(quantities))
        
        if used <= area:
            count += 1
    return count


with open('input12.txt', 'r') as f:
    puzzle_input = f.read()

print(f"Part 1: {solve(puzzle_input)}")

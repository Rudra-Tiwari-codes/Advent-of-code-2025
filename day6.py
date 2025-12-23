def parse_worksheet_part1(input_text):
    """
    Part 1: Parse numbers row-wise within each problem.
    """
    lines = input_text.rstrip('\n').split('\n')
    max_width = max(len(line) for line in lines)
    lines = [line.ljust(max_width) for line in lines]
    
    ops_line = lines[-1]
    number_lines = lines[:-1]
    
    ops = []
    for i, c in enumerate(ops_line):
        if c in '+*':
            ops.append((i, c))
    
    results = []
    for op_pos, op in ops:
        # Find problem boundaries
        start = op_pos
        while start > 0:
            if all(line[start-1] == ' ' for line in number_lines):
                break
            start -= 1
        
        end = op_pos + 1
        while end < max_width:
            if all(line[end] == ' ' for line in number_lines):
                break
            end += 1
        
        numbers = []
        for line in number_lines:
            segment = line[start:end].strip()
            if segment:
                try:
                    numbers.append(int(segment))
                except ValueError:
                    pass
        
        if numbers:
            results.append((numbers, op))
    
    return results


def parse_worksheet_part2(input_text):
    """
    Part 2: Parse numbers column-wise (each column is a number, 
    reading top-to-bottom for digits, right-to-left for column order).
    """
    lines = input_text.rstrip('\n').split('\n')
    max_width = max(len(line) for line in lines)
    lines = [line.ljust(max_width) for line in lines]
    
    ops_line = lines[-1]
    number_lines = lines[:-1]
    
    ops = []
    for i, c in enumerate(ops_line):
        if c in '+*':
            ops.append((i, c))
    
    results = []
    for op_pos, op in ops:
        start = op_pos
        while start > 0:
            if all(line[start-1] == ' ' for line in number_lines):
                break
            start -= 1
        
        end = op_pos + 1
        while end < max_width:
            if all(line[end] == ' ' for line in number_lines):
                break
            end += 1
        
        numbers = []
        for col in range(start, end):
            digits = []
            for line in number_lines:
                c = line[col]
                if c.isdigit():
                    digits.append(c)
            
            if digits:
                number = int(''.join(digits))
                numbers.append(number)
        
        if numbers:
            results.append((numbers, op))
    
    return results


def solve_problem(numbers, op):
    """Solve a single math problem."""
    if op == '+':
        return sum(numbers)
    else:  # op == '*'
        result = 1
        for n in numbers:
            result *= n
        return result


def solve_part1(input_text):
    """Solve all problems (row-wise numbers)."""
    problems = parse_worksheet_part1(input_text)
    total = 0
    for numbers, op in problems:
        total += solve_problem(numbers, op)
    return total


def solve_part2(input_text):
    """Solve all problems (column-wise numbers)."""
    problems = parse_worksheet_part2(input_text)
    total = 0
    for numbers, op in problems:
        total += solve_problem(numbers, op)
    return total


with open('input6.txt', 'r') as f:
    puzzle_input = f.read()

print(f"Part 1: {solve_part1(puzzle_input)}")
print(f"Part 2: {solve_part2(puzzle_input)}")

import re
from itertools import combinations
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
import numpy as np

def parse_line(line):
    """Parse a machine specification line."""
    line = line.strip().rstrip('.')
    if not line:
        return None
    
    # Extract indicator diagram [...]
    diagram_match = re.search(r'\[([.#]+)\]', line)
    if not diagram_match:
        return None
    diagram = diagram_match.group(1)
    
    # Extract button schematics (...)
    buttons = []
    for match in re.finditer(r'\(([0-9,]+)\)', line):
        indices = [int(x) for x in match.group(1).split(',')]
        buttons.append(indices)
    
    # Extract joltage requirements {...}
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage = []
    if joltage_match:
        joltage = [int(x) for x in joltage_match.group(1).split(',')]
    
    # Target state from diagram
    target = [1 if c == '#' else 0 for c in diagram]
    
    return target, buttons, joltage


def apply_buttons(n_lights, buttons, pressed):
    """Apply button presses and return resulting state."""
    state = [0] * n_lights
    for i, btn in enumerate(buttons):
        if pressed[i]:
            for idx in btn:
                if idx < n_lights:
                    state[idx] ^= 1
    return state


def solve_machine_part1(target, buttons):
    """Find minimum button presses to achieve target state (XOR mode)."""
    n_lights = len(target)
    n_buttons = len(buttons)
    
    min_presses = float('inf')
    
    for num_pressed in range(n_buttons + 1):
        if num_pressed >= min_presses:
            break
        for combo in combinations(range(n_buttons), num_pressed):
            pressed = [0] * n_buttons
            for i in combo:
                pressed[i] = 1
            
            state = apply_buttons(n_lights, buttons, pressed)
            if state == target:
                min_presses = min(min_presses, num_pressed)
                break
        
        if min_presses <= num_pressed:
            break
    
    return min_presses if min_presses != float('inf') else 0


def solve_machine_part2(buttons, joltage):
    """Find minimum button presses to achieve joltage targets (additive mode)."""
    n_counters = len(joltage)
    n_buttons = len(buttons)
    
    if n_buttons == 0:
        return 0 if all(j == 0 for j in joltage) else float('inf')
    
    # Build the constraint matrix A where A[i][j] = 1 if button j affects counter i
    A = np.zeros((n_counters, n_buttons))
    for j, btn in enumerate(buttons):
        for idx in btn:
            if idx < n_counters:
                A[idx][j] = 1
    
    b = np.array(joltage, dtype=float)
    
    # Minimize sum of x (button presses) subject to A @ x = b, x >= 0
    c = np.ones(n_buttons)  # Minimize total presses
    
    # Use integer linear programming
    try:
        from scipy.optimize import milp, LinearConstraint, Bounds
        
        constraints = LinearConstraint(A, b, b)
        integrality = np.ones(n_buttons)  # All variables are integers
        bounds = Bounds(0, np.inf)
        
        result = milp(c, constraints=constraints, integrality=integrality, bounds=bounds)
        
        if result.success:
            return int(round(sum(result.x)))
        else:
            return 0
    except:
        # Fallback: try non-negative least squares
        from scipy.optimize import nnls
        x, _ = nnls(A, b)
        x = np.round(x).astype(int)
        if np.allclose(A @ x, b):
            return int(sum(x))
        return 0


def solve_part1(input_text):
    """Sum of minimum button presses for all machines (Part 1)."""
    total = 0
    for line in input_text.strip().split('\n'):
        result = parse_line(line)
        if result:
            target, buttons, _ = result
            presses = solve_machine_part1(target, buttons)
            total += presses
    return total


def solve_part2(input_text):
    """Sum of minimum button presses for all machines (Part 2)."""
    total = 0
    for line in input_text.strip().split('\n'):
        result = parse_line(line)
        if result:
            _, buttons, joltage = result
            presses = solve_machine_part2(buttons, joltage)
            total += presses
    return total


# Read puzzle input from file
with open('input10.txt', 'r') as f:
    puzzle_input = f.read()

print(f"Part 1: {solve_part1(puzzle_input)}")
print(f"Part 2: {solve_part2(puzzle_input)}")

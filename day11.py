from functools import lru_cache

def parse_input(input_text):
    """Parse device connections into a graph."""
    graph = {}
    for line in input_text.strip().split('\n'):
        line = line.strip().rstrip('.')
        if ':' not in line:
            continue
        parts = line.split(':')
        device = parts[0].strip()
        outputs = parts[1].strip().split()
        graph[device] = outputs
    return graph


def count_paths(graph, start, end):
    """Count all paths from start to end using memoization."""
    memo = {}
    
    def dfs(node):
        if node == end:
            return 1
        if node not in graph:
            return 0
        if node in memo:
            return memo[node]
        
        total = 0
        for next_node in graph[node]:
            total += dfs(next_node)
        
        memo[node] = total
        return total
    
    return dfs(start)


def count_paths_through_both(graph, start, end, required1, required2):
    """Count paths from start to end that pass through both required nodes."""
    # Use state-based memoization: (node, visited_req1, visited_req2)
    memo = {}
    
    def dfs(node, has_req1, has_req2):
        # Update flags if we're at a required node
        if node == required1:
            has_req1 = True
        if node == required2:
            has_req2 = True
        
        if node == end:
            return 1 if (has_req1 and has_req2) else 0
        if node not in graph:
            return 0
        
        state = (node, has_req1, has_req2)
        if state in memo:
            return memo[state]
        
        total = 0
        for next_node in graph[node]:
            total += dfs(next_node, has_req1, has_req2)
        
        memo[state] = total
        return total
    
    return dfs(start, False, False)


def solve_part1(input_text):
    """Count all paths from 'you' to 'out'."""
    graph = parse_input(input_text)
    return count_paths(graph, 'you', 'out')


def solve_part2(input_text):
    """Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'."""
    graph = parse_input(input_text)
    return count_paths_through_both(graph, 'svr', 'out', 'dac', 'fft')


# Read puzzle input from file
with open('input11.txt', 'r') as f:
    puzzle_input = f.read()

print(f"Part 1: {solve_part1(puzzle_input)}")
print(f"Part 2: {solve_part2(puzzle_input)}")

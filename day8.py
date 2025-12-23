import math
from collections import defaultdict

def parse_input(input_text):
    """Parse junction box coordinates."""
    boxes = []
    for line in input_text.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith('.'):
            parts = line.rstrip('.').split(',')
            if len(parts) == 3:
                x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
                boxes.append((x, y, z))
    return boxes


def distance(p1, p2):
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)


class UnionFind:
    """Union-Find data structure for tracking circuits."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.num_components = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already in same circuit
        
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.num_components -= 1
        return True
    
    def get_circuit_sizes(self):
        """Get sizes of all circuits."""
        sizes = []
        for i in range(len(self.parent)):
            if self.find(i) == i:
                sizes.append(self.size[i])
        return sorted(sizes, reverse=True)


def solve_part1(input_text):
    """Connect 1000 closest pairs and find product of 3 largest circuit sizes."""
    boxes = parse_input(input_text)
    n = len(boxes)
    
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(boxes[i], boxes[j])
            pairs.append((d, i, j))
    
    pairs.sort()
    
    uf = UnionFind(n)
    for k in range(min(1000, len(pairs))):
        _, i, j = pairs[k]
        uf.union(i, j)
    
    sizes = uf.get_circuit_sizes()
    result = 1
    for i in range(min(3, len(sizes))):
        result *= sizes[i]
    
    return result


def solve_part2(input_text):
    """Find the last connection that unifies all into one circuit."""
    boxes = parse_input(input_text)
    n = len(boxes)
    
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(boxes[i], boxes[j])
            pairs.append((d, i, j))
    
    pairs.sort()
    
    uf = UnionFind(n)
    for d, i, j in pairs:
        if uf.union(i, j):
            if uf.num_components == 1:
                # This was the last connection!
                return boxes[i][0] * boxes[j][0]
    
    return 0


# Read puzzle input from file
with open('input8.txt', 'r') as f:
    puzzle_input = f.read()

print(f"Part 1: {solve_part1(puzzle_input)}")
print(f"Part 2: {solve_part2(puzzle_input)}")

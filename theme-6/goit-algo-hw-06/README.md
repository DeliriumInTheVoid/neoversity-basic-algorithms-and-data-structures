# Graph Path Finding: BFS vs DFS Comparison

## Overview

This HW implements and compares two fundamental graph traversal algorithms - **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** - for finding paths in a transportation network graph.

## Task Description

The goal is to:
1. Use BFS and DFS algorithms to find paths in a generated transportation network graph
2. Compare the results of both algorithms
3. Explain the differences in the paths obtained
4. Analyze why each algorithm produces its specific results

## Algorithms Implemented

### 1. Breadth-First Search (BFS)

**How it works:**
- Uses a **queue** (FIFO - First In, First Out)
- Explores all neighbors at the current depth level before moving to the next level
- Marks nodes as visited when they are added to the queue

### 2. Depth-First Search (DFS)

**How it works:**
- Uses **recursion** (implicit stack - LIFO - Last In, First Out)
- Explores as far as possible along each branch before backtracking
- Marks nodes as visited when first encountered

## Comparison Results

### Key Differences

| Aspect                   | BFS                                        | DFS                              |
|--------------------------|--------------------------------------------|----------------------------------|
| **Data Structure**       | Queue (FIFO)                               | Stack/Recursion (LIFO)           |
| **Path Quality**         | Always finds shortest path                 | May find longer path             |
| **Memory Usage**         | Higher (stores all nodes at current level) | Lower (stores only current path) |
| **Exploration Strategy** | Level by level (breadth-wise)              | Branch by branch (depth-wise)    |
| **Time Complexity**      | O(V + E)                                   | O(V + E)                         |
| **Space Complexity**     | O(V)                                       | O(h) where h is max depth        |

### Why Paths Differ

1. **BFS Guarantees Shortest Path**
   - BFS explores nodes in order of their distance from the start
   - First time it reaches the goal, it has found the shortest path
   - Example: If there's a path of length 2 and a path of length 4, BFS will always find the path of length 2

2. **DFS May Find Longer Paths**
   - DFS follows one branch completely before trying another
   - The path it finds depends on the order of neighbors (often alphabetical or insertion order)
   - May explore a long winding path before finding a shorter alternative
   - Example: DFS might follow Station_1 → Station_2 → Station_3 → Station_4 → Station_5 even if Station_1 → Station_5 exists

### Practical Example

Consider a simple graph:
```
Station_1 --- Station_2 --- Station_5
    |                           |
Station_3 --- Station_4 --------+
```

**Searching from Station_1 to Station_5:**

- **BFS Result**: `Station_1 → Station_2 → Station_5` (2 connections)
  - Level 0: Station_1
  - Level 1: Station_2, Station_3
  - Level 2: Station_5 ✓ (shortest path found!)

- **DFS Result** (if neighbors are ordered): `Station_1 → Station_3 → Station_4 → Station_5` (3 connections)
  - Explores: Station_1 → Station_3 → Station_4 → Station_5 ✓ (first valid path found)
  - Never backtracks to try Station_1 → Station_2 → Station_5 because goal was already reached

## When to Use Each Algorithm

### Use BFS When:
- ✓ Finding the shortest path is critical
- ✓ The solution is likely to be close to the start
- ✓ Memory is not a significant constraint
- ✓ All edges have equal weight/cost

### Use DFS When:
- ✓ Memory is limited
- ✓ You need to explore all possible paths
- ✓ The solution is likely to be deep in the graph
- ✓ Checking connectivity or finding cycles

## Conclusions

1. **BFS is optimal for shortest path finding** in unweighted graphs because it systematically explores nodes level by level
2. **DFS is more memory-efficient** but doesn't guarantee the shortest path - it finds *a* path, not necessarily the *best* path
3. **Both algorithms have the same time complexity** O(V + E), but their space complexity and path quality differ significantly
4. **The choice of algorithm** depends on your specific requirements: shortest path (BFS) vs. memory efficiency (DFS)
5. **In transportation networks**, BFS is generally preferred as users typically want the route with the fewest transfers/stops

The program will:
- Generate a random transportation network (with fixed seed for reproducibility)
- Display graph statistics and edge connections
- Find paths using both BFS and DFS
- Compare and analyze the results

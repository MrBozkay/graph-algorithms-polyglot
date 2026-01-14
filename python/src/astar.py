"""A* Search Algorithm Implementation

A* is an informed search algorithm that uses heuristics to find the shortest path
more efficiently than Dijkstra's algorithm.

Time Complexity: O(E) in the worst case, but typically much faster with good heuristics
Space Complexity: O(V)
"""

import heapq
from typing import Dict, List, Tuple, Optional, Callable, Set, TypeVar

T = TypeVar('T')


def astar_search(
    graph: Dict[T, Dict[T, float]],
    start: T,
    goal: T,
    heuristic: Callable[[T, T], float]
) -> Tuple[float, List[T]]:
    """
    A* search algorithm for finding the shortest path using a heuristic.
    
    Args:
        graph: Adjacency list representation {node: {neighbor: weight}}
        start: Starting node
        goal: Goal node
        heuristic: Function h(node, goal) estimating distance to goal
                   Must be admissible (never overestimate) for optimal results
        
    Returns:
        Tuple of (distance, path)
        - distance: Actual shortest distance from start to goal
        - path: List of nodes in the shortest path
        
    Raises:
        ValueError: If no path exists between start and goal
        
    Example:
        >>> # Manhattan distance heuristic for grid
        >>> def manhattan(pos1, pos2):
        ...     return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        >>> graph = {(0,0): {(0,1): 1, (1,0): 1}, ...}
        >>> distance, path = astar_search(graph, (0,0), (5,5), manhattan)
    """
    # g_score: actual distance from start
    g_score: Dict[T, float] = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    # f_score: g_score + heuristic (estimated total distance)
    f_score: Dict[T, float] = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)
    
    # Track predecessors for path reconstruction
    predecessors: Dict[T, Optional[T]] = {node: None for node in graph}
    
    # Priority queue: (f_score, g_score, node)
    # We include g_score as tiebreaker for nodes with same f_score
    pq: List[Tuple[float, float, T]] = [(f_score[start], 0, start)]
    
    # Closed set: nodes already evaluated
    closed_set: Set[T] = set()
    
    while pq:
        current_f, current_g, current = heapq.heappop(pq)
        
        # Goal reached!
        if current == goal:
            path = _reconstruct_path(predecessors, current)
            return g_score[goal], path
        
        # Skip if already evaluated
        if current in closed_set:
            continue
        
        closed_set.add(current)
        
        # Explore neighbors
        if current not in graph:
            continue
            
        for neighbor, weight in graph[current].items():
            if neighbor in closed_set:
                continue
            
            # Calculate tentative g_score
            tentative_g = g_score[current] + weight
            
            # If this path is better than any previous one
            if tentative_g < g_score[neighbor]:
                # Update path
                predecessors[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                
                # Add to priority queue
                heapq.heappush(pq, (f_score[neighbor], tentative_g, neighbor))
    
    # No path found
    raise ValueError(f"No path exists from {start} to {goal}")


def _reconstruct_path(predecessors: Dict[T, Optional[T]], current: T) -> List[T]:
    """Reconstruct path from predecessors dictionary."""
    path: List[T] = []
    node: Optional[T] = current
    
    while node is not None:
        path.append(node)
        node = predecessors[node]
    
    path.reverse()
    return path


def astar_grid_search(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    allow_diagonal: bool = False
) -> Tuple[float, List[Tuple[int, int]]]:
    """
    A* search specialized for 2D grids.
    
    Args:
        grid: 2D grid where 0 = passable, 1 = obstacle
        start: Starting position (row, col)
        goal: Goal position (row, col)
        allow_diagonal: Whether diagonal movement is allowed
        
    Returns:
        Tuple of (distance, path)
        
    Example:
        >>> grid = [
        ...     [0, 0, 0, 0],
        ...     [0, 1, 1, 0],
        ...     [0, 0, 0, 0]
        ... ]
        >>> distance, path = astar_grid_search(grid, (0, 0), (2, 3))
    """
    rows, cols = len(grid), len(grid[0])
    
    # Build graph from grid
    graph: Dict[Tuple[int, int], Dict[Tuple[int, int], float]] = {}
    
    # Define movement directions
    if allow_diagonal:
        # 8 directions (including diagonals)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        # Diagonal moves cost sqrt(2) ≈ 1.414
        costs = [1.414, 1, 1.414, 1, 1, 1.414, 1, 1.414]
    else:
        # 4 directions (cardinal only)
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        costs = [1, 1, 1, 1]
    
    # Build adjacency list
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:  # Skip obstacles
                continue
            
            if (r, c) not in graph:
                graph[(r, c)] = {}
            
            for (dr, dc), cost in zip(directions, costs):
                nr, nc = r + dr, c + dc
                
                # Check bounds and obstacles
                if (0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0):
                    graph[(r, c)][(nr, nc)] = cost
    
    # Manhattan distance heuristic
    def manhattan(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    # Euclidean distance heuristic (better for diagonal movement)
    def euclidean(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    
    heuristic = euclidean if allow_diagonal else manhattan
    
    return astar_search(graph, start, goal, heuristic)

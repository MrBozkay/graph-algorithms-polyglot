"""Breadth-First Search (BFS) Implementation

BFS is used for finding shortest paths in unweighted graphs.
It's a special case of Dijkstra's algorithm where all edge weights are 1.

Time Complexity: O(V + E)
Space Complexity: O(V)
"""

from collections import deque
from typing import Dict, List, Optional, Set, Tuple, TypeVar

T = TypeVar('T')


def bfs(graph: Dict[T, List[T]], start: T) -> Dict[T, int]:
    """
    Breadth-First Search to find shortest distances in an unweighted graph.
    
    Args:
        graph: Adjacency list representation {node: [neighbors]}
        start: Starting node
        
    Returns:
        Dict mapping each reachable node to its distance from start
        
    Example:
        >>> graph = {
        ...     'A': ['B', 'C'],
        ...     'B': ['D'],
        ...     'C': ['D', 'E'],
        ...     'D': ['E'],
        ...     'E': []
        ... }
        >>> distances = bfs(graph, 'A')
        >>> distances['E']
        2
    """
    distances: Dict[T, int] = {start: 0}
    queue: deque[T] = deque([start])
    
    while queue:
        current = queue.popleft()
        current_distance = distances[current]
        
        for neighbor in graph.get(current, []):
            if neighbor not in distances:
                distances[neighbor] = current_distance + 1
                queue.append(neighbor)
    
    return distances


def bfs_shortest_path(
    graph: Dict[T, List[T]], 
    start: T, 
    end: T
) -> Tuple[int, List[T]]:
    """
    Find the shortest path between two nodes in an unweighted graph.
    
    Args:
        graph: Adjacency list representation
        start: Starting node
        end: Target node
        
    Returns:
        Tuple of (distance, path)
        - distance: Number of edges in the shortest path
        - path: List of nodes in the shortest path
        
    Raises:
        ValueError: If no path exists between start and end
        
    Example:
        >>> graph = {'A': ['B'], 'B': ['C'], 'C': []}
        >>> distance, path = bfs_shortest_path(graph, 'A', 'C')
        >>> path
        ['A', 'B', 'C']
    """
    if start == end:
        return 0, [start]
    
    distances: Dict[T, int] = {start: 0}
    predecessors: Dict[T, Optional[T]] = {start: None}
    queue: deque[T] = deque([start])
    
    while queue:
        current = queue.popleft()
        
        # Early exit if we found the target
        if current == end:
            break
        
        current_distance = distances[current]
        
        for neighbor in graph.get(current, []):
            if neighbor not in distances:
                distances[neighbor] = current_distance + 1
                predecessors[neighbor] = current
                queue.append(neighbor)
    
    # Check if path exists
    if end not in distances:
        raise ValueError(f"No path exists from {start} to {end}")
    
    # Reconstruct path
    path: List[T] = []
    current_node: Optional[T] = end
    
    while current_node is not None:
        path.append(current_node)
        current_node = predecessors[current_node]
    
    path.reverse()
    
    return distances[end], path


def bfs_all_paths(
    graph: Dict[T, List[T]], 
    start: T, 
    end: T,
    max_paths: int = 10
) -> List[List[T]]:
    """
    Find all shortest paths between two nodes (up to max_paths).
    
    Args:
        graph: Adjacency list representation
        start: Starting node
        end: Target node
        max_paths: Maximum number of paths to return
        
    Returns:
        List of paths, where each path is a list of nodes
        
    Example:
        >>> graph = {
        ...     'A': ['B', 'C'],
        ...     'B': ['D'],
        ...     'C': ['D'],
        ...     'D': []
        ... }
        >>> paths = bfs_all_paths(graph, 'A', 'D')
        >>> len(paths)
        2
    """
    if start == end:
        return [[start]]
    
    # First, find the shortest distance
    distances: Dict[T, int] = {start: 0}
    queue: deque[T] = deque([start])
    
    while queue and end not in distances:
        current = queue.popleft()
        current_distance = distances[current]
        
        for neighbor in graph.get(current, []):
            if neighbor not in distances:
                distances[neighbor] = current_distance + 1
                queue.append(neighbor)
    
    if end not in distances:
        return []
    
    target_distance = distances[end]
    
    # Now find all paths of that length
    paths: List[List[T]] = []
    path_queue: deque[Tuple[T, List[T]]] = deque([(start, [start])])
    
    while path_queue and len(paths) < max_paths:
        current, path = path_queue.popleft()
        
        if current == end:
            paths.append(path)
            continue
        
        # Only explore if we haven't exceeded the shortest distance
        if len(path) - 1 < target_distance:
            for neighbor in graph.get(current, []):
                # Only follow edges that maintain shortest path property
                if neighbor in distances and distances[neighbor] == distances[current] + 1:
                    path_queue.append((neighbor, path + [neighbor]))
    
    return paths


def bfs_connected_components(graph: Dict[T, List[T]]) -> List[Set[T]]:
    """
    Find all connected components in an undirected graph.
    
    Args:
        graph: Adjacency list representation
        
    Returns:
        List of sets, where each set contains nodes in a connected component
        
    Example:
        >>> graph = {
        ...     'A': ['B'], 'B': ['A'],
        ...     'C': ['D'], 'D': ['C'],
        ...     'E': []
        ... }
        >>> components = bfs_connected_components(graph)
        >>> len(components)
        3
    """
    visited: Set[T] = set()
    components: List[Set[T]] = []
    
    for node in graph:
        if node in visited:
            continue
        
        # BFS to find all nodes in this component
        component: Set[T] = set()
        queue: deque[T] = deque([node])
        component.add(node)
        visited.add(node)
        
        while queue:
            current = queue.popleft()
            
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        
        components.append(component)
    
    return components

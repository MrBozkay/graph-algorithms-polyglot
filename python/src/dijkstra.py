"""Dijkstra's Algorithm Implementation

Finds the shortest path from a source node to all other nodes in a weighted graph
with non-negative edge weights.

Time Complexity: O((V + E) log V) with binary heap
Space Complexity: O(V)
"""

import heapq
from typing import Dict, List, Tuple, Optional, Set


def dijkstra(
    graph: Dict[str, Dict[str, float]], 
    start: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Dijkstra's algorithm for finding shortest paths from a source node.
    
    Args:
        graph: Adjacency list representation {node: {neighbor: weight}}
        start: Starting node
        
    Returns:
        Tuple of (distances, predecessors)
        - distances: Dict mapping each node to its shortest distance from start
        - predecessors: Dict mapping each node to its predecessor in the shortest path
        
    Example:
        >>> graph = {
        ...     'A': {'B': 4, 'C': 2},
        ...     'B': {'C': 1, 'D': 5},
        ...     'C': {'D': 8, 'E': 10},
        ...     'D': {'E': 2},
        ...     'E': {}
        ... }
        >>> distances, predecessors = dijkstra(graph, 'A')
        >>> distances['E']
        11
    """
    # Initialize distances and predecessors
    distances: Dict[str, float] = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessors: Dict[str, Optional[str]] = {node: None for node in graph}
    
    # Priority queue: (distance, node)
    pq: List[Tuple[float, str]] = [(0, start)]
    visited: Set[str] = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Skip if we found a better path already
        if current_distance > distances[current_node]:
            continue
        
        # Check all neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # If we found a shorter path, update it
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    return distances, predecessors


def dijkstra_path(
    graph: Dict[str, Dict[str, float]], 
    start: str, 
    end: str
) -> Tuple[float, List[str]]:
    """
    Find the shortest path between two specific nodes.
    
    Args:
        graph: Adjacency list representation
        start: Starting node
        end: Target node
        
    Returns:
        Tuple of (distance, path)
        - distance: Shortest distance from start to end
        - path: List of nodes in the shortest path
        
    Raises:
        ValueError: If no path exists between start and end
        
    Example:
        >>> graph = {'A': {'B': 1}, 'B': {'C': 2}, 'C': {}}
        >>> distance, path = dijkstra_path(graph, 'A', 'C')
        >>> path
        ['A', 'B', 'C']
    """
    distances, predecessors = dijkstra(graph, start)
    
    # Check if path exists
    if distances[end] == float('inf'):
        raise ValueError(f"No path exists from {start} to {end}")
    
    # Reconstruct path
    path: List[str] = []
    current: Optional[str] = end
    
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    path.reverse()
    
    return distances[end], path


def dijkstra_early_exit(
    graph: Dict[str, Dict[str, float]], 
    start: str, 
    target: str
) -> Tuple[float, List[str]]:
    """
    Optimized version that stops as soon as the target is reached.
    
    Args:
        graph: Adjacency list representation
        start: Starting node
        target: Target node
        
    Returns:
        Tuple of (distance, path)
    """
    distances: Dict[str, float] = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessors: Dict[str, Optional[str]] = {node: None for node in graph}
    
    pq: List[Tuple[float, str]] = [(0, start)]
    visited: Set[str] = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Early exit if we reached the target
        if current_node == target:
            break
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    # Reconstruct path
    if distances[target] == float('inf'):
        raise ValueError(f"No path exists from {start} to {target}")
    
    path: List[str] = []
    current: Optional[str] = target
    
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    path.reverse()
    
    return distances[target], path

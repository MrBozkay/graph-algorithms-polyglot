"""Bellman-Ford Algorithm Implementation

Finds shortest paths from a source node to all other nodes, even with negative edge weights.
Can also detect negative cycles.

Time Complexity: O(VE)
Space Complexity: O(V)
"""

from typing import Dict, List, Tuple, Optional, Set


def bellman_ford(
    graph: Dict[str, Dict[str, float]], 
    start: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Bellman-Ford algorithm for shortest paths with negative weights.
    
    Args:
        graph: Adjacency list representation {node: {neighbor: weight}}
        start: Starting node
        
    Returns:
        Tuple of (distances, predecessors)
        - distances: Dict mapping each node to its shortest distance from start
        - predecessors: Dict mapping each node to its predecessor in the shortest path
        
    Raises:
        ValueError: If a negative cycle is detected
        
    Example:
        >>> graph = {
        ...     'A': {'B': -1, 'C': 4},
        ...     'B': {'C': 3, 'D': 2},
        ...     'C': {},
        ...     'D': {'B': 1, 'C': 5}
        ... }
        >>> distances, predecessors = bellman_ford(graph, 'A')
        >>> distances['C']
        2
    """
    # Initialize distances and predecessors
    distances: Dict[str, float] = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessors: Dict[str, Optional[str]] = {node: None for node in graph}
    
    # Get all nodes
    nodes = list(graph.keys())
    num_nodes = len(nodes)
    
    # Relax edges V-1 times
    for _ in range(num_nodes - 1):
        updated = False
        
        for node in nodes:
            if distances[node] == float('inf'):
                continue
                
            for neighbor, weight in graph[node].items():
                new_distance = distances[node] + weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = node
                    updated = True
        
        # Early termination if no updates
        if not updated:
            break
    
    # Check for negative cycles
    for node in nodes:
        if distances[node] == float('inf'):
            continue
            
        for neighbor, weight in graph[node].items():
            if distances[node] + weight < distances[neighbor]:
                raise ValueError("Graph contains a negative cycle")
    
    return distances, predecessors


def detect_negative_cycle(graph: Dict[str, Dict[str, float]]) -> Optional[List[str]]:
    """
    Detect if a graph contains a negative cycle and return it.
    
    Args:
        graph: Adjacency list representation
        
    Returns:
        List of nodes forming a negative cycle, or None if no cycle exists
        
    Example:
        >>> graph = {
        ...     'A': {'B': 1},
        ...     'B': {'C': -3},
        ...     'C': {'A': 1}
        ... }
        >>> cycle = detect_negative_cycle(graph)
        >>> cycle
        ['A', 'B', 'C', 'A']
    """
    # Initialize distances and predecessors
    nodes = list(graph.keys())
    distances: Dict[str, float] = {node: float('inf') for node in nodes}
    predecessors: Dict[str, Optional[str]] = {node: None for node in nodes}
    
    # Use first node as arbitrary start
    if not nodes:
        return None
    
    start = nodes[0]
    distances[start] = 0
    
    num_nodes = len(nodes)
    
    # Relax edges V-1 times
    for _ in range(num_nodes - 1):
        for node in nodes:
            if distances[node] == float('inf'):
                continue
                
            for neighbor, weight in graph[node].items():
                new_distance = distances[node] + weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = node
    
    # Check for negative cycles and find a node in the cycle
    cycle_node: Optional[str] = None
    
    for node in nodes:
        if distances[node] == float('inf'):
            continue
            
        for neighbor, weight in graph[node].items():
            if distances[node] + weight < distances[neighbor]:
                cycle_node = neighbor
                break
        
        if cycle_node:
            break
    
    if not cycle_node:
        return None
    
    # Trace back to find the cycle
    # Move back V times to ensure we're in the cycle
    for _ in range(num_nodes):
        cycle_node = predecessors[cycle_node]
    
    # Now trace the cycle
    cycle: List[str] = []
    current = cycle_node
    
    while True:
        cycle.append(current)
        current = predecessors[current]
        
        if current == cycle_node:
            cycle.append(current)
            break
    
    cycle.reverse()
    return cycle


def bellman_ford_path(
    graph: Dict[str, Dict[str, float]], 
    start: str, 
    end: str
) -> Tuple[float, List[str]]:
    """
    Find the shortest path between two specific nodes using Bellman-Ford.
    
    Args:
        graph: Adjacency list representation
        start: Starting node
        end: Target node
        
    Returns:
        Tuple of (distance, path)
        
    Raises:
        ValueError: If no path exists or negative cycle detected
    """
    distances, predecessors = bellman_ford(graph, start)
    
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

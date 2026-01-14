"""Tests for BFS Algorithm"""

import pytest
from src.bfs import bfs, bfs_shortest_path, bfs_all_paths, bfs_connected_components


class TestBFS:
    """Test cases for BFS algorithm."""
    
    def test_simple_graph(self) -> None:
        """Test BFS with a simple graph."""
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['D', 'E'],
            'D': ['E'],
            'E': []
        }
        
        distances = bfs(graph, 'A')
        
        assert distances['A'] == 0
        assert distances['B'] == 1
        assert distances['C'] == 1
        assert distances['D'] == 2
        assert distances['E'] == 2
    
    def test_shortest_path(self) -> None:
        """Test finding shortest path."""
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['D'],
            'D': []
        }
        
        distance, path = bfs_shortest_path(graph, 'A', 'D')
        
        assert distance == 2
        assert len(path) == 3
        assert path[0] == 'A'
        assert path[-1] == 'D'
    
    def test_start_equals_end(self) -> None:
        """Test when start and end are the same."""
        graph = {'A': ['B'], 'B': []}
        
        distance, path = bfs_shortest_path(graph, 'A', 'A')
        
        assert distance == 0
        assert path == ['A']
    
    def test_no_path_exists(self) -> None:
        """Test when no path exists."""
        graph = {
            'A': ['B'],
            'B': [],
            'C': []
        }
        
        with pytest.raises(ValueError, match="No path exists"):
            bfs_shortest_path(graph, 'A', 'C')
    
    def test_all_shortest_paths(self) -> None:
        """Test finding all shortest paths."""
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['D'],
            'D': []
        }
        
        paths = bfs_all_paths(graph, 'A', 'D')
        
        assert len(paths) == 2
        assert ['A', 'B', 'D'] in paths
        assert ['A', 'C', 'D'] in paths
    
    def test_connected_components(self) -> None:
        """Test finding connected components."""
        graph = {
            'A': ['B'],
            'B': ['A'],
            'C': ['D'],
            'D': ['C'],
            'E': []
        }
        
        components = bfs_connected_components(graph)
        
        assert len(components) == 3
        
        # Check that each component has the right nodes
        component_sets = [set(c) for c in components]
        assert {'A', 'B'} in component_sets
        assert {'C', 'D'} in component_sets
        assert {'E'} in component_sets
    
    def test_single_node(self) -> None:
        """Test with a single node."""
        graph = {'A': []}
        
        distances = bfs(graph, 'A')
        
        assert distances == {'A': 0}
    
    def test_linear_graph(self) -> None:
        """Test with a linear graph."""
        graph = {
            'A': ['B'],
            'B': ['C'],
            'C': ['D'],
            'D': []
        }
        
        distance, path = bfs_shortest_path(graph, 'A', 'D')
        
        assert distance == 3
        assert path == ['A', 'B', 'C', 'D']
    
    def test_cyclic_graph(self) -> None:
        """Test with a graph containing cycles."""
        graph = {
            'A': ['B'],
            'B': ['C'],
            'C': ['A', 'D'],
            'D': []
        }
        
        distance, path = bfs_shortest_path(graph, 'A', 'D')
        
        assert distance == 3
        assert path == ['A', 'B', 'C', 'D']

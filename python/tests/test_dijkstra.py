"""Tests for Dijkstra's Algorithm"""

import pytest
from src.dijkstra import dijkstra, dijkstra_path, dijkstra_early_exit


class TestDijkstra:
    """Test cases for Dijkstra's algorithm."""
    
    def test_simple_graph(self) -> None:
        """Test with a simple graph."""
        graph = {
            'A': {'B': 4, 'C': 2},
            'B': {'C': 1, 'D': 5},
            'C': {'D': 8},
            'D': {}
        }
        
        distances, predecessors = dijkstra(graph, 'A')
        
        assert distances['A'] == 0
        assert distances['B'] == 4
        assert distances['C'] == 2
        assert distances['D'] == 9
        
        assert predecessors['A'] is None
        assert predecessors['B'] == 'A'
        assert predecessors['C'] == 'A'
        assert predecessors['D'] == 'B'
    
    def test_path_finding(self) -> None:
        """Test finding a specific path."""
        graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'C': 2, 'D': 5},
            'C': {'D': 1},
            'D': {}
        }
        
        distance, path = dijkstra_path(graph, 'A', 'D')
        
        assert distance == 4
        assert path == ['A', 'B', 'C', 'D']
    
    def test_single_node(self) -> None:
        """Test with a single node."""
        graph = {'A': {}}
        
        distances, _ = dijkstra(graph, 'A')
        
        assert distances['A'] == 0
    
    def test_disconnected_graph(self) -> None:
        """Test with disconnected components."""
        graph = {
            'A': {'B': 1},
            'B': {},
            'C': {'D': 1},
            'D': {}
        }
        
        distances, _ = dijkstra(graph, 'A')
        
        assert distances['A'] == 0
        assert distances['B'] == 1
        assert distances['C'] == float('inf')
        assert distances['D'] == float('inf')
    
    def test_no_path_exists(self) -> None:
        """Test when no path exists between nodes."""
        graph = {
            'A': {'B': 1},
            'B': {},
            'C': {}
        }
        
        with pytest.raises(ValueError, match="No path exists"):
            dijkstra_path(graph, 'A', 'C')
    
    def test_multiple_paths(self) -> None:
        """Test graph with multiple paths - should find shortest."""
        graph = {
            'A': {'B': 5, 'C': 2},
            'B': {'D': 1},
            'C': {'B': 1, 'D': 6},
            'D': {}
        }
        
        distance, path = dijkstra_path(graph, 'A', 'D')
        
        assert distance == 4
        assert path == ['A', 'C', 'B', 'D']
    
    def test_early_exit_optimization(self) -> None:
        """Test early exit variant."""
        graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'C': 2, 'D': 5},
            'C': {'D': 1},
            'D': {'E': 1},
            'E': {}
        }
        
        distance, path = dijkstra_early_exit(graph, 'A', 'D')
        
        assert distance == 4
        assert path == ['A', 'B', 'C', 'D']
    
    def test_zero_weight_edges(self) -> None:
        """Test with zero-weight edges."""
        graph = {
            'A': {'B': 0, 'C': 5},
            'B': {'C': 1},
            'C': {}
        }
        
        distances, _ = dijkstra(graph, 'A')
        
        assert distances['A'] == 0
        assert distances['B'] == 0
        assert distances['C'] == 1
    
    def test_self_loop(self) -> None:
        """Test with self-loops (should be ignored)."""
        graph = {
            'A': {'A': 5, 'B': 1},
            'B': {}
        }
        
        distances, _ = dijkstra(graph, 'A')
        
        assert distances['A'] == 0
        assert distances['B'] == 1

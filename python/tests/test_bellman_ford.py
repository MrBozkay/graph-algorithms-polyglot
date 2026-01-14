"""Tests for Bellman-Ford Algorithm"""

import pytest
from src.bellman_ford import bellman_ford, detect_negative_cycle, bellman_ford_path


class TestBellmanFord:
    """Test cases for Bellman-Ford algorithm."""
    
    def test_simple_graph(self) -> None:
        """Test with a simple graph."""
        graph = {
            'A': {'B': -1, 'C': 4},
            'B': {'C': 3, 'D': 2},
            'C': {},
            'D': {'B': 1, 'C': 5}
        }
        
        distances, predecessors = bellman_ford(graph, 'A')
        
        assert distances['A'] == 0
        assert distances['B'] == -1
        assert distances['C'] == 2
        assert distances['D'] == 1
    
    def test_negative_weights(self) -> None:
        """Test handling of negative weights."""
        graph = {
            'A': {'B': 5},
            'B': {'C': -3},
            'C': {'D': 2},
            'D': {}
        }
        
        distances, _ = bellman_ford(graph, 'A')
        
        assert distances['A'] == 0
        assert distances['B'] == 5
        assert distances['C'] == 2
        assert distances['D'] == 4
    
    def test_negative_cycle_detection(self) -> None:
        """Test detection of negative cycles."""
        graph = {
            'A': {'B': 1},
            'B': {'C': -3},
            'C': {'A': 1}
        }
        
        with pytest.raises(ValueError, match="negative cycle"):
            bellman_ford(graph, 'A')
    
    def test_detect_negative_cycle_returns_cycle(self) -> None:
        """Test that detect_negative_cycle returns the actual cycle."""
        graph = {
            'A': {'B': 1},
            'B': {'C': -3},
            'C': {'A': 1}
        }
        
        cycle = detect_negative_cycle(graph)
        
        assert cycle is not None
        assert len(cycle) >= 3
        assert cycle[0] == cycle[-1]  # Cycle should start and end at same node
    
    def test_no_negative_cycle(self) -> None:
        """Test when no negative cycle exists."""
        graph = {
            'A': {'B': 1},
            'B': {'C': -1},
            'C': {'D': 1},
            'D': {}
        }
        
        cycle = detect_negative_cycle(graph)
        
        assert cycle is None
    
    def test_path_finding(self) -> None:
        """Test finding a specific path."""
        graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'C': -2, 'D': 5},
            'C': {'D': 1},
            'D': {}
        }
        
        distance, path = bellman_ford_path(graph, 'A', 'D')
        
        assert distance == 0
        assert path == ['A', 'B', 'C', 'D']
    
    def test_disconnected_graph(self) -> None:
        """Test with disconnected components."""
        graph = {
            'A': {'B': 1},
            'B': {},
            'C': {'D': 1},
            'D': {}
        }
        
        distances, _ = bellman_ford(graph, 'A')
        
        assert distances['A'] == 0
        assert distances['B'] == 1
        assert distances['C'] == float('inf')
        assert distances['D'] == float('inf')
    
    def test_early_termination(self) -> None:
        """Test that algorithm terminates early when no updates occur."""
        graph = {
            'A': {'B': 1},
            'B': {'C': 1},
            'C': {'D': 1},
            'D': {}
        }
        
        # Should terminate before V-1 iterations
        distances, _ = bellman_ford(graph, 'A')
        
        assert distances['D'] == 3

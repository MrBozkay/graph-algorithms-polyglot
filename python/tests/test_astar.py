"""Tests for A* Search Algorithm"""

import pytest
from src.astar import astar_search, astar_grid_search


class TestAstar:
    """Test cases for A* search algorithm."""
    
    def test_simple_graph_with_heuristic(self) -> None:
        """Test A* with a simple graph and zero heuristic (becomes Dijkstra)."""
        graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'D': 2},
            'C': {'D': 1},
            'D': {}
        }
        
        def zero_heuristic(node: str, goal: str) -> float:
            return 0
        
        distance, path = astar_search(graph, 'A', 'D', zero_heuristic)
        
        assert distance == 3
        assert path == ['A', 'B', 'D']
    
    def test_grid_search_manhattan(self) -> None:
        """Test A* on a grid with Manhattan distance."""
        grid = [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]
        ]
        
        distance, path = astar_grid_search(grid, (0, 0), (2, 3), allow_diagonal=False)
        
        assert distance == 5  # Manhattan distance
        assert len(path) == 6  # 6 steps
        assert path[0] == (0, 0)
        assert path[-1] == (2, 3)
    
    def test_grid_search_diagonal(self) -> None:
        """Test A* on a grid with diagonal movement."""
        grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        distance, path = astar_grid_search(grid, (0, 0), (2, 2), allow_diagonal=True)
        
        # Diagonal distance should be less than Manhattan
        assert distance < 4
        assert path[0] == (0, 0)
        assert path[-1] == (2, 2)
    
    def test_grid_with_obstacles(self) -> None:
        """Test A* navigating around obstacles."""
        grid = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        
        distance, path = astar_grid_search(grid, (0, 0), (2, 2), allow_diagonal=False)
        
        # Should navigate around the obstacle
        assert (1, 1) not in path
        assert path[0] == (0, 0)
        assert path[-1] == (2, 2)
    
    def test_no_path_in_grid(self) -> None:
        """Test when no path exists in grid."""
        grid = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]
        
        with pytest.raises(ValueError, match="No path exists"):
            astar_grid_search(grid, (0, 0), (2, 2), allow_diagonal=False)
    
    def test_admissible_heuristic(self) -> None:
        """Test that A* finds optimal path with admissible heuristic."""
        graph = {
            'A': {'B': 1, 'C': 2},
            'B': {'D': 3},
            'C': {'D': 1},
            'D': {}
        }
        
        # Admissible heuristic (never overestimates)
        def heuristic(node: str, goal: str) -> float:
            distances_to_d = {'A': 2, 'B': 3, 'C': 1, 'D': 0}
            return distances_to_d.get(node, 0)
        
        distance, path = astar_search(graph, 'A', 'D', heuristic)
        
        assert distance == 3
        assert path == ['A', 'C', 'D']
    
    def test_start_equals_goal(self) -> None:
        """Test when start and goal are the same."""
        grid = [[0, 0], [0, 0]]
        
        distance, path = astar_grid_search(grid, (0, 0), (0, 0), allow_diagonal=False)
        
        assert distance == 0
        assert path == [(0, 0)]

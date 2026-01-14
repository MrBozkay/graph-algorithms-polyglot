"""Graph Algorithms Library - Python Implementation

A collection of classic graph algorithms with real-world examples.
"""

__version__ = "0.1.0"
__author__ = "Graph Algorithms Polyglot Contributors"

from .dijkstra import dijkstra, dijkstra_path
from .astar import astar_search
from .bellman_ford import bellman_ford, detect_negative_cycle
from .bfs import bfs, bfs_shortest_path

__all__ = [
    "dijkstra",
    "dijkstra_path",
    "astar_search",
    "bellman_ford",
    "detect_negative_cycle",
    "bfs",
    "bfs_shortest_path",
]

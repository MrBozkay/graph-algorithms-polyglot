# Python Graph Algorithms

Professional Python implementation of classic graph algorithms with comprehensive examples and tests.

## Features

- ✅ **Dijkstra's Algorithm** - Shortest path in weighted graphs
- ✅ **A* Search** - Heuristic-based pathfinding
- ✅ **Bellman-Ford** - Handles negative weights, detects cycles
- ✅ **BFS** - Shortest path in unweighted graphs
- 📝 Full type hints (mypy compatible)
- 🧪 90%+ test coverage
- 📚 Comprehensive documentation
- 🎯 Real-world examples

## Installation

```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
from src.dijkstra import dijkstra_path

# Create a graph
graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'C': 1, 'D': 5},
    'C': {'D': 8},
    'D': {}
}

# Find shortest path
distance, path = dijkstra_path(graph, 'A', 'D')
print(f"Distance: {distance}, Path: {path}")
# Output: Distance: 8, Path: ['A', 'B', 'C', 'D']
```

## Examples

Run the real-world examples:

```bash
# GPS Navigation (Dijkstra)
python examples/gps_navigation.py

# Game AI Pathfinding (A*)
python examples/game_pathfinding.py

# Currency Arbitrage Detection (Bellman-Ford)
python examples/currency_arbitrage.py

# Social Network Analysis (BFS)
python examples/social_network.py
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Type checking
mypy src/

# Linting
ruff check src/ tests/ examples/
```

## Project Structure

```
python/
├── src/              # Core algorithm implementations
│   ├── dijkstra.py
│   ├── astar.py
│   ├── bellman_ford.py
│   └── bfs.py
├── examples/         # Real-world examples
│   ├── gps_navigation.py
│   ├── game_pathfinding.py
│   ├── currency_arbitrage.py
│   └── social_network.py
├── tests/            # Unit tests
└── pyproject.toml    # Project configuration
```

## Requirements

- Python 3.10 or higher
- No external dependencies for core algorithms
- Development dependencies: pytest, mypy, ruff

## License

MIT License - see LICENSE file for details

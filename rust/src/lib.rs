//! Graph Algorithms Library
//!
//! Professional implementation of classic graph algorithms in Rust.
//!
//! # Algorithms
//!
//! - **Dijkstra's Algorithm**: Shortest path in weighted graphs with non-negative weights
//! - **A* Search**: Heuristic-based pathfinding
//! - **Bellman-Ford**: Shortest path with negative weights, cycle detection
//! - **BFS**: Shortest path in unweighted graphs
//!
//! # Example
//!
//! ```
//! use graph_algorithms::dijkstra::{Graph, dijkstra_path};
//! use std::collections::HashMap;
//!
//! let mut graph = HashMap::new();
//! graph.insert("A", vec![("B", 4.0), ("C", 2.0)]);
//! graph.insert("B", vec![("D", 5.0)]);
//! graph.insert("C", vec![("D", 1.0)]);
//! graph.insert("D", vec![]);
//!
//! let (distance, path) = dijkstra_path(&graph, "A", "D").unwrap();
//! assert_eq!(distance, 3.0);
//! ```

pub mod dijkstra;
pub mod astar;
pub mod bellman_ford;
pub mod bfs;

//! Dijkstra's Algorithm Implementation
//!
//! Finds the shortest path from a source node to all other nodes in a weighted graph
//! with non-negative edge weights.
//!
//! Time Complexity: O((V + E) log V) with binary heap
//! Space Complexity: O(V)

use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, HashSet};
use std::hash::Hash;

/// Graph represented as an adjacency list
pub type Graph<'a, T> = HashMap<T, Vec<(T, f64)>>;

/// Result of Dijkstra's algorithm
#[derive(Debug, Clone)]
pub struct DijkstraResult<T: Clone> {
    pub distances: HashMap<T, f64>,
    pub predecessors: HashMap<T, Option<T>>,
}

/// Path result between two nodes
#[derive(Debug, Clone)]
pub struct PathResult<T: Clone> {
    pub distance: f64,
    pub path: Vec<T>,
}

/// Priority queue item for Dijkstra's algorithm
#[derive(Debug, Clone)]
struct PQItem<T> {
    node: T,
    distance: f64,
}

impl<T> PartialEq for PQItem<T> {
    fn eq(&self, other: &Self) -> bool {
        self.distance == other.distance
    }
}

impl<T> Eq for PQItem<T> {}

impl<T> PartialOrd for PQItem<T> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl<T> Ord for PQItem<T> {
    fn cmp(&self, other: &Self) -> Ordering {
        // Reverse ordering for min-heap
        other.distance.partial_cmp(&self.distance).unwrap_or(Ordering::Equal)
    }
}

/// Run Dijkstra's algorithm from a source node
///
/// # Arguments
///
/// * `graph` - Adjacency list representation of the graph
/// * `start` - Starting node
///
/// # Returns
///
/// `DijkstraResult` containing distances and predecessors
///
/// # Example
///
/// ```
/// use graph_algorithms::dijkstra::{dijkstra, Graph};
/// use std::collections::HashMap;
///
/// let mut graph: Graph<&str> = HashMap::new();
/// graph.insert("A", vec![("B", 4.0), ("C", 2.0)]);
/// graph.insert("B", vec![]);
/// graph.insert("C", vec![]);
///
/// let result = dijkstra(&graph, &"A");
/// assert_eq!(result.distances[&"A"], 0.0);
/// assert_eq!(result.distances[&"B"], 4.0);
/// ```
pub fn dijkstra<T>(graph: &Graph<T>, start: &T) -> DijkstraResult<T>
where
    T: Eq + Hash + Clone,
{
    let mut distances: HashMap<T, f64> = HashMap::new();
    let mut predecessors: HashMap<T, Option<T>> = HashMap::new();
    let mut visited: HashSet<T> = HashSet::new();

    // Initialize distances
    for node in graph.keys() {
        distances.insert(node.clone(), f64::INFINITY);
        predecessors.insert(node.clone(), None);
    }
    distances.insert(start.clone(), 0.0);

    // Priority queue
    let mut pq = BinaryHeap::new();
    pq.push(PQItem {
        node: start.clone(),
        distance: 0.0,
    });

    while let Some(PQItem { node: current, distance: current_distance }) = pq.pop() {
        // Skip if already visited
        if visited.contains(&current) {
            continue;
        }
        visited.insert(current.clone());

        // Skip if we found a better path already
        if current_distance > distances[&current] {
            continue;
        }

        // Check all neighbors
        if let Some(neighbors) = graph.get(&current) {
            for (neighbor, weight) in neighbors {
                let distance = current_distance + weight;

                // If we found a shorter path, update it
                if distance < distances[neighbor] {
                    distances.insert(neighbor.clone(), distance);
                    predecessors.insert(neighbor.clone(), Some(current.clone()));
                    pq.push(PQItem {
                        node: neighbor.clone(),
                        distance,
                    });
                }
            }
        }
    }

    DijkstraResult {
        distances,
        predecessors,
    }
}

/// Find the shortest path between two specific nodes
///
/// # Arguments
///
/// * `graph` - Adjacency list representation
/// * `start` - Starting node
/// * `end` - Target node
///
/// # Returns
///
/// `Result` containing `PathResult` or error if no path exists
pub fn dijkstra_path<T>(graph: &Graph<T>, start: &T, end: &T) -> Result<PathResult<T>, String>
where
    T: Eq + Hash + Clone,
{
    let result = dijkstra(graph, start);

    // Check if path exists
    if result.distances[end].is_infinite() {
        return Err(format!("No path exists from {:?} to {:?}", start, end));
    }

    // Reconstruct path
    let mut path = Vec::new();
    let mut current = Some(end.clone());

    while let Some(node) = current {
        path.push(node.clone());
        current = result.predecessors[&node].clone();
    }

    path.reverse();

    Ok(PathResult {
        distance: result.distances[end],
        path,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_graph() {
        let mut graph: Graph<&str> = HashMap::new();
        graph.insert("A", vec![("B", 4.0), ("C", 2.0)]);
        graph.insert("B", vec![("C", 1.0), ("D", 5.0)]);
        graph.insert("C", vec![("D", 8.0)]);
        graph.insert("D", vec![]);

        let result = dijkstra(&graph, &"A");

        assert_eq!(result.distances[&"A"], 0.0);
        assert_eq!(result.distances[&"B"], 4.0);
        assert_eq!(result.distances[&"C"], 2.0);
        assert_eq!(result.distances[&"D"], 9.0);
    }

    #[test]
    fn test_path_finding() {
        let mut graph: Graph<&str> = HashMap::new();
        graph.insert("A", vec![("B", 1.0), ("C", 4.0)]);
        graph.insert("B", vec![("C", 2.0), ("D", 5.0)]);
        graph.insert("C", vec![("D", 1.0)]);
        graph.insert("D", vec![]);

        let result = dijkstra_path(&graph, &"A", &"D").unwrap();

        assert_eq!(result.distance, 4.0);
        assert_eq!(result.path, vec!["A", "B", "C", "D"]);
    }

    #[test]
    fn test_no_path() {
        let mut graph: Graph<&str> = HashMap::new();
        graph.insert("A", vec![("B", 1.0)]);
        graph.insert("B", vec![]);
        graph.insert("C", vec![]);

        let result = dijkstra_path(&graph, &"A", &"C");

        assert!(result.is_err());
    }
}

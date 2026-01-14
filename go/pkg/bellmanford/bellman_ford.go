package bellmanford

import (
	"fmt"
	"math"
)

// Graph represents a graph where edges have weights
type Graph map[string]map[string]float64

// Result contains the shortest distances and predecessors
type Result struct {
	Distances    map[string]float64
	Predecessors map[string]*string
}

// CheckNegativeCycleResult contains the cycle if found
type CheckNegativeCycleResult struct {
	HasCycle bool
	Cycle    []string
}

// Run executes the Bellman-Ford algorithm
// Returns error if a negative cycle is detected
func Run(graph Graph, start string) (*Result, error) {
	distances := make(map[string]float64)
	predecessors := make(map[string]*string)

	// Initialize
	for node := range graph {
		distances[node] = math.Inf(1)
		predecessors[node] = nil
	}
	distances[start] = 0

	// Get all nodes for iteration
	nodes := make([]string, 0, len(graph))
	for node := range graph {
		nodes = append(nodes, node)
	}

	// Relax edges |V| - 1 times
	for i := 0; i < len(nodes)-1; i++ {
		updated := false
		for u := range graph {
			if math.IsInf(distances[u], 1) {
				continue
			}
			for v, weight := range graph[u] {
				if distances[u]+weight < distances[v] {
					distances[v] = distances[u] + weight
					curr := u
					predecessors[v] = &curr
					updated = true
				}
			}
		}
		if !updated {
			break
		}
	}

	// Check for negative cycles
	for u := range graph {
		if math.IsInf(distances[u], 1) {
			continue
		}
		for v, weight := range graph[u] {
			if distances[u]+weight < distances[v] {
				return nil, fmt.Errorf("negative cycle detected")
			}
		}
	}

	return &Result{
		Distances:    distances,
		Predecessors: predecessors,
	}, nil
}

// DetectNegativeCycle checks for negative cycles and returns one if found
func DetectNegativeCycle(graph Graph) []string {
	distances := make(map[string]float64)
	predecessors := make(map[string]*string)

	// Identify all nodes
	nodes := make([]string, 0, len(graph))
	for node := range graph {
		nodes = append(nodes, node)
	}

	if len(nodes) == 0 {
		return nil
	}

	// Initialize with arbitrary start node (or all 0 if we want to find any cycle reachable from anywhere)
	// For cycle detection in disconnected components, we'd typically add a dummy source connected to all nodes with 0 weight.
	// Here we'll just try to relax from a source. If the graph is connected, it works.
	// A more robust way for ANY cycle is to set all distances to 0.
	for _, node := range nodes {
		distances[node] = 0
		predecessors[node] = nil
	}

	// Relax |V| - 1 times
	for i := 0; i < len(nodes)-1; i++ {
		for u := range graph {
			for v, weight := range graph[u] {
				if distances[u]+weight < distances[v] {
					distances[v] = distances[u] + weight
					curr := u
					predecessors[v] = &curr
				}
			}
		}
	}

	// Check for cycle
	var cycleNode *string
	for u := range graph {
		for v, weight := range graph[u] {
			if distances[u]+weight < distances[v] {
				// Cycle detected
				node := v
				cycleNode = &node
				// Retrace back to ensure we are in the cycle
				for i := 0; i < len(nodes); i++ {
					if predecessors[*cycleNode] != nil {
						node := *predecessors[*cycleNode]
						cycleNode = &node
					}
				}
				goto Found
			}
		}
	}
	return nil

Found:
	// Trace the cycle
	cycle := make([]string, 0)
	curr := *cycleNode
	for {
		cycle = append(cycle, curr)
		if predecessors[curr] != nil {
			curr = *predecessors[curr]
			if curr == *cycleNode && len(cycle) > 0 {
				cycle = append(cycle, curr)
				break
			}
		} else {
			break // Should not happen in a cycle
		}
	}

	// Reverse to get correct order
	for i, j := 0, len(cycle)-1; i < j; i, j = i+1, j-1 {
		cycle[i], cycle[j] = cycle[j], cycle[i]
	}

	return cycle
}

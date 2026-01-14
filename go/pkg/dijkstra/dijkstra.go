// Package dijkstra implements Dijkstra's shortest path algorithm
package dijkstra

import (
	"container/heap"
	"fmt"
	"math"
)

// Graph represents a weighted directed graph using an adjacency list
type Graph map[string]map[string]float64

// Result contains the shortest distances and predecessors from a source node
type Result struct {
	Distances    map[string]float64
	Predecessors map[string]*string
}

// PathResult contains the distance and path between two nodes
type PathResult struct {
	Distance float64
	Path     []string
}

// priorityQueueItem represents an item in the priority queue
type priorityQueueItem struct {
	node     string
	distance float64
	index    int
}

// priorityQueue implements heap.Interface
type priorityQueue []*priorityQueueItem

func (pq priorityQueue) Len() int { return len(pq) }

func (pq priorityQueue) Less(i, j int) bool {
	return pq[i].distance < pq[j].distance
}

func (pq priorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *priorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*priorityQueueItem)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *priorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	item.index = -1
	*pq = old[0 : n-1]
	return item
}

// Dijkstra finds the shortest paths from a source node to all other nodes
//
// Time Complexity: O((V + E) log V)
// Space Complexity: O(V)
func Dijkstra(graph Graph, start string) (*Result, error) {
	// Initialize distances and predecessors
	distances := make(map[string]float64)
	predecessors := make(map[string]*string)
	visited := make(map[string]bool)

	for node := range graph {
		distances[node] = math.Inf(1)
		predecessors[node] = nil
	}
	distances[start] = 0

	// Initialize priority queue
	pq := make(priorityQueue, 0)
	heap.Init(&pq)
	heap.Push(&pq, &priorityQueueItem{
		node:     start,
		distance: 0,
	})

	for pq.Len() > 0 {
		current := heap.Pop(&pq).(*priorityQueueItem)

		// Skip if already visited
		if visited[current.node] {
			continue
		}
		visited[current.node] = true

		// Skip if we found a better path already
		if current.distance > distances[current.node] {
			continue
		}

		// Check all neighbors
		for neighbor, weight := range graph[current.node] {
			distance := current.distance + weight

			// If we found a shorter path, update it
			if distance < distances[neighbor] {
				distances[neighbor] = distance
				pred := current.node
				predecessors[neighbor] = &pred
				heap.Push(&pq, &priorityQueueItem{
					node:     neighbor,
					distance: distance,
				})
			}
		}
	}

	return &Result{
		Distances:    distances,
		Predecessors: predecessors,
	}, nil
}

// FindPath finds the shortest path between two specific nodes
func FindPath(graph Graph, start, end string) (*PathResult, error) {
	result, err := Dijkstra(graph, start)
	if err != nil {
		return nil, err
	}

	// Check if path exists
	if math.IsInf(result.Distances[end], 1) {
		return nil, fmt.Errorf("no path exists from %s to %s", start, end)
	}

	// Reconstruct path
	path := make([]string, 0)
	current := &end

	for current != nil {
		path = append([]string{*current}, path...)
		current = result.Predecessors[*current]
	}

	return &PathResult{
		Distance: result.Distances[end],
		Path:     path,
	}, nil
}

// FindPathEarlyExit finds the shortest path with early termination
func FindPathEarlyExit(graph Graph, start, target string) (*PathResult, error) {
	distances := make(map[string]float64)
	predecessors := make(map[string]*string)
	visited := make(map[string]bool)

	for node := range graph {
		distances[node] = math.Inf(1)
		predecessors[node] = nil
	}
	distances[start] = 0

	pq := make(priorityQueue, 0)
	heap.Init(&pq)
	heap.Push(&pq, &priorityQueueItem{
		node:     start,
		distance: 0,
	})

	for pq.Len() > 0 {
		current := heap.Pop(&pq).(*priorityQueueItem)

		// Early exit if we reached the target
		if current.node == target {
			break
		}

		if visited[current.node] {
			continue
		}
		visited[current.node] = true

		if current.distance > distances[current.node] {
			continue
		}

		for neighbor, weight := range graph[current.node] {
			distance := current.distance + weight

			if distance < distances[neighbor] {
				distances[neighbor] = distance
				pred := current.node
				predecessors[neighbor] = &pred
				heap.Push(&pq, &priorityQueueItem{
					node:     neighbor,
					distance: distance,
				})
			}
		}
	}

	// Check if path exists
	if math.IsInf(distances[target], 1) {
		return nil, fmt.Errorf("no path exists from %s to %s", start, target)
	}

	// Reconstruct path
	path := make([]string, 0)
	current := &target

	for current != nil {
		path = append([]string{*current}, path...)
		current = predecessors[*current]
	}

	return &PathResult{
		Distance: distances[target],
		Path:     path,
	}, nil
}

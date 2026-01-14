package astar

import (
	"container/heap"
	"fmt"
	"math"
)

// Graph represents a graph where edges have costs
type Graph map[string]map[string]float64

// HeuristicFunc estimates the cost from a node to the goal
type HeuristicFunc func(node, goal string) float64

// Result contains the path and total cost
type Result struct {
	Distance float64
	Path     []string
}

// priorityQueueItem represents an item in the priority queue
type priorityQueueItem struct {
	node   string
	fScore float64 // f = g + h
	gScore float64 // Cost from start
	index  int
}

// priorityQueue implements heap.Interface
type priorityQueue []*priorityQueueItem

func (pq priorityQueue) Len() int { return len(pq) }

func (pq priorityQueue) Less(i, j int) bool {
	return pq[i].fScore < pq[j].fScore
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

// FindPath finds the shortest path using A* algorithm
func FindPath(graph Graph, start, goal string, h HeuristicFunc) (*Result, error) {
	// Initialize scores
	gScore := make(map[string]float64)
	for node := range graph {
		gScore[node] = math.Inf(1)
	}
	gScore[start] = 0

	// Predecessors for path reconstruction
	predecessors := make(map[string]string)

	// Priority queue
	pq := make(priorityQueue, 0)
	heap.Init(&pq)
	heap.Push(&pq, &priorityQueueItem{
		node:   start,
		gScore: 0,
		fScore: h(start, goal),
	})

	visited := make(map[string]bool)

	for pq.Len() > 0 {
		current := heap.Pop(&pq).(*priorityQueueItem)

		if current.node == goal {
			// Reconstruct path
			path := []string{goal}
			curr := goal
			for curr != start {
				prev, ok := predecessors[curr]
				if !ok {
					return nil, fmt.Errorf("broken path reconstruction")
				}
				path = append([]string{prev}, path...)
				curr = prev
			}
			return &Result{
				Distance: gScore[goal],
				Path:     path,
			}, nil
		}

		if visited[current.node] {
			continue
		}
		visited[current.node] = true

		for neighbor, weight := range graph[current.node] {
			tentativeG := gScore[current.node] + weight

			// Initialize neighbor gScore if infinity (not in map means infinity here effectively if we check properly,
			// but we initialized above loop. However, nodes might be discovered dynamically in some impls,
			// here we rely on graph map keys)
			if val, ok := gScore[neighbor]; !ok || val == 0 {
				// if neighbor wasn't in original graph map iteration (e.g. implicitly defined), treat as inf
				if !ok {
					gScore[neighbor] = math.Inf(1)
				}
			}

			if tentativeG < gScore[neighbor] {
				predecessors[neighbor] = current.node
				gScore[neighbor] = tentativeG
				fScore := tentativeG + h(neighbor, goal)
				heap.Push(&pq, &priorityQueueItem{
					node:   neighbor,
					gScore: tentativeG,
					fScore: fScore,
				})
			}
		}
	}

	return nil, fmt.Errorf("no path found from %s to %s", start, goal)
}

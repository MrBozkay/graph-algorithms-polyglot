package astar

import (
	"math"
	"reflect"
	"testing"
)

func TestAStar(t *testing.T) {
	graph := Graph{
		"A": {"B": 1, "C": 4},
		"B": {"D": 2},
		"C": {"D": 1},
		"D": {},
	}

	// Simple heuristic: just 0 (Dijkstra behavior)
	h := func(node, goal string) float64 {
		return 0
	}

	result, err := FindPath(graph, "A", "D", h)
	if err != nil {
		t.Fatalf("A* failed: %v", err)
	}

	if result.Distance != 3 {
		t.Errorf("Distance: got %v, want 3", result.Distance)
	}

	expectedPath := []string{"A", "B", "D"}
	if !reflect.DeepEqual(result.Path, expectedPath) {
		t.Errorf("Path: got %v, want %v", result.Path, expectedPath)
	}
}

func TestAStarWithHeuristic(t *testing.T) {
	// Grid-like graph
	// A(0,0) -1-> B(1,0) -1-> D(2,0)
	// |                   ^
	// 4                   1
	// v                   |
	// C(0,1) -------------+

	// Coordinates for Manhattan distance
	coords := map[string][2]float64{
		"A": {0, 0},
		"B": {1, 0},
		"C": {0, 1},
		"D": {2, 0},
	}

	graph := Graph{
		"A": {"B": 1, "C": 4},
		"B": {"D": 1},
		"C": {"D": 1},
		"D": {},
	}

	h := func(node, goal string) float64 {
		n := coords[node]
		g := coords[goal]
		return math.Abs(n[0]-g[0]) + math.Abs(n[1]-g[1])
	}

	result, err := FindPath(graph, "A", "D", h)
	if err != nil {
		t.Fatalf("A* failed: %v", err)
	}

	if result.Distance != 2 {
		t.Errorf("Distance: got %v, want 2", result.Distance)
	}

	expectedPath := []string{"A", "B", "D"}
	if !reflect.DeepEqual(result.Path, expectedPath) {
		t.Errorf("Path: got %v, want %v", result.Path, expectedPath)
	}
}

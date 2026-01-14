package bellmanford

import (
	"testing"
)

func TestBellmanFord(t *testing.T) {
	graph := Graph{
		"A": {"B": -1, "C": 4},
		"B": {"C": 3, "D": 2},
		"C": {},
		"D": {"B": 1, "C": 5},
	}

	result, err := Run(graph, "A")
	if err != nil {
		t.Fatalf("Bellman-Ford failed: %v", err)
	}

	expectedDistances := map[string]float64{
		"A": 0,
		"B": -1,
		"C": 2,
		"D": 1,
	}

	for node, expected := range expectedDistances {
		if got := result.Distances[node]; got != expected {
			t.Errorf("Distance for %s: got %v, want %v", node, got, expected)
		}
	}
}

func TestNegativeCycle(t *testing.T) {
	graph := Graph{
		"A": {"B": 1},
		"B": {"C": -3},
		"C": {"A": 1},
	}

	_, err := Run(graph, "A")
	if err == nil {
		t.Fatal("Expected error for negative cycle, got nil")
	}

	cycle := DetectNegativeCycle(graph)
	if cycle == nil {
		t.Fatal("Expected cycle detection, got nil")
	}

	if len(cycle) < 3 {
		t.Errorf("Cycle too short: %v", cycle)
	}
}

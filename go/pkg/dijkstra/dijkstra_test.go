package dijkstra

import (
	"reflect"
	"testing"
)

func TestDijkstra(t *testing.T) {
	graph := Graph{
		"A": {"B": 4, "C": 2},
		"B": {"C": 1, "D": 5},
		"C": {"D": 8},
		"D": {},
	}

	result, err := Dijkstra(graph, "A")
	if err != nil {
		t.Fatalf("Dijkstra failed: %v", err)
	}

	expectedDistances := map[string]float64{
		"A": 0,
		"B": 4,
		"C": 2,
		"D": 9,
	}

	for node, expected := range expectedDistances {
		if got := result.Distances[node]; got != expected {
			t.Errorf("Distance for %s: got %v, want %v", node, got, expected)
		}
	}
}

func TestFindPath(t *testing.T) {
	graph := Graph{
		"A": {"B": 1, "C": 4},
		"B": {"C": 2, "D": 5},
		"C": {"D": 1},
		"D": {},
	}

	result, err := FindPath(graph, "A", "D")
	if err != nil {
		t.Fatalf("FindPath failed: %v", err)
	}

	if result.Distance != 4 {
		t.Errorf("Path distance: got %v, want 4", result.Distance)
	}

	expectedPath := []string{"A", "B", "C", "D"}
	if !reflect.DeepEqual(result.Path, expectedPath) {
		t.Errorf("Path: got %v, want %v", result.Path, expectedPath)
	}
}

func TestNoPath(t *testing.T) {
	graph := Graph{
		"A": {"B": 1},
		"B": {},
		"C": {},
	}

	_, err := FindPath(graph, "A", "C")
	if err == nil {
		t.Error("Expected error for non-existent path, got nil")
	}
}

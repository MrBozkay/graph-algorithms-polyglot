"""Game AI Pathfinding Example using A* Algorithm

Real-world example: Finding optimal paths for game characters in a grid-based game.
"""

from typing import List, Tuple
from src.astar import astar_grid_search


def create_dungeon_map() -> List[List[int]]:
    """
    Create a dungeon map for a game.
    0 = walkable floor
    1 = wall/obstacle
    """
    return [
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    ]


def visualize_path(
    grid: List[List[int]], 
    path: List[Tuple[int, int]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> None:
    """Visualize the grid with the path marked."""
    rows, cols = len(grid), len(grid[0])
    
    # Create a copy for visualization
    visual = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if grid[r][c] == 1:
                row.append('█')  # Wall
            else:
                row.append('·')  # Floor
        visual.append(row)
    
    # Mark the path
    for pos in path:
        if pos != start and pos != goal:
            visual[pos[0]][pos[1]] = '•'
    
    # Mark start and goal
    visual[start[0]][start[1]] = 'S'
    visual[goal[0]][goal[1]] = 'G'
    
    # Print the grid
    print("   " + "".join(str(i) for i in range(cols)))
    for r, row in enumerate(visual):
        print(f"{r:2} " + "".join(row))


def find_path_in_dungeon(
    start: Tuple[int, int], 
    goal: Tuple[int, int],
    allow_diagonal: bool = False
) -> None:
    """Find and visualize a path through the dungeon."""
    dungeon = create_dungeon_map()
    
    try:
        distance, path = astar_grid_search(dungeon, start, goal, allow_diagonal)
        
        print(f"\n🎮 Game Pathfinding: {start} → {goal}")
        print("=" * 60)
        print(f"Movement: {'8-directional' if allow_diagonal else '4-directional (cardinal only)'}")
        print(f"Path length: {len(path)} steps")
        print(f"Total distance: {distance:.2f} units")
        print()
        
        visualize_path(dungeon, path, start, goal)
        
        print(f"\nPath coordinates: {' → '.join(str(p) for p in path)}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nDungeon map:")
        visualize_path(dungeon, [], start, goal)


def main():
    """Run game pathfinding examples."""
    print("🎮 Dungeon Crawler - AI Pathfinding System")
    print("=" * 60)
    print("Legend: S=Start, G=Goal, █=Wall, ·=Floor, •=Path")
    
    # Example 1: Simple path (cardinal directions only)
    print("\n\n📍 Example 1: Character moving to treasure")
    find_path_in_dungeon((0, 0), (9, 9), allow_diagonal=False)
    
    # Example 2: With diagonal movement
    print("\n\n📍 Example 2: Same path with diagonal movement")
    find_path_in_dungeon((0, 0), (9, 9), allow_diagonal=True)
    
    # Example 3: Navigating around obstacles
    print("\n\n📍 Example 3: Navigating through narrow corridor")
    find_path_in_dungeon((0, 5), (4, 9), allow_diagonal=False)
    
    # Example 4: Short path
    print("\n\n📍 Example 4: Quick escape route")
    find_path_in_dungeon((2, 2), (4, 7), allow_diagonal=True)


if __name__ == '__main__':
    main()

"""Social Network Analysis using BFS

Real-world example: Finding connections and distances in a social network.
"""

from typing import Dict, List, Set
from src.bfs import bfs_shortest_path, bfs_all_paths, bfs_connected_components


def create_social_network() -> Dict[str, List[str]]:
    """
    Create a social network graph representing friendships.
    This is an undirected graph (friendships are bidirectional).
    """
    # Define friendships (we'll make it bidirectional)
    friendships = {
        'Alice': ['Bob', 'Charlie', 'Diana'],
        'Bob': ['Alice', 'Charlie', 'Eve'],
        'Charlie': ['Alice', 'Bob', 'Frank'],
        'Diana': ['Alice', 'Grace'],
        'Eve': ['Bob', 'Frank', 'Henry'],
        'Frank': ['Charlie', 'Eve', 'Grace'],
        'Grace': ['Diana', 'Frank', 'Henry'],
        'Henry': ['Eve', 'Grace', 'Ivan'],
        'Ivan': ['Henry', 'Jack'],
        'Jack': ['Ivan'],
        # Separate component
        'Kate': ['Leo', 'Mike'],
        'Leo': ['Kate', 'Mike'],
        'Mike': ['Kate', 'Leo'],
        # Isolated node
        'Nina': []
    }
    
    return friendships


def find_connection(person1: str, person2: str, network: Dict[str, List[str]]) -> None:
    """Find and display the connection between two people."""
    try:
        distance, path = bfs_shortest_path(network, person1, person2)
        
        print(f"\n👥 Connection: {person1} ↔ {person2}")
        print("=" * 60)
        print(f"🔗 Degrees of separation: {distance}")
        print(f"📍 Path: {' → '.join(path)}")
        
        if distance == 1:
            print("💬 They are direct friends!")
        elif distance == 2:
            print(f"💬 They have a mutual friend: {path[1]}")
        else:
            print(f"💬 Connection through {distance - 1} intermediaries")
            
    except ValueError:
        print(f"\n❌ No connection exists between {person1} and {person2}")


def find_all_connections(person1: str, person2: str, network: Dict[str, List[str]]) -> None:
    """Find all shortest paths between two people."""
    paths = bfs_all_paths(network, person1, person2, max_paths=5)
    
    if not paths:
        print(f"\n❌ No connection exists between {person1} and {person2}")
        return
    
    print(f"\n👥 All shortest connections: {person1} ↔ {person2}")
    print("=" * 60)
    print(f"🔗 Degrees of separation: {len(paths[0]) - 1}")
    print(f"📊 Number of shortest paths: {len(paths)}")
    print("\n📍 Paths:")
    
    for i, path in enumerate(paths, 1):
        print(f"   {i}. {' → '.join(path)}")


def analyze_network(network: Dict[str, List[str]]) -> None:
    """Analyze the social network structure."""
    print("\n📊 Network Analysis")
    print("=" * 60)
    
    # Find connected components
    components = bfs_connected_components(network)
    
    print(f"👥 Total people: {len(network)}")
    print(f"🔗 Total friendships: {sum(len(friends) for friends in network.values()) // 2}")
    print(f"🌐 Connected groups: {len(components)}")
    
    print("\n📍 Groups:")
    for i, component in enumerate(sorted(components, key=len, reverse=True), 1):
        members = sorted(component)
        print(f"   Group {i} ({len(members)} members): {', '.join(members)}")
    
    # Find most connected person
    most_connected = max(network.items(), key=lambda x: len(x[1]))
    print(f"\n⭐ Most connected person: {most_connected[0]} ({len(most_connected[1])} friends)")
    
    # Find isolated people
    isolated = [person for person, friends in network.items() if not friends]
    if isolated:
        print(f"😔 Isolated people: {', '.join(isolated)}")


def suggest_friends(person: str, network: Dict[str, List[str]]) -> None:
    """Suggest potential friends (friends of friends)."""
    if person not in network:
        print(f"❌ {person} not found in network")
        return
    
    # Get direct friends
    direct_friends = set(network[person])
    
    # Get friends of friends
    friends_of_friends: Set[str] = set()
    for friend in direct_friends:
        friends_of_friends.update(network[friend])
    
    # Remove self and direct friends
    suggestions = friends_of_friends - direct_friends - {person}
    
    print(f"\n💡 Friend suggestions for {person}")
    print("=" * 60)
    
    if not suggestions:
        print("   No suggestions available")
        return
    
    # Count mutual friends
    suggestion_scores = []
    for suggestion in suggestions:
        mutual = len(set(network[suggestion]) & direct_friends)
        suggestion_scores.append((suggestion, mutual))
    
    # Sort by number of mutual friends
    suggestion_scores.sort(key=lambda x: x[1], reverse=True)
    
    for suggested_person, mutual_count in suggestion_scores[:5]:
        mutual_friends = set(network[suggested_person]) & direct_friends
        print(f"   👤 {suggested_person}")
        print(f"      {mutual_count} mutual friend(s): {', '.join(sorted(mutual_friends))}")


def main():
    """Run social network analysis examples."""
    print("🌐 Social Network Analysis System")
    print("=" * 60)
    
    network = create_social_network()
    
    # Example 1: Find connection between two people
    find_connection('Alice', 'Jack', network)
    
    # Example 2: Find all shortest paths
    find_all_connections('Alice', 'Grace', network)
    
    # Example 3: Check direct friends
    find_connection('Alice', 'Bob', network)
    
    # Example 4: No connection (different components)
    find_connection('Alice', 'Kate', network)
    
    # Example 5: Analyze the entire network
    analyze_network(network)
    
    # Example 6: Friend suggestions
    suggest_friends('Alice', network)
    suggest_friends('Diana', network)
    
    # Example 7: Six degrees of separation
    print("\n\n🌍 Six Degrees of Separation Test")
    print("=" * 60)
    print("Testing the theory that everyone is connected within 6 steps...")
    
    people = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivan', 'Jack']
    max_separation = 0
    max_pair = None
    
    for i, person1 in enumerate(people):
        for person2 in people[i+1:]:
            try:
                distance, _ = bfs_shortest_path(network, person1, person2)
                if distance > max_separation:
                    max_separation = distance
                    max_pair = (person1, person2)
            except ValueError:
                pass
    
    if max_pair:
        print(f"Maximum separation in main network: {max_separation} degrees")
        print(f"Between: {max_pair[0]} and {max_pair[1]}")
        
        if max_separation <= 6:
            print("✅ Six degrees of separation holds!")
        else:
            print("❌ Exceeds six degrees of separation")


if __name__ == '__main__':
    main()

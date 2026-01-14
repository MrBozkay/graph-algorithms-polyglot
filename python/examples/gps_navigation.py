"""GPS Navigation Example using Dijkstra's Algorithm

Real-world example: Finding the shortest route between cities in Turkey.
"""

from typing import Dict
from src.dijkstra import dijkstra_path


def create_turkey_road_network() -> Dict[str, Dict[str, float]]:
    """
    Create a simplified road network of major Turkish cities.
    Distances are in kilometers.
    """
    return {
        'Istanbul': {
            'Edirne': 235,
            'Bursa': 155,
            'Ankara': 450,
            'Kocaeli': 100
        },
        'Edirne': {
            'Istanbul': 235,
            'Kırklareli': 90
        },
        'Kırklareli': {
            'Edirne': 90,
            'Istanbul': 210
        },
        'Bursa': {
            'Istanbul': 155,
            'Ankara': 380,
            'Eskişehir': 155,
            'Kocaeli': 140
        },
        'Kocaeli': {
            'Istanbul': 100,
            'Bursa': 140,
            'Ankara': 380
        },
        'Ankara': {
            'Istanbul': 450,
            'Bursa': 380,
            'Kocaeli': 380,
            'Eskişehir': 235,
            'Konya': 265,
            'Kayseri': 335
        },
        'Eskişehir': {
            'Bursa': 155,
            'Ankara': 235,
            'Konya': 330
        },
        'Konya': {
            'Ankara': 265,
            'Eskişehir': 330,
            'Kayseri': 335,
            'Antalya': 335
        },
        'Kayseri': {
            'Ankara': 335,
            'Konya': 335,
            'Adana': 265
        },
        'Adana': {
            'Kayseri': 265,
            'Mersin': 70,
            'Gaziantep': 220
        },
        'Mersin': {
            'Adana': 70,
            'Antalya': 480
        },
        'Antalya': {
            'Konya': 335,
            'Mersin': 480,
            'Burdur': 120
        },
        'Burdur': {
            'Antalya': 120,
            'Konya': 235
        },
        'Gaziantep': {
            'Adana': 220,
            'Şanlıurfa': 145
        },
        'Şanlıurfa': {
            'Gaziantep': 145,
            'Diyarbakır': 185
        },
        'Diyarbakır': {
            'Şanlıurfa': 185
        }
    }


def find_route(start: str, end: str) -> None:
    """Find and display the shortest route between two cities."""
    network = create_turkey_road_network()
    
    try:
        distance, path = dijkstra_path(network, start, end)
        
        print(f"\n🗺️  GPS Navigation: {start} → {end}")
        print("=" * 60)
        print(f"📍 Route: {' → '.join(path)}")
        print(f"📏 Total Distance: {distance:.0f} km")
        print(f"🚗 Estimated Time: {distance / 80:.1f} hours (at 80 km/h avg)")
        
        # Show step-by-step directions
        print("\n📋 Turn-by-turn directions:")
        for i in range(len(path) - 1):
            segment_distance = network[path[i]][path[i + 1]]
            print(f"   {i + 1}. {path[i]} → {path[i + 1]}: {segment_distance:.0f} km")
        
    except ValueError as e:
        print(f"❌ Error: {e}")


def main():
    """Run GPS navigation examples."""
    print("🇹🇷 Turkey Road Network - GPS Navigation System")
    print("=" * 60)
    
    # Example 1: Istanbul to Antalya
    find_route('Istanbul', 'Antalya')
    
    # Example 2: Ankara to Diyarbakır
    find_route('Ankara', 'Diyarbakır')
    
    # Example 3: Bursa to Mersin
    find_route('Bursa', 'Mersin')
    
    # Show all distances from Istanbul
    print("\n\n📊 All distances from Istanbul:")
    print("=" * 60)
    network = create_turkey_road_network()
    from src.dijkstra import dijkstra
    distances, _ = dijkstra(network, 'Istanbul')
    
    # Sort cities by distance
    sorted_cities = sorted(
        [(city, dist) for city, dist in distances.items() if dist != float('inf')],
        key=lambda x: x[1]
    )
    
    for city, dist in sorted_cities:
        if city != 'Istanbul':
            print(f"   {city:15} {dist:6.0f} km")


if __name__ == '__main__':
    main()

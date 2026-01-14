"""Currency Arbitrage Detection using Bellman-Ford Algorithm

Real-world example: Detecting profitable currency exchange cycles.
"""

import math
from typing import Dict, List, Optional
from src.bellman_ford import detect_negative_cycle


def create_currency_graph(exchange_rates: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    """
    Convert exchange rates to a graph with negative log weights.
    
    This transformation allows us to use Bellman-Ford to detect arbitrage:
    - Multiplying exchange rates becomes adding log values
    - A profitable cycle (product > 1) becomes a negative cycle (sum < 0)
    """
    graph = {}
    
    for from_currency in exchange_rates:
        graph[from_currency] = {}
        for to_currency, rate in exchange_rates[from_currency].items():
            # Use negative log to convert multiplication to addition
            # and profit detection to negative cycle detection
            graph[from_currency][to_currency] = -math.log(rate)
    
    return graph


def detect_arbitrage_opportunity(exchange_rates: Dict[str, Dict[str, float]]) -> Optional[List[str]]:
    """
    Detect if there's an arbitrage opportunity in the exchange rates.
    
    Args:
        exchange_rates: Dict of {currency: {other_currency: exchange_rate}}
        
    Returns:
        List of currencies forming an arbitrage cycle, or None if no opportunity exists
    """
    graph = create_currency_graph(exchange_rates)
    return detect_negative_cycle(graph)


def calculate_profit(cycle: List[str], exchange_rates: Dict[str, Dict[str, float]]) -> float:
    """Calculate the profit multiplier for an arbitrage cycle."""
    profit = 1.0
    
    for i in range(len(cycle) - 1):
        from_curr = cycle[i]
        to_curr = cycle[i + 1]
        rate = exchange_rates[from_curr][to_curr]
        profit *= rate
    
    return profit


def main():
    """Run currency arbitrage detection examples."""
    print("💱 Currency Arbitrage Detection System")
    print("=" * 60)
    
    # Example 1: No arbitrage opportunity
    print("\n📊 Example 1: Balanced market (no arbitrage)")
    print("-" * 60)
    
    balanced_rates = {
        'USD': {'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0},
        'EUR': {'USD': 1.18, 'GBP': 0.86, 'JPY': 129.5},
        'GBP': {'USD': 1.37, 'EUR': 1.16, 'JPY': 150.7},
        'JPY': {'USD': 0.0091, 'EUR': 0.0077, 'GBP': 0.0066}
    }
    
    cycle = detect_arbitrage_opportunity(balanced_rates)
    if cycle:
        profit = calculate_profit(cycle, balanced_rates)
        print(f"✅ Arbitrage found: {' → '.join(cycle)}")
        print(f"💰 Profit: {(profit - 1) * 100:.2f}%")
    else:
        print("❌ No arbitrage opportunity found")
    
    # Example 2: Arbitrage opportunity exists
    print("\n\n📊 Example 2: Market inefficiency (arbitrage exists)")
    print("-" * 60)
    
    arbitrage_rates = {
        'USD': {'EUR': 0.85, 'GBP': 0.73, 'TRY': 28.5},
        'EUR': {'USD': 1.18, 'GBP': 0.86, 'TRY': 33.5},
        'GBP': {'USD': 1.40, 'EUR': 1.16, 'TRY': 39.0},  # Slightly inflated
        'TRY': {'USD': 0.0351, 'EUR': 0.0299, 'GBP': 0.0257}
    }
    
    cycle = detect_arbitrage_opportunity(arbitrage_rates)
    if cycle:
        profit = calculate_profit(cycle, arbitrage_rates)
        print(f"✅ Arbitrage found: {' → '.join(cycle)}")
        print(f"💰 Profit multiplier: {profit:.6f}")
        print(f"💰 Profit percentage: {(profit - 1) * 100:.4f}%")
        
        # Show the calculation
        print("\n📝 Calculation:")
        initial_amount = 1000
        amount = initial_amount
        for i in range(len(cycle) - 1):
            from_curr = cycle[i]
            to_curr = cycle[i + 1]
            rate = arbitrage_rates[from_curr][to_curr]
            new_amount = amount * rate
            print(f"   {amount:.2f} {from_curr} × {rate:.6f} = {new_amount:.2f} {to_curr}")
            amount = new_amount
        
        print(f"\n💵 Starting with: {initial_amount:.2f} {cycle[0]}")
        print(f"💵 Ending with: {amount:.2f} {cycle[0]}")
        print(f"💵 Profit: {amount - initial_amount:.2f} {cycle[0]}")
    else:
        print("❌ No arbitrage opportunity found")
    
    # Example 3: Three-currency arbitrage
    print("\n\n📊 Example 3: Classic triangular arbitrage")
    print("-" * 60)
    
    triangular_rates = {
        'USD': {'EUR': 0.90, 'GBP': 0.75},
        'EUR': {'USD': 1.10, 'GBP': 0.85},
        'GBP': {'USD': 1.35, 'EUR': 1.18}  # Creates arbitrage
    }
    
    cycle = detect_arbitrage_opportunity(triangular_rates)
    if cycle:
        profit = calculate_profit(cycle, triangular_rates)
        print(f"✅ Triangular arbitrage found: {' → '.join(cycle)}")
        print(f"💰 Profit: {(profit - 1) * 100:.4f}%")
        
        # Demonstrate with $10,000
        print(f"\n💡 Example with $10,000:")
        amount = 10000
        for i in range(len(cycle) - 1):
            from_curr = cycle[i]
            to_curr = cycle[i + 1]
            rate = triangular_rates[from_curr][to_curr]
            new_amount = amount * rate
            print(f"   {from_curr} → {to_curr}: ${amount:,.2f} → ${new_amount:,.2f}")
            amount = new_amount
        print(f"   Final profit: ${amount - 10000:,.2f}")
    else:
        print("❌ No arbitrage opportunity found")
    
    # Example 4: Crypto arbitrage
    print("\n\n📊 Example 4: Cryptocurrency arbitrage")
    print("-" * 60)
    
    crypto_rates = {
        'BTC': {'ETH': 15.5, 'USDT': 45000},
        'ETH': {'BTC': 0.065, 'USDT': 2900},
        'USDT': {'BTC': 0.0000223, 'ETH': 0.000345}
    }
    
    cycle = detect_arbitrage_opportunity(crypto_rates)
    if cycle:
        profit = calculate_profit(cycle, crypto_rates)
        print(f"✅ Crypto arbitrage found: {' → '.join(cycle)}")
        print(f"💰 Profit: {(profit - 1) * 100:.4f}%")
    else:
        print("❌ No arbitrage opportunity found")
    
    print("\n\n⚠️  Note: In real markets, arbitrage opportunities are rare and")
    print("    quickly eliminated by automated trading systems. Transaction")
    print("    fees and slippage must also be considered.")


if __name__ == '__main__':
    main()

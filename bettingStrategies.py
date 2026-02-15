import random
import matplotlib.pyplot as plt
import numpy as np


def flat_betting(trials, bet_size=1):
    """Flat betting: bet the same amount every time."""
    money = 0
    for _ in range(trials):
        if random.choice([True, False]):
            money += bet_size
        else:
            money -= bet_size
    return money

def martingale(trials, base_bet=1, cap=1024):
    """Martingale: double bet after each loss until cap."""
    money = 0
    bet = base_bet
    for _ in range(trials):
        win = random.choice([True, False])
        if win:
            money += bet
            bet = base_bet
        else:
            money -= bet
            bet = min(bet * 2, cap)
    return money

def stop_loss(trials, stop_after=10):
    """Stop-loss: stop after a certain number of consecutive losses."""
    money = 0
    loss_streak = 0
    for _ in range(trials):
        if loss_streak >= stop_after:
            break
        win = random.choice([True, False])
        if win:
            money += 1
            loss_streak = 0
        else:
            money -= 1
            loss_streak += 1
    return money

def random_betting(trials, max_bet=5):
    """Random betting: bet a random amount each time."""
    money = 0
    for _ in range(trials):
        bet = random.randint(1, max_bet)
        win = random.choice([True, False])
        if win:
            money += bet
        else:
            money -= bet
    return money

def run_simulation(strategy_func, trials, runs, **kwargs):
    """
    Run a strategy multiple times and compute statistics:
    - average profit
    - standard deviation
    - max drawdown
    """
    profits = [strategy_func(trials, **kwargs) for _ in range(runs)]
    avg = np.mean(profits)
    std_dev = np.std(profits)
    max_loss = np.min(profits)
    sharpe_ratio = avg / std_dev if std_dev != 0 else float('inf')
    return {
        "profits": profits,
        "avg": avg,
        "std_dev": std_dev,
        "max_loss": max_loss,
        "sharpe_ratio": sharpe_ratio
    }

def optimize_martingale(trials, runs, caps=[16,32,64,128,256,512,1024]):
    """Find the best Martingale cap for expected return vs risk."""
    results = {}
    for cap in caps:
        stats = run_simulation(martingale, trials, runs, cap=cap)
        results[cap] = stats
    return results


def plot_histograms(strategy_results):
    """Plot profit distributions for each strategy."""
    plt.figure(figsize=(10,6))
    for name, stats in strategy_results.items():
        plt.hist(stats["profits"], bins=30, alpha=0.6, label=name)
    plt.xlabel("Profit")
    plt.ylabel("Frequency")
    plt.title("Profit Distribution by Strategy")
    plt.legend()
    plt.show()

def plot_martingale_caps(martingale_stats):
    """Show how expected profit and risk change with Martingale cap."""
    caps = sorted(martingale_stats.keys())
    avg_profits = [martingale_stats[cap]["avg"] for cap in caps]
    max_losses = [martingale_stats[cap]["max_loss"] for cap in caps]
    
    plt.figure(figsize=(10,5))
    plt.plot(caps, avg_profits, marker='o', label="Average Profit")
    plt.plot(caps, max_losses, marker='x', label="Max Loss")
    plt.xlabel("Martingale Cap")
    plt.ylabel("Profit / Loss")
    plt.title("Effect of Martingale Cap on Profit & Risk")
    plt.legend()
    plt.show()


def main():
    trials = 1000   # Bets per run
    runs = 500      # Simulation runs

    strategies = {
        "Flat Betting": flat_betting,
        "Martingale": martingale,
        "Stop-Loss": stop_loss,
        "Random Betting": random_betting
    }

    # Run simulations
    strategy_results = {}
    print("Running simulations...\n")
    for name, func in strategies.items():
        stats = run_simulation(func, trials, runs)
        strategy_results[name] = stats
        print("{}: Avg={:.2f}, Std={:.2f}, Max Loss={}, Sharpe={:.2f}".format(name, stats['avg'], stats['std_dev'], stats['max_loss'], stats['sharpe_ratio']
))


    # Visualize distributions
    plot_histograms(strategy_results)

    # Optimize Martingale caps
    print("\nOptimizing Martingale caps...")
    caps = [16, 32, 64, 128, 256, 512, 1024]
    martingale_stats = optimize_martingale(trials, runs, caps=caps)
    for cap, stats in martingale_stats.items():
        print("Cap {}: Avg={:.2f}, Max Loss={}".format(cap, stats['avg'], stats['max_loss']))
        plot_martingale_caps(martingale_stats)

if __name__ == "__main__":
    main()

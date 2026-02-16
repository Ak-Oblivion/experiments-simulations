import itertools
import random
import math

# ---------- Exact Probability Functions ----------
def dice_sum_probability(dice, target):
    total_outcomes = 6 ** dice
    favorable = 0
    for outcome in itertools.product(range(1, 7), repeat=dice):
        if sum(outcome) == target:
            favorable += 1
    return favorable / float(total_outcomes)  # force float division

def combination(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

def probability_k_heads(n, k):
    return combination(n, k) / float(2 ** n)  # force float division

# ---------- Monte Carlo Simulation ----------
def monte_carlo_dice(dice, target, trials=100000):
    hits = 0
    for _ in range(trials):
        if sum(random.randint(1, 6) for _ in range(dice)) == target:
            hits += 1
    return hits / float(trials)  # force float division

# ---------- Expected Value Game ----------
def expected_value_coin_game():
    return 0.5 * 1 + 0.5 * (-1)

# ---------- Example Outputs ----------
print("Probability of sum 10 with 3 dice (exact):", dice_sum_probability(3, 10))
print("Probability of sum 10 with 3 dice (MC):", monte_carlo_dice(3, 10))
print("Probability of exactly 3 heads in 5 flips:", probability_k_heads(5, 3))
print("EV of coin game:", expected_value_coin_game())

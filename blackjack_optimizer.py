import random
import numpy as np
import matplotlib.pyplot as plt

# ---------- Card / Hand Functions ----------
def draw_card():
    cards = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    return random.choice(cards)

def hand_value(hand):
    total = sum(hand)
    aces = hand.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

# ---------- Play One Hand ----------
def play_hand(hit_threshold):
    player = [draw_card(), draw_card()]
    dealer = [draw_card(), draw_card()]

    # Player hits until threshold
    while True:
        p_val = hand_value(player)
        if p_val >= hit_threshold:
            break
        player.append(draw_card())
        p_val = hand_value(player)
        if p_val > 21:
            return -1

    # Dealer hits until 17
    while True:
        d_val = hand_value(dealer)
        if d_val >= 17:
            break
        dealer.append(draw_card())
        d_val = hand_value(dealer)

    # Determine outcome
    if d_val > 21 or p_val > d_val:
        return 1
    elif p_val < d_val:
        return -1
    else:
        return 0

# ---------- Simulate Strategy ----------
def simulate_strategy(threshold, rounds=5000):
    results = [play_hand(threshold) for _ in range(rounds)]
    avg_ev = np.mean(results)
    std_ev = np.std(results)
    return avg_ev, std_ev

# ---------- Test Thresholds ----------
thresholds = range(12, 21)
evs = []
stds = []

for t in thresholds:
    avg, std = simulate_strategy(t)
    evs.append(avg)
    stds.append(std)
    print("Threshold {}: EV = {:.4f}, Std = {:.4f}".format(t, avg, std))

# ---------- Plot Results ----------
plt.figure(figsize=(8,5))
plt.errorbar(thresholds, evs, yerr=stds, fmt='o-', capsize=5)
plt.xlabel("Hit Threshold")
plt.ylabel("Expected Profit per Hand")
plt.title("Blackjack Strategy: Expected Value +/- Standard Deviation")
plt.grid(True)
plt.show()

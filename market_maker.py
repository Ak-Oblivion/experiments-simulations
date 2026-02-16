import numpy as np
import matplotlib.pyplot as plt

# this class represents our market maker
# it will place buy and sell quotes and track inventory and cash
class MarketMaker:
    def __init__(self, spread=1.0, inventory_limit=10, risk_aversion=0.01):
        # spread is the distance between bid and ask
        self.spread = spread
        
        # this is the max number of shares we allow ourselves to hold
        self.inventory_limit = inventory_limit
        
        # risk aversion controls how much we adjust quotes when inventory grows
        self.risk_aversion = risk_aversion
        
        # current number of shares we hold
        self.inventory = 0
        
        # cash we have made or lost
        self.cash = 0

    # this function calculates our bid and ask quotes
    def quote(self, price):
        # if we hold too many shares we want to push quotes to reduce risk
        inventory_adjustment = self.risk_aversion * self.inventory
        
        # bid is where we buy
        bid = price - self.spread/2 - inventory_adjustment
        
        # ask is where we sell
        ask = price + self.spread/2 - inventory_adjustment
        
        return bid, ask

    # this function handles trades from the market
    def trade(self, order_type, price):
        # get current bid and ask
        bid, ask = self.quote(price)

        # if someone buys from us
        if order_type == "buy" and self.inventory > -self.inventory_limit:
            # we sell one unit
            self.inventory -= 1
            # we receive cash at the ask price
            self.cash += ask

        # if someone sells to us
        elif order_type == "sell" and self.inventory < self.inventory_limit:
            # we buy one unit
            self.inventory += 1
            # we pay cash at the bid price
            self.cash -= bid

    # this computes total profit and loss
    # we combine cash and value of inventory
    def pnl(self, price):
        return self.cash + self.inventory * price


# this runs the full simulation
def simulate(steps=2000):
    # start price
    price = 100
    
    # create our market maker
    maker = MarketMaker(spread=1.0, inventory_limit=15, risk_aversion=0.05)

    prices = []
    pnls = []

    for _ in range(steps):
        # price moves randomly
        price += np.random.normal(0, 0.5)

        # random order from traders
        order = np.random.choice(["buy", "sell", None], p=[0.4, 0.4, 0.2])
        
        # process the trade
        maker.trade(order, price)

        prices.append(price)
        pnls.append(maker.pnl(price))

    return prices, pnls


# this computes sharpe ratio
# which is average return divided by risk
def sharpe_ratio(pnls):
    returns = np.diff(pnls)
    if np.std(returns) == 0:
        return 0
    return np.mean(returns) / np.std(returns)


# run the simulation
prices, pnls = simulate()

# print final results
print("Final P&L:", pnls[-1])
print("Sharpe Ratio:", sharpe_ratio(pnls))

# plot the profit over time
plt.figure()
plt.plot(pnls)
plt.title("Market Maker P&L")
plt.xlabel("Time")
plt.ylabel("P&L")
plt.show()

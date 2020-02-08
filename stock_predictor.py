import sys
import numpy as np
import os
from sklearn import linear_model
import math
import operator

stock_data = {} # This holds our working stock price data
inputlines = sys.stdin.readlines() # This is our input

# We want to judge based on more than the past five days, so store data in files and read them in every turn
for i in os.listdir():
    # Get all txt files assuming there are no other txt files other than the ones we've created
    if i.endswith('.txt'):
        i_file = open(i, 'r')
        stock_name = i[:-4] # Everything up until .txt is the name of the stock
        stock_prices = i_file.readlines() # stock prices written sequentially
        stock_data[stock_name] = []
        for j in stock_prices:
            stock_data[stock_name].append(float(j))
        i_file.close()

# Remove newline characters at the end of input lines
for i in range(len(inputlines)):
    inputlines[i] = inputlines[i].rstrip()

constraints_line = inputlines[0]
money_available, num_stocks_available, remaining_days = constraints_line.split(' ')

# Adjusting constraints to right data types
money_available = float(money_available)
num_stocks_available = int(num_stocks_available)
remaining_days = int(remaining_days)

# Read input stock prices, store necessary values in working data and persistent memory
owned_data = {}

for i in range(1, len(inputlines)):
    name, owned, price1, price2, price3, price4, price5 = inputlines[i].split(' ')
    owned_data[name] = owned
    if name in stock_data.keys():
        stock_data[name].append(float(price5))
        i_file = open(name + '.txt', 'a')
        i_file.write(price5)
        i_file.write('\n')
        i_file.close()
    else:
        past_five_prices = [price1, price2, price3, price4, price5]
        past_five_prices = [float(pf) for pf in past_five_prices]
        stock_data[name] = past_five_prices
        i_file = open(name + '.txt', 'a')
        for j in past_five_prices:
            i_file.write(str(j))
            i_file.write('\n')
        i_file.close()


# Strategy 1
rainy_day_sum = 0.2 * money_available

stock_gain_predictions = {}
for stock_name, price_data in stock_data.items():
    model = linear_model.LinearRegression()
    indices = np.array([i for i in range(len(price_data))]).reshape(-1,1)
    price_data_np = np.array(price_data).reshape(-1,1)
    model.fit(indices, price_data_np)
    prediction = model.predict([[len(price_data)]])
    stock_gain_predictions[stock_name] = prediction.item(0) - price_data[-1]

best_stock = max(stock_gain_predictions.items(), key=operator.itemgetter(1))[0]

if len(stock_data[best_stock]) < 10:
    if math.floor(money_available / stock_data[best_stock][-1]) > 0:
        print(1)
        print(best_stock + " BUY " + str(math.floor(money_available / stock_data[best_stock][-1])))
    else:
        print(0)
elif len(stock_data[best_stock]) == 10:
    print(best_stock + " SELL " + str(owned_data[best_stock]))

import pandas as pd
from data_handling import load_data
from indicators import calculate_macd, calculate_rsi
from strategy import apply_strategy
from transaction import Transaction
from performance import calculate_performance
from visualizations import visualize_backtest
 def backtest(data, macd_params, rsi_params, capital):
    # Initialize a DataFrame to store the performance of each strategy
    performance_df = pd.DataFrame()
     # Loop through each stock
    for stock in data.columns:
        # Get the country from the stock name
        country = stock.split("-")[0]
         # Calculate the MACD and RSI for the stock
        macd = calculate_macd(data[stock], *macd_params)
        rsi = calculate_rsi(data[stock], *rsi_params)
         # Loop through each strategy
        for strategy in ['macd', 'rsi', 'macd_rsi']:
            # Apply the strategy to generate signals
            signals = apply_strategy(data[stock], macd, rsi, strategy)
             # Execute trades based on the signals
            trades = execute_trades(signals, capital, country)
             # Calculate the performance metrics of the strategy
            performance = calculate_performance(trades)
             # Add the performance to the DataFrame
            performance_df = pd.concat([performance_df, performance])
     return performance_df
 def execute_trades(signals, capital, country):
    # Initialize a DataFrame to store the trades
    trades_df = pd.DataFrame()
     # Loop through each signal
    for index, signal in signals.iterrows():
        # If the signal is to buy
        if signal['Signal'] == 'Buy':
            # Calculate the number of shares to buy
            shares = capital // signal['Price']
             # Add the transaction fee
            capital -= Transaction.apply_fee(country, shares * signal['Price'])
             # Add the trade to the DataFrame
            trades_df = trades_df.append({'Date': index, 'Shares': shares, 'Price': signal['Price'], 'Action': 'Buy'}, ignore_index=True)
         # If the signal is to sell
        elif signal['Signal'] == 'Sell' and not trades_df.empty and trades_df.iloc[-1]['Action'] == 'Buy':
            # Calculate the trade value
            trade_value = trades_df.iloc[-1]['Shares'] * signal['Price']
             # Add the transaction fee
            capital -= Transaction.apply_fee(country, trade_value)
             # Add the trade to the DataFrame
            trades_df = trades_df.append({'Date': index, 'Shares': trades_df.iloc[-1]['Shares'], 'Price': signal['Price'], 'Action': 'Sell'}, ignore_index=True)
     return trades_df
 # Load your data using the function provided in 'data_handling.py'
filepath = "C:\\Users\\abdul\\Downloads\\Abdelgadir\\Final_Python\\DISS\\Data.xlsx"
data = load_data(filepath)
 # Visualize the backtest results
performance_df = backtest(data, macd_params, rsi_params, capital)
visualize_backtest(performance_df)
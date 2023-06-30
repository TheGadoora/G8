import numpy as np
from itertools import product
from indicators import calculate_macd, calculate_rsi
from data_handling import load_data

# Define the MACD and RSI parameters
macd_params = [(12,26,9), (12,26,12), (9,26,9), (20,50,10), (5,35,5), (6,19,6), (50,200,50), (19,39,19), (8, 17,9), (12,26,14)]
rsi_params = [(7,50,50), (14,50,50), (21,50,50), (7,70,30), (14,70,30), (21,70,30), (14,40,40), (14,70,35), (14,60,30), (14,80,20)]

def calculate_signals(data, macd_params, rsi_params):
    """
    Calculate signals for each combination of MACD and RSI parameters, including MACD only, RSI only, and MACD-RSI combined.

    :param df: DataFrame with price data
    :param macd_params: List of tuples, each containing a set of MACD parameters
    :param rsi_params: List of tuples, each containing a set of RSI parameters
    :return: DataFrame with signals for each set of parameters
    """
    df_copy = data.copy()

    # For each column (stock), calculate the signals
    for stock in df_copy.columns:
        
        # MACD only signals
        for macd_param in macd_params:
            macd = calculate_macd(df_copy[stock], *macd_param)
            buy_signals = (macd['MACD'] > macd['Signal_Line'])
            sell_signals = (macd['MACD'] < macd['Signal_Line'])
            df_copy[f'{stock}_macd_{macd_param}_signals'] = np.where(buy_signals, 1, np.where(sell_signals, -1, 0))
        
        # RSI only signals
        for rsi_param in rsi_params:
            rsi = calculate_rsi(df_copy[stock], *rsi_param)
            overbought = (rsi > rsi_param[1])
            oversold = (rsi < rsi_param[2])
            df_copy[f'{stock}_rsi_{rsi_param}_signals'] = np.where(overbought, -1, np.where(oversold, 1, 0))
            
            # MACD-RSI combined signals
        for macd_param, rsi_param in product(macd_params, rsi_params):
            macd = calculate_macd(df_copy[stock], *macd_param)
            rsi = calculate_rsi(df_copy[stock], *rsi_param)
            buy_signals = (macd['MACD'] > macd['Signal_Line']) & (rsi < rsi_param[2])
            sell_signals = (macd['MACD'] < macd['Signal_Line']) & (rsi > rsi_param[1])
            df_copy[f'{stock}_macd_{macd_param}_rsi_{rsi_param}_signals'] = np.where(buy_signals, 1, np.where(sell_signals, -1, 0))
    
    return df_copy

# Load your data using the function provided in 'data_handling.py'
filepath = "C:\\Users\\abdul\\Downloads\\Abdelgadir\\Final_Python\\DISS\\Data.xlsx"
data = load_data(filepath)

# Generate the signals
signals_df = calculate_signals(data, macd_params, rsi_params)
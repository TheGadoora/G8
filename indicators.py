import pandas as pd
from data_handling import load_data

# Load your data using the function provided in 'data_handling.py'
filepath = "C:\\Users\\abdul\\Downloads\\Abdelgadir\\Final_Python\\DISS\\Data.xlsx"
data = load_data(filepath)

def calculate_macd(data, short_term, long_term, signal):
    # Calculate the Short Term EMA
    ShortEMA = data.ewm(span=short_term, adjust=False).mean() 

    # Calculate the Long Term EMA
    LongEMA = data.ewm(span=long_term, adjust=False).mean() 

    # Calculate the MACD line
    MACD = ShortEMA - LongEMA
    
    # Calculate the signal line
    signal_line = MACD.ewm(span=signal, adjust=False).mean()
    
    # Return a DataFrame with MACD and Signal line
    return pd.DataFrame({'MACD': MACD, 'Signal_Line': signal_line})

def calculate_rsi(data, period, overbought, oversold):
    # Get the difference in price from the previous day
    delta = data.diff()
    
    # Get rid of the first row, which is NaN since it did not have a previous row to calculate the differences
    delta = delta[1:] 

    # Make the positive gains (up) and negative gains (down) series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the EWMA
    AVG_Gain = up.ewm(com=(period - 1), min_periods=period).mean()
    AVG_Loss = abs(down.ewm(com=(period - 1), min_periods=period).mean())

    # Calculate the RS
    RS = AVG_Gain / AVG_Loss

    # Calculate the RSI
    RSI = 100.0 - (100.0 / (1.0 + RS))

    # Create a DataFrame to return RSI and thresholds
    RSI_df = pd.DataFrame({'RSI': RSI})
    
    return RSI_df

from data_handling import load_data
from backtest import backtest
from visualizations import visualize_backtest

# Load the data
data = load_data("C:\\Users\\abdul\\Downloads\\Abdelgadir\\Final_Python\\DISS\\Data.xlsx")

# Define the MACD parameters
macd_params = [(12,26,9), (12,26,12), (9,26,9), (20,50,10), (5,35,5), (6,19,6), (50,200,50), (19,39,19), (8, 17,9), (12,26,14)]

# Define the RSI parameters
rsi_params = [(7,50,50), (14,50,50), (21,50,50), (7,70,30), (14,70,30), (21,70,30), (14,40,40), (14,70,35), (14,60,30), (14,80,20)]

# Define the starting capital
capital = 100000

# Run the backtest
performance_df = backtest(data, macd_params, rsi_params, capital)

# Visualize the backtest results
visualize_backtest(performance_df)

# Save the performance dataframe to an Excel file
performance_df.to_excel("performance_results.xlsx")

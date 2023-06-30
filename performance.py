import pandas as pd
import numpy as np
from data_handling import load_data
from transaction import Transaction

# Load the data
data = load_data("C:\\Users\\abdul\\Downloads\\Abdelgadir\\Final_Python\\DISS\\Data.xlsx")

# Risk-free rates per country
rf_rates = {
    "Bahrain": 0.012,
    "UAE": 0.008,
    "Qatar": 0.029,
    "Oman": 0.017,
    "Kuwait": 0.0225,
    "KSA": 0.0075
}

def calculate_performance(data, signals_df):
    results = {}

    for col in signals_df.columns:
        if 'signals' not in col:
            continue

        stock_name, _, strategy_type, strategy_id = col.split('_')

        # Calculate returns
        data[f'{stock_name}_returns'] = data[stock_name].pct_change()
        data[f'{stock_name}_strategy_returns'] = signals_df[col] * data[f'{stock_name}_returns']

        # Apply transaction fees
        country = stock_name.split('-')[0]
        data[f'{stock_name}_strategy_returns'] = data[f'{stock_name}_strategy_returns'].apply(lambda x: Transaction.apply_fee(country, x))

        # Calculate metrics
        mean_return = data[f'{stock_name}_strategy_returns'].mean()
        std_return = data[f'{stock_name}_strategy_returns'].std()
        total_return = (1 + data[f'{stock_name}_strategy_returns']).cumprod()[-1] - 1
        sharpe_ratio = (mean_return - rf_rates[country]) / std_return
        sortino_ratio = (mean_return - rf_rates[country]) / data[data[f'{stock_name}_strategy_returns'] < 0][f'{stock_name}_strategy_returns'].std()
        total_trades = signals_df[col].abs().sum()
        bh_return = data[f'{stock_name}_returns'].mean()

        # Calculate X-statistic
        N = len(data)
        f = total_trades / N
        X_statistic = (mean_return - bh_return) / (std_return * np.sqrt(f * (1 - f) * N))

        results[f'{stock_name}_{strategy_type}_{strategy_id}'] = {
            'mean_return': mean_return,
            'total_return': total_return,
            'std_return': std_return,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'total_trades': total_trades,
            'X_statistic': X_statistic
        }

    return pd.DataFrame(results)

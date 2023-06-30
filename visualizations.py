import matplotlib.pyplot as plt

def visualize_backtest(df, strategy_names):
    """
    Generates plots given backtest results.

    :param df: DataFrame with backtest results
    :param strategy_names: List of strategy names
    """
    # Cumulative Returns Over Time
    plt.figure(figsize=(10, 5))
    for strategy in strategy_names:
        plt.plot(df.index, df[f'{strategy}_strategy_returns'].cumsum(), label=strategy)
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.title('Cumulative Returns Over Time')
    plt.legend()
    plt.show()

    # Histogram of Returns
    for strategy in strategy_names:
        plt.figure(figsize=(10, 5))
        plt.hist(df[f'{strategy}_strategy_returns'].dropna(), bins=50, alpha=0.75, label=strategy)
        plt.xlabel('Returns')
        plt.ylabel('Frequency')
        plt.title(f'Returns Distribution ({strategy})')
        plt.legend()
        plt.show()

    # Sharpe Ratio Bar Plot
    sharpe_ratios = [df[f'{strategy}_sharpe_ratio'].mean() for strategy in strategy_names]
    plt.figure(figsize=(10, 5))
    plt.bar(strategy_names, sharpe_ratios, alpha=0.75)
    plt.xlabel('Strategy')
    plt.ylabel('Sharpe Ratio')
    plt.title('Sharpe Ratios of Strategies')
    plt.show()

    # Total Trades Bar Plot
    total_trades = [df[f'{strategy}_total_trades'].sum() for strategy in strategy_names]
    plt.figure(figsize=(10, 5))
    plt.bar(strategy_names, total_trades, alpha=0.75)
    plt.xlabel('Strategy')
    plt.ylabel('Total Trades')
    plt.title('Total Trades of Strategies')
    plt.show()

# MACD Strategy Trading Bot

This project is a trading bot built using the [Lumibot](https://lumibot.com/) framework and the Alpaca trading API. The bot implements a trading strategy based on the Moving Average Convergence Divergence (MACD) indicator, combined with a 200-day Exponential Moving Average (EMA) filter, to generate buy and sell signals for the AAPL stock.

## Features

-   **MACD-Based Strategy**: The bot uses the MACD indicator to identify potential buy and sell opportunities.
-   **Trend Confirmation**: It incorporates a 200-day EMA to confirm the trend before making trades.
-   **Automated Trading**: Trades are automatically executed using Alpaca as the broker.
-   **Backtesting**: The bot can be backtested on historical data using Yahoo Finance data.
-   **Environment Configuration**: API keys and other configurations are managed through environment variables.

## Requirements

-   Python 3.8 or higher
-   Lumibot
-   Alpaca API Account (with API key and secret)
-   Pandas
-   NumPy
-   Dotenv

## Setup

1.  **Clone the repository**:
    
    bash
    
    Copy code
    
    `git clone https://github.com/yourusername/macd-strategy-bot.git
    cd macd-strategy-bot` 
    
2.  **Install the required Python packages**:
    
    bash
    
    Copy code
    
    `pip install lumibot pandas numpy python-dotenv` 
    
3.  **Set up your environment variables**:
    
    Create a `.env` file in the root directory and add your Alpaca API credentials:
    
    plaintext
    
    Copy code
    
    `API_KEY=your_alpaca_api_key
    API_SECRET=your_alpaca_api_secret` 
    
4.  **Configure Alpaca**:
    
    The `ALPACA_CONFIG` dictionary in the script uses your API key and secret to set up the connection to Alpaca. Make sure your keys are correct and that your account is set to paper trading (`PAPER: True`).
    

## Usage

### Running the Bot in Live Trading Mode

To run the bot in live trading mode, set the `trade` variable in the `__main__` block to `True`:

python

Copy code

`if __name__ == "__main__":
    trade = True
    if trade:
        # run strategy through Alpaca
        alpaca = Alpaca(ALPACA_CONFIG)
        strategy = MACDStrategy(broker=alpaca)
        trader = Trader()
        trader.add_strategy(strategy)
        trader.run_all()` 

### Backtesting the Strategy

To backtest the strategy, set the `trade` variable to `False` and specify the backtesting period:

python

Copy code

`if __name__ == "__main__":
    trade = False
    if trade:
        alpaca = Alpaca(ALPACA_CONFIG)
        strategy = MACDStrategy(broker=alpaca)
        trader = Trader()
        trader.add_strategy(strategy)
        trader.run_all()
    else:
        # Create a backtest
        backtesting_start = datetime(2015, 4, 15)
        backtesting_end = datetime(2023, 4, 15)

        MACDStrategy.backtest(
            YahooDataBacktesting,
            backtesting_start,
            backtesting_end,
        )` 

### Strategy Details

-   **MACD**: The MACD is calculated using a 12-day EMA, a 26-day EMA, and a 9-day signal line.
-   **200-day EMA**: The strategy uses a 200-day EMA to determine the overall market trend. Only buy signals are considered when the price is above the 200-day EMA, and sell signals are considered when the price is below.
-   **Position Management**: The bot will buy the stock if no position is currently held when a buy signal is triggered. It will sell the entire position when a sell signal is triggered.

## Contributing

Feel free to open issues or submit pull requests if you have any suggestions or improvements.

## License

This project is licensed under the MIT License.
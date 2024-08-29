from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime, date
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import os

# Load the environment variables from the .env file
load_dotenv()

# Get the API key and secret from the environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

ALPACA_CONFIG = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

class MACDStrategy(Strategy):
    def initialize(self):
        self.symbol = "SPY"
        self.signal = None
        self.sleeptime = "1D"       
    
    def on_trading_iteration(self):   
        # MACD SIGNAL LOGIC DONE
        bars = self.get_historical_prices(self.symbol, 1000, "day")
        data = bars.df 
        data['ema12'] = data['close'].ewm(span=12).mean()
        data['ema26'] = data['close'].ewm(span=26).mean()
        data['macd'] = data['ema12'] - data['ema26']
        data['signal'] = data['macd'].ewm(span=9).mean()
        data['ema200'] = data['close'].ewm(span=200).mean()   
        result = data.iloc[-1]
        if result.macd > result.signal and result.macd < 0:
            self.signal = "BUY"
        elif result.signal > result.macd and result.signal > 0:
            self.signal = "SELL"
        else:
            self.signal = None

        quantity = 200
        hasStock = self.get_position(self.symbol)
        if self.signal == 'BUY':
            if hasStock is None:
                order = self.create_order(self.symbol, quantity, "buy")
                self.submit_order(order)

        elif self.signal == 'SELL':
            if hasStock is not None:
                order = self.create_order(self.symbol, quantity, "sell")
                self.submit_order(order)
                
            
if __name__ == "__main__":
    trade = False
    if trade:
        # run strategy through alpaca
        alpaca = Alpaca(ALPACA_CONFIG)
        strategy = MACDStrategy(broker=alpaca)
        trader = Trader()
        trader.add_strategy(strategy)
        trader.run_all()
    else:
        # Create a backtest
        backtesting_start = datetime(2022, 4, 15)
        backtesting_end = datetime(2023, 4, 15)

        MACDStrategy.backtest(
            YahooDataBacktesting,
            backtesting_start,
            backtesting_end,
        )

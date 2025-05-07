from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.traders import Trader
from lumibot.strategies.strategy import Strategy
from datetime import datetime

API_KEY = ''
SECRET_KEY = ''
BASE_URL = 'https://paper-api.alpaca.markets/v2'

credentials = {
    'API_KEY': API_KEY,
    'API_SECRET': SECRET_KEY,
    'PAPER': True
}

start_date = datetime(2020, 1, 1)
end_date = datetime(2021, 1, 1)

"""
- cash at risk is the percentage of the account that is at risk for each trade.
- 0.5 means 50% of the account is at risk for each trade.
"""
params = {'symbol': 'SPY', 'cash_at_risk': 0.5}


class BaselineStrategy(Strategy):
    def initialize(self, symbol:str = 'SPY', cash_at_risk:float = 0.5):
        self.symbol = symbol
        self.sleep_time = '24H'
        self.last_trade = None
        self.cash_at_risk = cash_at_risk

    def position_size(self):
        """
        Calculate the position size based on the account balance and the symbol's price
        """
        cash = self.get_cash()
        price = self.get_last_price(self.symbol)
        quantity = round((self.cash_at_risk * cash) / price, 0)
        return cash, price, quantity
    
    def on_trading_iteration(self):
        cash, price, quantity = self.position_size()
        
        if price < cash:
            if self.last_trade is None:
                order = self.create_order(self.symbol, quantity, 'buy', 
                type='bracket', take_profit_price=(price * 1.20), stop_loss_price=(price * 0.95))
                self.submit_order(order)
                self.last_trade = order
                self.log_message(f'First trade: {order}')
    


broker = Alpaca(credentials)
strategy = BaselineStrategy(name='mlstrat', broker=broker, 
params=params)
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters=params,
    show_tearsheet=False
)
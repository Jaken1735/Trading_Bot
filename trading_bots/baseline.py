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


class BaselineStrategy(Strategy):
    def initialize(self, symbol:str = 'SPY'):
        self.symbol = symbol
        self.sleep_time = '24H'
        self.last_trade = None
    
    def on_trading_iteration(self):
        if self.last_trade is None:
            order = self.create_order(self.symbol, 10, 'buy', type='market')
            self.submit_order(order)
            self.last_trade = order
            self.log_message(f'First trade: {order}')
    


broker = Alpaca(credentials)
strategy = BaselineStrategy(name='mlstrat', broker=broker, params={})
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={},
    show_tearsheet=False
)









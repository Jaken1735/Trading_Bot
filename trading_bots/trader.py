from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.traders import Trader
from lumibot.strategies.strategy import Strategy
from datetime import datetime, timedelta
from alpaca_trade_api import REST
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from finbert_utils import calculate_sentiment

API_KEY = ''
SECRET_KEY = ''
BASE_URL = 'https://paper-api.alpaca.markets/v2'

credentials = {
    'API_KEY': API_KEY,
    'API_SECRET': SECRET_KEY,
    'PAPER': True
}

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

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
        self.api = REST(key_id=API_KEY, secret_key=SECRET_KEY, base_url=BASE_URL)

    def position_size(self):
        """
        Calculate the position size based on the account balance and the symbol's price
        """
        cash = self.get_cash()
        price = self.get_last_price(self.symbol)
        quantity = round((self.cash_at_risk * cash) / price, 0)
        return cash, price, quantity

    def get_dates(self):
        """
        Fetch the current date with respect to the backtesting start date
        """
        today = self.get_datetime()
        three_days_prior = today - timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self):
        """
        Get the sentiment for the symbol
        """
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
        news = [event.__dict__['_raw']['headline'] for event in news]
        probability, sentiment = calculate_sentiment(news)
        return probability, sentiment
    
    def on_trading_iteration(self):
        cash, price, quantity = self.position_size()
        probability, sentiment = self.get_sentiment()


        if price < cash:
            if sentiment == 'positive' and probability > 0.999:

                if self.last_trade == 'sell':
                    self.sell_all()

                order = self.create_order(self.symbol, quantity, 'buy', 
                type='bracket', take_profit_price=(price * 1.20), stop_loss_price=(price * 0.95))
                self.submit_order(order)
                self.last_trade = 'buy'
                self.log_message(f'First trade: {order}')
            
            if sentiment == 'negative' and probability > 0.999:

                if self.last_trade == 'buy':
                    self.sell_all()

                order = self.create_order(self.symbol, quantity, 'sell', 
                type='bracket', take_profit_price=(price * 0.8), stop_loss_price=(price * 1.05))
                self.submit_order(order)
                self.last_trade = 'sell'
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
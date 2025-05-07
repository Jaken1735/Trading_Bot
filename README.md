# Trading Bot

A sentiment-based algorithmic trading system leveraging FinBERT for stock market prediction.

## Overview

This project implements a trading bot that makes buy/sell decisions based on sentiment analysis of financial news. It uses the FinBERT model to analyze news headlines and determine market sentiment (positive, negative, or neutral).

## Features

- Sentiment analysis of financial news using FinBERT
- Automated trading strategy based on sentiment scores
- Integration with Alpaca trading API
- Backtesting capabilities using historical data from Yahoo Finance
- Risk management through position sizing and stop-loss/take-profit orders

## Components

- **finbert_utils.py**: Utility functions for sentiment analysis using the FinBERT model
- **trading_bots/trader.py**: The main trading strategy implementing sentiment-based decisions
- **trading_bots/baseline.py**: A baseline trading strategy for comparison

## Requirements

```
lumibot==2.9.13
alpaca-trade-api==3.1.1
torch
torchvision
torchaudio
transformers
```

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your Alpaca API credentials in the strategy files
4. Run the trading bot or perform backtesting

## Usage

### Backtesting

The project includes backtesting functionality to evaluate the strategy against historical data:

```python
from trading_bots.trader import strategy
# Backtesting is configured in the strategy file
```

### Live Trading

To run the strategy with live trading:

```python
from lumibot.traders import Trader
from trading_bots.trader import strategy

trader = Trader()
trader.add_strategy(strategy)
trader.run_all()
```

## Trading Strategy

The main strategy:
1. Analyzes financial news headlines using FinBERT
2. Calculates sentiment probability (positive, negative, neutral)
3. Makes trading decisions based on sentiment:
   - Buy when sentiment is strongly positive (> 99.9% confidence)
   - Sell when sentiment is strongly negative (> 99.9% confidence)
4. Implements risk management through position sizing and stop-loss orders

## License

[Specify your license here]

## Disclaimer

This trading bot is for educational and research purposes only. Use at your own risk. Past performance does not guarantee future results.
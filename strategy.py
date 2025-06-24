#!/usr/bin/env python3
"""
all equity - Time_series_momentum Trading Strategy

Strategy Type: time_series_momentum
Description: all equity
Created: 2025-06-24T23:34:17.564Z

WARNING: This is a template implementation. Thoroughly backtest before live trading.
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('strategy.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class allequityStrategy:
    """
    all equity Implementation
    
    Strategy Type: time_series_momentum
    Risk Level: Monitor drawdowns and position sizes carefully
    """
    
    def __init__(self, config=None):
        self.config = config or self.get_default_config()
        self.positions = {}
        self.performance_metrics = {}
        logger.info(f"Initialized all equity strategy")
        
    def get_default_config(self):
        """Default configuration parameters"""
        return {
            'max_position_size': 0.05,  # 5% max position size
            'stop_loss_pct': 0.05,      # 5% stop loss
            'lookback_period': 20,       # 20-day lookback
            'rebalance_freq': 'daily',   # Rebalancing frequency
            'transaction_costs': 0.001,  # 0.1% transaction costs
        }
    
    def load_data(self, symbols, start_date, end_date):
        """Load market data for analysis"""
        try:
            import yfinance as yf
            data = yf.download(symbols, start=start_date, end=end_date)
            logger.info(f"Loaded data for {len(symbols)} symbols")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None

# =============================================================================
# USER'S STRATEGY IMPLEMENTATION
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Sample data generation
def generate_sample_data(n_days=504, seed=42):
    # Generate synthetic equity price data using geometric Brownian motion
    np.random.seed(seed)
    dates = pd.date_range(start='2022-01-01', periods=n_days, freq='B')
    mu = 0.0005  # daily drift
    sigma = 0.01  # daily volatility
    prices = [100]
    for _ in range(1, n_days):
        ret = np.random.normal(mu, sigma)
        prices.append(prices[-1] * np.exp(ret))
    df = pd.DataFrame({'Close': prices}, index=dates)
    return df

class AllEquityMomentumStrategy:
    def __init__(self, data, lookback=20, risk_free_rate=0.01, position_size=1.0):
        # data: DataFrame with 'Close' prices
        self.data = data.copy()
        self.lookback = lookback
        self.risk_free_rate = risk_free_rate
        self.position_size = position_size
        self.signals = pd.Series(index=self.data.index, dtype=np.float64)
        self.returns = pd.Series(index=self.data.index, dtype=np.float64)
        self.strategy_returns = pd.Series(index=self.data.index, dtype=np.float64)
        self.positions = pd.Series(index=self.data.index, dtype=np.float64)
        self.equity_curve = pd.Series(index=self.data.index, dtype=np.float64)
        self._prepare_data()
    
    def _prepare_data(self):
        # Calculate daily returns
        self.data['Returns'] = self.data['Close'].pct_change()
    
    def generate_signals(self):
        # Momentum signal: if price > lookback-period moving average, go long; else, go to cash
        self.data['MA'] = self.data['Close'].rolling(window=self.lookback).mean()
        self.signals = np.where(self.data['Close'] > self.data['MA'], 1, 0)
        self.signals = pd.Series(self.signals, index=self.data.index)
        logging.info("Signals generated using momentum logic.")
    
    def position_sizing(self):
        # All equity: invest full capital when signal is 1, else 0
        self.positions = self.signals * self.position_size
        logging.info("Position sizing applied: all equity when signal is 1.")
    
    def apply_risk_management(self):
        # No additional risk management for all equity strategy
        pass
    
    def backtest(self):
        # Calculate strategy returns
        self.returns = self.data['Returns'].fillna(0)
        self.strategy_returns = self.positions.shift(1).fillna(0) * self.returns
        self.equity_curve = (1 + self.strategy_returns).cumprod()
        logging.info("Backtest completed.")
    
    def calculate_performance_metrics(self):
        # Sharpe Ratio
        excess_returns = self.strategy_returns - (self.risk_free_rate / 252)
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / (excess_returns.std() + 1e-8)
        # Max Drawdown
        rolling_max = self.equity_curve.cummax()
        drawdown = self.equity_curve / rolling_max - 1
        max_drawdown = drawdown.min()
        # CAGR
        n_years = (self.equity_curve.index[-1] - self.equity_curve.index[0]).days / 365.25
        cagr = self.equity_curve.iloc[-1] ** (1 / n_years) - 1
        # Total Return
        total_return = self.equity_curve.iloc[-1] - 1
        metrics = {
            'Sharpe Ratio': sharpe_ratio,
            'Max Drawdown': max_drawdown,
            'CAGR': cagr,
            'Total Return': total_return
        }
        logging.info("Performance metrics calculated.")
        return metrics
    
    def plot_results(self):
        plt.figure(figsize=(12,6))
        plt.plot(self.equity_curve, label='Strategy Equity Curve')
        plt.title('All Equity Momentum Strategy Equity Curve')
        plt.xlabel('Date')
        plt.ylabel('Equity')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def run(self):
        try:
            self.generate_signals()
            self.position_sizing()
            self.apply_risk_management()
            self.backtest()
            metrics = self.calculate_performance_metrics()
            self.plot_results()
            print("Performance Metrics:")
            for k, v in metrics.items():
                print("%s: %.4f" % (k, v))
        except Exception as e:
            logging.error("Error running strategy: %s" % str(e))

# Main execution block
if __name__ == "__main__":
    # Generate sample data
    data = generate_sample_data()
    # Initialize and run the strategy
    strategy = AllEquityMomentumStrategy(data, lookback=20, risk_free_rate=0.01, position_size=1.0)
    strategy.run()

# =============================================================================
# STRATEGY EXECUTION AND TESTING
# =============================================================================

if __name__ == "__main__":
    # Example usage and testing
    strategy = allequityStrategy()
    print(f"Strategy '{strategyName}' initialized successfully!")
    
    # Example data loading
    symbols = ['SPY', 'QQQ', 'IWM']
    start_date = '2020-01-01'
    end_date = '2023-12-31'
    
    print(f"Loading data for symbols: {symbols}")
    data = strategy.load_data(symbols, start_date, end_date)
    
    if data is not None:
        print(f"Data loaded successfully. Shape: {data.shape}")
        print("Strategy ready for backtesting!")
    else:
        print("Failed to load data. Check your internet connection.")

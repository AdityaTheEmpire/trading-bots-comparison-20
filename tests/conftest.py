"""
Test fixtures and utilities.
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


@pytest.fixture
def sample_ohlcv_data():
    """
    Generate sample OHLCV data for testing.
    
    Returns:
        DataFrame with sample market data
    """
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='1H')
    
    # Generate realistic price movement
    base_price = 30000
    prices = [base_price]
    
    np.random.seed(42)  # For reproducibility
    for _ in range(len(dates) - 1):
        change = np.random.randn() * base_price * 0.01
        prices.append(max(prices[-1] + change, base_price * 0.5))
    
    data = pd.DataFrame({
        'open': prices,
        'high': [p * (1 + abs(np.random.randn() * 0.005)) for p in prices],
        'low': [p * (1 - abs(np.random.randn() * 0.005)) for p in prices],
        'close': [p + np.random.randn() * base_price * 0.005 for p in prices],
        'volume': [np.random.randint(100, 10000) for _ in prices]
    }, index=dates)
    
    return data


@pytest.fixture
def bot_config():
    """
    Sample bot configuration.
    
    Returns:
        Configuration dictionary
    """
    return {
        'short_window': 20,
        'long_window': 50,
        'rsi_period': 14,
        'rsi_oversold': 30,
        'rsi_overbought': 70,
        'bb_period': 20,
        'bb_std': 2,
        'fast_period': 12,
        'slow_period': 26,
        'signal_period': 9,
        'momentum_period': 10,
        'lookback': 20,
        'std_dev': 2,
        'fast': 10,
        'slow': 30,
        'k_period': 14,
        'atr_period': 14,
        'atr_multiplier': 2,
        'volume_period': 20,
        'grid_size': 0.02,
        'spread': 0.01
    }

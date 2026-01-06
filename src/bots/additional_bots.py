"""
Additional trading bot implementations for the comparison framework.
This file contains 16 additional bots with various strategies.
"""
from typing import Dict, Optional
import pandas as pd
import numpy as np
from datetime import datetime
from src.core.base_bot import BaseTradingBot


class QuantConnectBot(BaseTradingBot):
    """Momentum-based strategy."""
    
    def __init__(self, config: Dict):
        super().__init__("QuantConnect", config)
        self.momentum_period = config.get('momentum_period', 10)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['momentum'] = data['close'].pct_change(periods=self.momentum_period)
        signals.loc[signals['momentum'] > 0.02, 'signal'] = 1
        signals.loc[signals['momentum'] < -0.02, 'signal'] = -1
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        if signal == 1:
            quantity = (capital * 0.9) / price
            if quantity > 0:
                return {'type': 'buy', 'timestamp': timestamp, 'price': price,
                       'quantity': quantity, 'cost': quantity * price}
        elif signal == -1 and hasattr(self, '_current_holdings'):
            if self._current_holdings > 0:
                return {'type': 'sell', 'timestamp': timestamp, 'price': price,
                       'quantity': self._current_holdings,
                       'proceeds': self._current_holdings * price}
        return None


class ZiplineBot(BaseTradingBot):
    """Mean reversion strategy."""
    
    def __init__(self, config: Dict):
        super().__init__("Zipline", config)
        self.lookback = config.get('lookback', 20)
        self.std_dev = config.get('std_dev', 2)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['mean'] = data['close'].rolling(window=self.lookback).mean()
        signals['std'] = data['close'].rolling(window=self.lookback).std()
        signals['z_score'] = (data['close'] - signals['mean']) / signals['std']
        signals.loc[signals['z_score'] < -self.std_dev, 'signal'] = 1
        signals.loc[signals['z_score'] > self.std_dev, 'signal'] = -1
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        if signal == 1:
            quantity = (capital * 0.9) / price
            if quantity > 0:
                return {'type': 'buy', 'timestamp': timestamp, 'price': price,
                       'quantity': quantity, 'cost': quantity * price}
        elif signal == -1 and hasattr(self, '_current_holdings'):
            if self._current_holdings > 0:
                return {'type': 'sell', 'timestamp': timestamp, 'price': price,
                       'quantity': self._current_holdings,
                       'proceeds': self._current_holdings * price}
        return None


class VectorBTBot(BaseTradingBot):
    """Dual moving average crossover."""
    
    def __init__(self, config: Dict):
        super().__init__("VectorBT", config)
        self.fast = config.get('fast', 10)
        self.slow = config.get('slow', 30)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['fast_ma'] = data['close'].rolling(window=self.fast).mean()
        signals['slow_ma'] = data['close'].rolling(window=self.slow).mean()
        signals.loc[signals['fast_ma'] > signals['slow_ma'], 'signal'] = 1
        signals.loc[signals['fast_ma'] < signals['slow_ma'], 'signal'] = -1
        signals['prev_signal'] = signals['signal'].shift(1)
        signals.loc[signals['signal'] == signals['prev_signal'], 'signal'] = 0
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        if signal == 1:
            quantity = (capital * 0.95) / price
            if quantity > 0:
                return {'type': 'buy', 'timestamp': timestamp, 'price': price,
                       'quantity': quantity, 'cost': quantity * price}
        elif signal == -1 and hasattr(self, '_current_holdings'):
            if self._current_holdings > 0:
                return {'type': 'sell', 'timestamp': timestamp, 'price': price,
                       'quantity': self._current_holdings,
                       'proceeds': self._current_holdings * price}
        return None


class TALibBot(BaseTradingBot):
    """Stochastic oscillator strategy."""
    
    def __init__(self, config: Dict):
        super().__init__("TALib", config)
        self.k_period = config.get('k_period', 14)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def calculate_stochastic(self, data: pd.DataFrame) -> pd.DataFrame:
        low_min = data['low'].rolling(window=self.k_period).min()
        high_max = data['high'].rolling(window=self.k_period).max()
        k = 100 * (data['close'] - low_min) / (high_max - low_min)
        d = k.rolling(window=3).mean()
        return pd.DataFrame({'k': k, 'd': d})
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        stoch = self.calculate_stochastic(data)
        signals['k'] = stoch['k']
        signals['d'] = stoch['d']
        signals.loc[signals['k'] < 20, 'signal'] = 1
        signals.loc[signals['k'] > 80, 'signal'] = -1
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        if signal == 1:
            quantity = (capital * 0.9) / price
            if quantity > 0:
                return {'type': 'buy', 'timestamp': timestamp, 'price': price,
                       'quantity': quantity, 'cost': quantity * price}
        elif signal == -1 and hasattr(self, '_current_holdings'):
            if self._current_holdings > 0:
                return {'type': 'sell', 'timestamp': timestamp, 'price': price,
                       'quantity': self._current_holdings,
                       'proceeds': self._current_holdings * price}
        return None


class PyAlgoTradeBot(BaseTradingBot):
    """ATR-based breakout strategy."""
    
    def __init__(self, config: Dict):
        super().__init__("PyAlgoTrade", config)
        self.atr_period = config.get('atr_period', 14)
        self.atr_multiplier = config.get('atr_multiplier', 2)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def calculate_atr(self, data: pd.DataFrame) -> pd.Series:
        high_low = data['high'] - data['low']
        high_close = np.abs(data['high'] - data['close'].shift())
        low_close = np.abs(data['low'] - data['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(self.atr_period).mean()
        return atr
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['atr'] = self.calculate_atr(data)
        signals['upper'] = data['close'] + signals['atr'] * self.atr_multiplier
        signals['lower'] = data['close'] - signals['atr'] * self.atr_multiplier
        signals.loc[data['close'] > signals['upper'].shift(1), 'signal'] = 1
        signals.loc[data['close'] < signals['lower'].shift(1), 'signal'] = -1
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        if signal == 1:
            quantity = (capital * 0.9) / price
            if quantity > 0:
                return {'type': 'buy', 'timestamp': timestamp, 'price': price,
                       'quantity': quantity, 'cost': quantity * price}
        elif signal == -1 and hasattr(self, '_current_holdings'):
            if self._current_holdings > 0:
                return {'type': 'sell', 'timestamp': timestamp, 'price': price,
                       'quantity': self._current_holdings,
                       'proceeds': self._current_holdings * price}
        return None


class CatalystBot(BaseTradingBot):
    """Volume-weighted strategy."""
    
    def __init__(self, config: Dict):
        super().__init__("Catalyst", config)
        self.volume_period = config.get('volume_period', 20)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['avg_volume'] = data['volume'].rolling(window=self.volume_period).mean()
        signals['price_change'] = data['close'].pct_change()
        signals.loc[(data['volume'] > signals['avg_volume'] * 1.5) & 
                   (signals['price_change'] > 0), 'signal'] = 1
        signals.loc[(data['volume'] > signals['avg_volume'] * 1.5) & 
                   (signals['price_change'] < 0), 'signal'] = -1
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        if signal == 1:
            quantity = (capital * 0.9) / price
            if quantity > 0:
                return {'type': 'buy', 'timestamp': timestamp, 'price': price,
                       'quantity': quantity, 'cost': quantity * price}
        elif signal == -1 and hasattr(self, '_current_holdings'):
            if self._current_holdings > 0:
                return {'type': 'sell', 'timestamp': timestamp, 'price': price,
                       'quantity': self._current_holdings,
                       'proceeds': self._current_holdings * price}
        return None

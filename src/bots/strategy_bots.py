"""
Strategy-specific trading bots (RSI, MACD, Bollinger, MA Crossover, etc.).
"""
from typing import Dict, Optional
import pandas as pd
import numpy as np
from datetime import datetime
from src.core.base_bot import BaseTradingBot


class RSIBot(BaseTradingBot):
    """Pure RSI strategy bot."""
    
    def __init__(self, config: Dict):
        super().__init__("RSI_Strategy", config)
        self.rsi_period = config.get('rsi_period', 14)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def calculate_rsi(self, data: pd.Series, period: int = 14) -> pd.Series:
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['rsi'] = self.calculate_rsi(data['close'], self.rsi_period)
        signals.loc[signals['rsi'] < 25, 'signal'] = 1
        signals.loc[signals['rsi'] > 75, 'signal'] = -1
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


class MACDBot(BaseTradingBot):
    """Pure MACD strategy bot."""
    
    def __init__(self, config: Dict):
        super().__init__("MACD_Strategy", config)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        exp1 = data['close'].ewm(span=12, adjust=False).mean()
        exp2 = data['close'].ewm(span=26, adjust=False).mean()
        signals['macd'] = exp1 - exp2
        signals['signal_line'] = signals['macd'].ewm(span=9, adjust=False).mean()
        signals.loc[signals['macd'] > signals['signal_line'], 'signal'] = 1
        signals.loc[signals['macd'] < signals['signal_line'], 'signal'] = -1
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


class BollingerBot(BaseTradingBot):
    """Bollinger Bands strategy bot."""
    
    def __init__(self, config: Dict):
        super().__init__("Bollinger_Strategy", config)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['middle'] = data['close'].rolling(window=20).mean()
        signals['std'] = data['close'].rolling(window=20).std()
        signals['upper'] = signals['middle'] + 2 * signals['std']
        signals['lower'] = signals['middle'] - 2 * signals['std']
        signals.loc[data['close'] <= signals['lower'], 'signal'] = 1
        signals.loc[data['close'] >= signals['upper'], 'signal'] = -1
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


class MACrossoverBot(BaseTradingBot):
    """Moving Average Crossover strategy bot."""
    
    def __init__(self, config: Dict):
        super().__init__("MA_Crossover_Strategy", config)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['ma_fast'] = data['close'].rolling(window=10).mean()
        signals['ma_slow'] = data['close'].rolling(window=50).mean()
        signals.loc[signals['ma_fast'] > signals['ma_slow'], 'signal'] = 1
        signals.loc[signals['ma_fast'] < signals['ma_slow'], 'signal'] = -1
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


class MeanReversionBot(BaseTradingBot):
    """Mean Reversion strategy bot."""
    
    def __init__(self, config: Dict):
        super().__init__("Mean_Reversion_Strategy", config)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['mean'] = data['close'].rolling(window=30).mean()
        signals['std'] = data['close'].rolling(window=30).std()
        signals['z_score'] = (data['close'] - signals['mean']) / signals['std']
        signals.loc[signals['z_score'] < -1.5, 'signal'] = 1
        signals.loc[signals['z_score'] > 1.5, 'signal'] = -1
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


class MomentumBot(BaseTradingBot):
    """Momentum strategy bot."""
    
    def __init__(self, config: Dict):
        super().__init__("Momentum_Strategy", config)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['momentum'] = data['close'].pct_change(periods=12)
        signals.loc[signals['momentum'] > 0.05, 'signal'] = 1
        signals.loc[signals['momentum'] < -0.05, 'signal'] = -1
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


class BreakoutBot(BaseTradingBot):
    """Breakout strategy bot."""
    
    def __init__(self, config: Dict):
        super().__init__("Breakout_Strategy", config)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['high_20'] = data['high'].rolling(window=20).max()
        signals['low_20'] = data['low'].rolling(window=20).min()
        signals.loc[data['close'] > signals['high_20'].shift(1), 'signal'] = 1
        signals.loc[data['close'] < signals['low_20'].shift(1), 'signal'] = -1
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


class GridTradingBot(BaseTradingBot):
    """Grid Trading strategy bot."""
    
    def __init__(self, config: Dict):
        super().__init__("Grid_Trading_Strategy", config)
        self.grid_size = config.get('grid_size', 0.02)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['price_change'] = data['close'].pct_change()
        signals.loc[signals['price_change'] < -self.grid_size, 'signal'] = 1
        signals.loc[signals['price_change'] > self.grid_size, 'signal'] = -1
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        if signal == 1:
            quantity = (capital * 0.2) / price  # Smaller position for grid
            if quantity > 0:
                return {'type': 'buy', 'timestamp': timestamp, 'price': price,
                       'quantity': quantity, 'cost': quantity * price}
        elif signal == -1 and hasattr(self, '_current_holdings'):
            if self._current_holdings > 0:
                quantity = min(self._current_holdings, (capital * 0.2) / price)
                return {'type': 'sell', 'timestamp': timestamp, 'price': price,
                       'quantity': quantity, 'proceeds': quantity * price}
        return None


class ArbitrageBot(BaseTradingBot):
    """Arbitrage strategy bot (simplified)."""
    
    def __init__(self, config: Dict):
        super().__init__("Arbitrage_Strategy", config)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['volatility'] = data['close'].rolling(window=10).std()
        signals['avg_volatility'] = signals['volatility'].rolling(window=20).mean()
        signals.loc[signals['volatility'] > signals['avg_volatility'] * 1.5, 'signal'] = 1
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        if signal == 1:
            quantity = (capital * 0.5) / price
            if quantity > 0:
                return {'type': 'buy', 'timestamp': timestamp, 'price': price,
                       'quantity': quantity, 'cost': quantity * price}
        return None


class MarketMakingBot(BaseTradingBot):
    """Market Making strategy bot (simplified)."""
    
    def __init__(self, config: Dict):
        super().__init__("Market_Making_Strategy", config)
        self.spread = config.get('spread', 0.01)
        
    def initialize(self, data: pd.DataFrame) -> None:
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['mid_price'] = (data['high'] + data['low']) / 2
        signals['spread'] = (data['high'] - data['low']) / signals['mid_price']
        signals.loc[signals['spread'] > self.spread * 2, 'signal'] = 1
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        if signal == 1:
            quantity = (capital * 0.3) / price
            if quantity > 0:
                return {'type': 'buy', 'timestamp': timestamp, 'price': price,
                       'quantity': quantity, 'cost': quantity * price}
        return None

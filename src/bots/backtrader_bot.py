"""
Backtrader-style trading bot implementation.
Uses MACD strategy.
"""
from typing import Dict, Optional
import pandas as pd
from datetime import datetime
from src.core.base_bot import BaseTradingBot


class BacktraderBot(BaseTradingBot):
    """
    Backtrader-inspired bot using MACD strategy.
    """
    
    def __init__(self, config: Dict):
        super().__init__("Backtrader", config)
        self.fast_period = config.get('fast_period', 12)
        self.slow_period = config.get('slow_period', 26)
        self.signal_period = config.get('signal_period', 9)
        
    def initialize(self, data: pd.DataFrame) -> None:
        """Initialize indicators."""
        pass
    
    def calculate_macd(self, data: pd.Series) -> pd.DataFrame:
        """Calculate MACD indicator."""
        exp1 = data.ewm(span=self.fast_period, adjust=False).mean()
        exp2 = data.ewm(span=self.slow_period, adjust=False).mean()
        
        macd = exp1 - exp2
        signal = macd.ewm(span=self.signal_period, adjust=False).mean()
        histogram = macd - signal
        
        return pd.DataFrame({'macd': macd, 'signal': signal, 'histogram': histogram})
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate signals based on MACD."""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # Calculate MACD
        macd_data = self.calculate_macd(data['close'])
        signals['macd'] = macd_data['macd']
        signals['macd_signal'] = macd_data['signal']
        signals['histogram'] = macd_data['histogram']
        
        # Generate signals on crossovers
        signals.loc[signals['histogram'] > 0, 'signal'] = 1  # Buy
        signals.loc[signals['histogram'] < 0, 'signal'] = -1  # Sell
        
        # Only trigger on crossover
        signals['prev_signal'] = signals['signal'].shift(1)
        signals.loc[signals['signal'] == signals['prev_signal'], 'signal'] = 0
        
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        """Execute trades based on signals."""
        if signal == 0:
            return None
        
        if signal == 1:  # Buy signal
            quantity = (capital * 0.95) / price
            if quantity > 0:
                return {
                    'type': 'buy',
                    'timestamp': timestamp,
                    'price': price,
                    'quantity': quantity,
                    'cost': quantity * price
                }
        
        elif signal == -1:  # Sell signal
            if hasattr(self, '_current_holdings') and self._current_holdings > 0:
                quantity = self._current_holdings
                return {
                    'type': 'sell',
                    'timestamp': timestamp,
                    'price': price,
                    'quantity': quantity,
                    'proceeds': quantity * price
                }
        
        return None

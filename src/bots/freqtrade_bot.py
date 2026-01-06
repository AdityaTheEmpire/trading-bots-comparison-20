"""
Freqtrade-style trading bot implementation.
Uses a simple moving average crossover strategy.
"""
from typing import Dict, Optional
import pandas as pd
from datetime import datetime
from src.core.base_bot import BaseTradingBot


class FreqtradeBot(BaseTradingBot):
    """
    Freqtrade-inspired bot using moving average crossover strategy.
    """
    
    def __init__(self, config: Dict):
        super().__init__("Freqtrade", config)
        self.short_window = config.get('short_window', 20)
        self.long_window = config.get('long_window', 50)
        
    def initialize(self, data: pd.DataFrame) -> None:
        """Initialize indicators."""
        pass
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate signals based on moving average crossover.
        """
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # Calculate moving averages
        signals['short_ma'] = data['close'].rolling(window=self.short_window, min_periods=1).mean()
        signals['long_ma'] = data['close'].rolling(window=self.long_window, min_periods=1).mean()
        
        # Generate signals
        signals.loc[signals['short_ma'] > signals['long_ma'], 'signal'] = 1
        signals.loc[signals['short_ma'] < signals['long_ma'], 'signal'] = -1
        
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
            quantity = (capital * 0.95) / price  # Use 95% of available capital
            if quantity > 0:
                return {
                    'type': 'buy',
                    'timestamp': timestamp,
                    'price': price,
                    'quantity': quantity,
                    'cost': quantity * price
                }
        
        elif signal == -1:  # Sell signal
            # Sell all holdings
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

"""
Jesse-style trading bot implementation.
Uses RSI-based mean reversion strategy.
"""
from typing import Dict, Optional
import pandas as pd
from datetime import datetime
from src.core.base_bot import BaseTradingBot


class JesseBot(BaseTradingBot):
    """
    Jesse-inspired bot using RSI mean reversion strategy.
    """
    
    def __init__(self, config: Dict):
        super().__init__("Jesse", config)
        self.rsi_period = config.get('rsi_period', 14)
        self.rsi_oversold = config.get('rsi_oversold', 30)
        self.rsi_overbought = config.get('rsi_overbought', 70)
        
    def initialize(self, data: pd.DataFrame) -> None:
        """Initialize indicators."""
        pass
    
    def calculate_rsi(self, data: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator."""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate signals based on RSI."""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # Calculate RSI
        signals['rsi'] = self.calculate_rsi(data['close'], self.rsi_period)
        
        # Generate signals
        signals.loc[signals['rsi'] < self.rsi_oversold, 'signal'] = 1  # Buy
        signals.loc[signals['rsi'] > self.rsi_overbought, 'signal'] = -1  # Sell
        
        return signals
    
    def execute_trade(self, signal: int, timestamp: datetime, price: float,
                      capital: float) -> Optional[Dict]:
        """Execute trades based on signals."""
        if signal == 0:
            return None
        
        if signal == 1:  # Buy signal
            quantity = (capital * 0.9) / price
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

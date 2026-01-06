"""
Base class for all trading bots in the comparison framework.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import pandas as pd
from datetime import datetime


class BaseTradingBot(ABC):
    """
    Abstract base class that all trading bots must implement.
    """
    
    def __init__(self, name: str, config: Dict):
        """
        Initialize the trading bot.
        
        Args:
            name: Unique name for this bot
            config: Configuration dictionary
        """
        self.name = name
        self.config = config
        self.trades: List[Dict] = []
        self.portfolio_value: List[float] = []
        self.positions: Dict = {}
        
    @abstractmethod
    def initialize(self, data: pd.DataFrame) -> None:
        """
        Initialize the bot with historical data.
        
        Args:
            data: DataFrame with OHLCV data
        """
        pass
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the strategy.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame with signals (1 for buy, -1 for sell, 0 for hold)
        """
        pass
    
    @abstractmethod
    def execute_trade(self, signal: int, timestamp: datetime, price: float, 
                      capital: float) -> Optional[Dict]:
        """
        Execute a trade based on the signal.
        
        Args:
            signal: Trading signal (1=buy, -1=sell, 0=hold)
            timestamp: Time of the trade
            price: Current price
            capital: Available capital
            
        Returns:
            Trade details dictionary or None
        """
        pass
    
    def backtest(self, data: pd.DataFrame, initial_capital: float) -> Dict:
        """
        Run backtest on historical data.
        
        Args:
            data: DataFrame with OHLCV data
            initial_capital: Starting capital
            
        Returns:
            Dictionary with backtest results
        """
        self.initialize(data)
        signals = self.generate_signals(data)
        
        capital = initial_capital
        holdings = 0
        portfolio_values = []
        
        for i, row in data.iterrows():
            signal = signals.loc[i, 'signal'] if 'signal' in signals.columns else 0
            
            trade = self.execute_trade(
                signal=signal,
                timestamp=row.name if isinstance(row.name, datetime) else i,
                price=row['close'],
                capital=capital
            )
            
            if trade:
                self.trades.append(trade)
                if trade['type'] == 'buy':
                    holdings += trade['quantity']
                    capital -= trade['cost']
                elif trade['type'] == 'sell':
                    holdings -= trade['quantity']
                    capital += trade['proceeds']
            
            # Calculate portfolio value
            portfolio_value = capital + (holdings * row['close'])
            portfolio_values.append(portfolio_value)
        
        self.portfolio_value = portfolio_values
        
        return {
            'bot_name': self.name,
            'initial_capital': initial_capital,
            'final_capital': portfolio_values[-1] if portfolio_values else initial_capital,
            'total_trades': len(self.trades),
            'trades': self.trades,
            'portfolio_values': portfolio_values
        }
    
    def get_performance_summary(self) -> Dict:
        """
        Get a summary of bot performance.
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.portfolio_value:
            return {}
        
        return {
            'bot_name': self.name,
            'final_portfolio_value': self.portfolio_value[-1],
            'total_trades': len(self.trades),
            'portfolio_history': self.portfolio_value
        }

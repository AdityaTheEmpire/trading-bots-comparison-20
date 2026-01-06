"""
Performance metrics calculator for trading bots.
Calculates Sharpe ratio, max drawdown, win rate, profit factor, and other metrics.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional


class PerformanceMetrics:
    """
    Calculate comprehensive performance metrics for trading strategies.
    """
    
    @staticmethod
    def calculate_returns(portfolio_values: List[float]) -> np.ndarray:
        """
        Calculate returns from portfolio values.
        
        Args:
            portfolio_values: List of portfolio values over time
            
        Returns:
            Array of returns
        """
        values = np.array(portfolio_values)
        returns = np.diff(values) / values[:-1]
        return returns
    
    @staticmethod
    def sharpe_ratio(portfolio_values: List[float], risk_free_rate: float = 0.02,
                     periods_per_year: int = 252) -> float:
        """
        Calculate Sharpe ratio.
        
        Args:
            portfolio_values: List of portfolio values
            risk_free_rate: Annual risk-free rate
            periods_per_year: Number of periods in a year (252 for daily, 52 for weekly)
            
        Returns:
            Sharpe ratio
        """
        if len(portfolio_values) < 2:
            return 0.0
        
        returns = PerformanceMetrics.calculate_returns(portfolio_values)
        
        if len(returns) == 0 or np.std(returns) == 0:
            return 0.0
        
        excess_returns = returns - (risk_free_rate / periods_per_year)
        sharpe = np.mean(excess_returns) / np.std(returns) * np.sqrt(periods_per_year)
        
        return float(sharpe)
    
    @staticmethod
    def max_drawdown(portfolio_values: List[float]) -> Dict[str, float]:
        """
        Calculate maximum drawdown.
        
        Args:
            portfolio_values: List of portfolio values
            
        Returns:
            Dictionary with max_drawdown, max_drawdown_pct, and duration
        """
        if len(portfolio_values) < 2:
            return {'max_drawdown': 0.0, 'max_drawdown_pct': 0.0, 'duration': 0}
        
        values = np.array(portfolio_values)
        cummax = np.maximum.accumulate(values)
        drawdown = (cummax - values) / cummax
        
        max_dd = float(np.max(drawdown))
        max_dd_value = float(np.max(cummax - values))
        
        # Find duration
        dd_duration = 0
        current_duration = 0
        for dd in drawdown:
            if dd > 0:
                current_duration += 1
                dd_duration = max(dd_duration, current_duration)
            else:
                current_duration = 0
        
        return {
            'max_drawdown': max_dd_value,
            'max_drawdown_pct': max_dd * 100,
            'duration': dd_duration
        }
    
    @staticmethod
    def win_rate(trades: List[Dict]) -> float:
        """
        Calculate win rate from trades.
        
        Args:
            trades: List of trade dictionaries
            
        Returns:
            Win rate as percentage
        """
        if not trades:
            return 0.0
        
        # Group trades into pairs (buy/sell)
        buy_trades = [t for t in trades if t.get('type') == 'buy']
        sell_trades = [t for t in trades if t.get('type') == 'sell']
        
        completed_trades = min(len(buy_trades), len(sell_trades))
        
        if completed_trades == 0:
            return 0.0
        
        winning_trades = 0
        for i in range(completed_trades):
            buy_price = buy_trades[i].get('price', 0)
            sell_price = sell_trades[i].get('price', 0)
            if sell_price > buy_price:
                winning_trades += 1
        
        return (winning_trades / completed_trades) * 100
    
    @staticmethod
    def profit_factor(trades: List[Dict]) -> float:
        """
        Calculate profit factor (gross profit / gross loss).
        
        Args:
            trades: List of trade dictionaries
            
        Returns:
            Profit factor
        """
        if not trades:
            return 0.0
        
        gross_profit = 0.0
        gross_loss = 0.0
        
        # Group trades into pairs
        buy_trades = [t for t in trades if t.get('type') == 'buy']
        sell_trades = [t for t in trades if t.get('type') == 'sell']
        
        completed_trades = min(len(buy_trades), len(sell_trades))
        
        for i in range(completed_trades):
            buy_cost = buy_trades[i].get('cost', 0)
            sell_proceeds = sell_trades[i].get('proceeds', 0)
            pnl = sell_proceeds - buy_cost
            
            if pnl > 0:
                gross_profit += pnl
            else:
                gross_loss += abs(pnl)
        
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0.0
        
        return gross_profit / gross_loss
    
    @staticmethod
    def calculate_all_metrics(portfolio_values: List[float], trades: List[Dict],
                             initial_capital: float, risk_free_rate: float = 0.02) -> Dict:
        """
        Calculate all performance metrics.
        
        Args:
            portfolio_values: List of portfolio values
            trades: List of trade dictionaries
            initial_capital: Starting capital
            risk_free_rate: Annual risk-free rate
            
        Returns:
            Dictionary with all metrics
        """
        final_value = portfolio_values[-1] if portfolio_values else initial_capital
        total_return = ((final_value - initial_capital) / initial_capital) * 100
        
        metrics = {
            'initial_capital': initial_capital,
            'final_value': final_value,
            'total_return_pct': total_return,
            'total_trades': len(trades),
            'sharpe_ratio': PerformanceMetrics.sharpe_ratio(portfolio_values, risk_free_rate),
            'win_rate_pct': PerformanceMetrics.win_rate(trades),
            'profit_factor': PerformanceMetrics.profit_factor(trades),
        }
        
        # Add max drawdown metrics
        dd_metrics = PerformanceMetrics.max_drawdown(portfolio_values)
        metrics.update(dd_metrics)
        
        return metrics

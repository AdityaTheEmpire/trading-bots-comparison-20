"""
Backtesting engine for running bot comparisons.
"""
from typing import Dict, List
import pandas as pd
from src.core.base_bot import BaseTradingBot
from src.core.metrics import PerformanceMetrics
from src.core.delta_api import DeltaExchangeAPI


class BacktestEngine:
    """
    Engine for running backtests across multiple bots.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize the backtest engine.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.api = DeltaExchangeAPI(
            api_key=config.get('delta_exchange', {}).get('api_key'),
            api_secret=config.get('delta_exchange', {}).get('api_secret'),
            testnet=config.get('delta_exchange', {}).get('testnet', True)
        )
        self.results = []
        
    def run_backtest(self, bot: BaseTradingBot, symbol: str) -> Dict:
        """
        Run backtest for a single bot on a symbol.
        
        Args:
            bot: Trading bot instance
            symbol: Trading symbol
            
        Returns:
            Dictionary with backtest results
        """
        # Get historical data
        backtest_settings = self.config.get('backtest_settings', {})
        start_date = pd.to_datetime(backtest_settings.get('start_date', '2023-01-01'))
        end_date = pd.to_datetime(backtest_settings.get('end_date', '2023-12-31'))
        initial_capital = backtest_settings.get('initial_capital', 10000)
        
        data = self.api.get_ohlc_data(
            symbol=symbol,
            resolution=backtest_settings.get('timeframe', '1h'),
            start_time=start_date,
            end_time=end_date
        )
        
        # Run backtest
        backtest_result = bot.backtest(data, initial_capital)
        
        # Calculate performance metrics
        metrics = PerformanceMetrics.calculate_all_metrics(
            portfolio_values=backtest_result['portfolio_values'],
            trades=backtest_result['trades'],
            initial_capital=initial_capital,
            risk_free_rate=self.config.get('performance_metrics', {}).get('risk_free_rate', 0.02)
        )
        
        # Combine results
        result = {
            'bot_name': bot.name,
            'symbol': symbol,
            'backtest_period': f"{start_date.date()} to {end_date.date()}",
            **metrics,
            'trades_detail': backtest_result['trades']
        }
        
        return result
    
    def run_all_backtests(self, bots: List[BaseTradingBot]) -> List[Dict]:
        """
        Run backtests for all bots across all symbols.
        
        Args:
            bots: List of bot instances
            
        Returns:
            List of result dictionaries
        """
        symbols = self.config.get('backtest_settings', {}).get('symbols', ['BTCUSDT'])
        results = []
        
        for symbol in symbols:
            for bot in bots:
                print(f"Running backtest: {bot.name} on {symbol}...")
                result = self.run_backtest(bot, symbol)
                results.append(result)
        
        self.results = results
        return results
    
    def get_aggregated_results(self) -> pd.DataFrame:
        """
        Get aggregated results as a DataFrame.
        
        Returns:
            DataFrame with all results
        """
        if not self.results:
            return pd.DataFrame()
        
        # Create DataFrame excluding trades_detail
        results_for_df = []
        for result in self.results:
            result_copy = result.copy()
            result_copy.pop('trades_detail', None)
            results_for_df.append(result_copy)
        
        df = pd.DataFrame(results_for_df)
        
        # Aggregate by bot (average across symbols)
        if 'symbol' in df.columns:
            agg_df = df.groupby('bot_name').agg({
                'initial_capital': 'first',
                'final_value': 'mean',
                'total_return_pct': 'mean',
                'total_trades': 'sum',
                'sharpe_ratio': 'mean',
                'win_rate_pct': 'mean',
                'profit_factor': 'mean',
                'max_drawdown': 'mean',
                'max_drawdown_pct': 'mean',
                'duration': 'mean'
            }).reset_index()
            
            return agg_df
        
        return df

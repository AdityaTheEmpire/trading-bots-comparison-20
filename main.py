"""
Main execution script for the trading bots comparison framework.
Runs all 20 bots, compares performance, and generates reports.
"""
import json
import sys
from typing import Dict, List

from src.core.backtest_engine import BacktestEngine
from src.analysis.visualizer import PerformanceVisualizer
from src.analysis.report_generator import ReportGenerator
from src.utils.exporters import ResultExporter

# Import all bot implementations
from src.bots.freqtrade_bot import FreqtradeBot
from src.bots.jesse_bot import JesseBot
from src.bots.ccxt_bot import CCXTBot
from src.bots.backtrader_bot import BacktraderBot
from src.bots.additional_bots import (
    QuantConnectBot, ZiplineBot, VectorBTBot, TALibBot,
    PyAlgoTradeBot, CatalystBot
)
from src.bots.strategy_bots import (
    RSIBot, MACDBot, BollingerBot, MACrossoverBot,
    MeanReversionBot, MomentumBot, BreakoutBot,
    GridTradingBot, ArbitrageBot, MarketMakingBot
)


def load_config(config_path: str = "config.json") -> Dict:
    """
    Load configuration from file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_path}")
        print("Using example config...")
        with open("config.json.example", 'r') as f:
            return json.load(f)


def initialize_all_bots(config: Dict) -> List:
    """
    Initialize all 20 trading bots.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of bot instances
    """
    bots = [
        # Framework-based bots
        FreqtradeBot(config),
        JesseBot(config),
        CCXTBot(config),
        BacktraderBot(config),
        QuantConnectBot(config),
        ZiplineBot(config),
        VectorBTBot(config),
        TALibBot(config),
        PyAlgoTradeBot(config),
        CatalystBot(config),
        
        # Strategy-based bots
        RSIBot(config),
        MACDBot(config),
        BollingerBot(config),
        MACrossoverBot(config),
        MeanReversionBot(config),
        MomentumBot(config),
        BreakoutBot(config),
        GridTradingBot(config),
        ArbitrageBot(config),
        MarketMakingBot(config),
    ]
    
    return bots


def main():
    """
    Main execution function.
    """
    print("=" * 80)
    print("TRADING BOTS COMPARISON FRAMEWORK")
    print("=" * 80)
    print()
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    print(f"Configuration loaded successfully")
    print()
    
    # Initialize bots
    print("Initializing 20 trading bots...")
    bots = initialize_all_bots(config)
    print(f"Initialized {len(bots)} bots:")
    for i, bot in enumerate(bots, 1):
        print(f"  {i}. {bot.name}")
    print()
    
    # Initialize components
    print("Initializing backtest engine...")
    engine = BacktestEngine(config)
    print()
    
    # Run backtests
    print("=" * 80)
    print("RUNNING BACKTESTS")
    print("=" * 80)
    print()
    
    results = engine.run_all_backtests(bots)
    print()
    print(f"Completed {len(results)} backtests")
    print()
    
    # Aggregate results
    print("Aggregating results...")
    aggregated_df = engine.get_aggregated_results()
    print(f"Aggregated results for {len(aggregated_df)} bots")
    print()
    
    # Export results
    print("=" * 80)
    print("EXPORTING RESULTS")
    print("=" * 80)
    print()
    
    exporter = ResultExporter(output_dir="results")
    exporter.export_aggregated_results(aggregated_df)
    exporter.export_detailed_trades(results)
    print()
    
    # Generate visualizations
    print("=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    print()
    
    visualizer = PerformanceVisualizer(output_dir="reports")
    visualizer.create_all_charts(aggregated_df)
    print()
    
    # Generate report
    print("=" * 80)
    print("GENERATING REPORT")
    print("=" * 80)
    print()
    
    report_gen = ReportGenerator(output_dir="reports")
    report_path = report_gen.generate_markdown_report(aggregated_df)
    print()
    
    # Summary
    print("=" * 80)
    print("EXECUTION SUMMARY")
    print("=" * 80)
    print()
    print(f"✓ Ran backtests for {len(bots)} trading bots")
    print(f"✓ Generated performance visualizations")
    print(f"✓ Exported results to JSON and CSV")
    print(f"✓ Created comprehensive markdown report")
    print()
    print("Output directories:")
    print("  - results/    : JSON and CSV result files")
    print("  - reports/    : Charts and markdown report")
    print()
    
    # Display top 5 performers
    print("=" * 80)
    print("TOP 5 PERFORMERS (by Total Return)")
    print("=" * 80)
    print()
    
    top_5 = aggregated_df.nlargest(5, 'total_return_pct')
    for i, (idx, row) in enumerate(top_5.iterrows(), 1):
        print(f"{i}. {row['bot_name']}")
        print(f"   Return: {row['total_return_pct']:.2f}%")
        print(f"   Sharpe: {row['sharpe_ratio']:.2f}")
        print(f"   Max DD: {row['max_drawdown_pct']:.2f}%")
        print()
    
    print("=" * 80)
    print("COMPARISON COMPLETE!")
    print("=" * 80)
    print()
    print(f"View full report: {report_path}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

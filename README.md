# Trading Bots Comparison Framework

A comprehensive Python framework for comparing 20 different trading bots with automated backtesting, performance analytics, and detailed reporting.

## 🎯 Features

- **20 Trading Bots**: Compares Freqtrade, Jesse, CCXT, Backtrader, QuantConnect, Zipline, VectorBT, TA-Lib, PyAlgoTrade, Catalyst, and 10 custom strategy bots
- **Automated Backtesting**: Run historical backtests across multiple symbols and timeframes
- **Performance Metrics**: 
  - Sharpe Ratio calculation
  - Maximum Drawdown analysis
  - Win Rate tracking
  - Profit Factor comparisons
  - Total return metrics
- **Delta Exchange API Integration**: Fetch real market data for backtesting
- **Result Aggregation**: Automated export to JSON and CSV formats
- **Visualization**: Beautiful performance comparison charts
- **Detailed Reports**: Comprehensive markdown reports ranking all bots by profitability

## 📋 Trading Bots Included

### Framework-Based Bots
1. **Freqtrade** - Moving Average Crossover strategy
2. **Jesse** - RSI-based mean reversion
3. **CCXT** - Bollinger Bands strategy
4. **Backtrader** - MACD strategy
5. **QuantConnect** - Momentum-based strategy
6. **Zipline** - Mean reversion strategy
7. **VectorBT** - Dual moving average crossover
8. **TALib** - Stochastic oscillator strategy
9. **PyAlgoTrade** - ATR-based breakout
10. **Catalyst** - Volume-weighted strategy

### Strategy-Based Bots
11. **RSI Strategy** - Pure RSI indicator
12. **MACD Strategy** - Pure MACD signals
13. **Bollinger Strategy** - Bollinger Bands
14. **MA Crossover** - Moving average crossover
15. **Mean Reversion** - Statistical mean reversion
16. **Momentum** - Price momentum
17. **Breakout** - Price breakout detection
18. **Grid Trading** - Grid-based trading
19. **Arbitrage** - Volatility-based arbitrage (simplified)
20. **Market Making** - Spread-based market making (simplified)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/AdityaTheEmpire/trading-bots-comparison-20.git
cd trading-bots-comparison-20

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy the example config:
```bash
cp config.json.example config.json
```

2. Edit `config.json` with your settings:
```json
{
  "delta_exchange": {
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_API_SECRET",
    "testnet": true
  },
  "backtest_settings": {
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "initial_capital": 10000,
    "symbols": ["BTCUSDT", "ETHUSDT"],
    "timeframe": "1h"
  }
}
```

### Run the Comparison

```bash
python main.py
```

This will:
1. Initialize all 20 trading bots
2. Run backtests on historical data
3. Calculate performance metrics
4. Generate visualizations
5. Create a detailed markdown report

## 📊 Output

The framework generates several output files:

### Results Directory (`results/`)
- `aggregated_results.json` - Complete results in JSON format
- `aggregated_results.csv` - Results in CSV format
- `detailed_trades.json` - Detailed trade-by-trade information

### Reports Directory (`reports/`)
- `comparison_report.md` - Comprehensive markdown report
- `returns_comparison.png` - Total returns bar chart
- `sharpe_ratio_comparison.png` - Sharpe ratio comparison
- `max_drawdown_comparison.png` - Maximum drawdown chart
- `win_rate_comparison.png` - Win rate comparison
- `profit_factor_comparison.png` - Profit factor chart
- `performance_heatmap.png` - Normalized metrics heatmap

## 📈 Performance Metrics Explained

- **Sharpe Ratio**: Risk-adjusted return metric. Higher is better. > 1 is good, > 2 is very good.
- **Maximum Drawdown**: Largest peak-to-trough decline. Lower is better (less risk).
- **Win Rate**: Percentage of profitable trades. Higher indicates consistency.
- **Profit Factor**: Gross profit / Gross loss. > 1 means profitable, > 2 is excellent.
- **Total Return**: Overall percentage return on investment.

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/bots/test_all_bots.py
```

## 📁 Project Structure

```
trading-bots-comparison-20/
├── src/
│   ├── core/              # Core framework components
│   │   ├── base_bot.py    # Base trading bot class
│   │   ├── metrics.py     # Performance metrics calculator
│   │   ├── delta_api.py   # Delta Exchange API client
│   │   └── backtest_engine.py
│   ├── bots/              # Bot implementations
│   │   ├── freqtrade_bot.py
│   │   ├── jesse_bot.py
│   │   ├── ccxt_bot.py
│   │   ├── backtrader_bot.py
│   │   ├── additional_bots.py
│   │   └── strategy_bots.py
│   ├── analysis/          # Analysis and reporting
│   │   ├── visualizer.py
│   │   └── report_generator.py
│   └── utils/             # Utility functions
│       └── exporters.py
├── tests/                 # Test suite
│   ├── bots/             # Bot-specific tests
│   └── integration/      # Integration tests
├── main.py               # Main execution script
├── requirements.txt      # Python dependencies
└── config.json.example   # Example configuration
```

## 🔧 Customization

### Adding a New Bot

1. Create a new bot class in `src/bots/`:

```python
from src.core.base_bot import BaseTradingBot

class MyCustomBot(BaseTradingBot):
    def __init__(self, config):
        super().__init__("MyBot", config)
    
    def initialize(self, data):
        pass
    
    def generate_signals(self, data):
        # Your strategy logic here
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        return signals
    
    def execute_trade(self, signal, timestamp, price, capital):
        # Your trade execution logic
        pass
```

2. Import and add it to `main.py`:

```python
from src.bots.my_custom_bot import MyCustomBot

# In initialize_all_bots():
bots.append(MyCustomBot(config))
```

### Customizing Visualizations

Edit `src/analysis/visualizer.py` to modify chart styles, colors, or add new charts.

### Modifying Performance Metrics

Update `src/core/metrics.py` to add custom performance calculations.

## 📝 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## ⚠️ Disclaimer

This framework is for educational and research purposes only. Past performance does not guarantee future results. Always perform your own due diligence before trading with real money.

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for algorithmic trading research**
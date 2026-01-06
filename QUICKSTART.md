# Quick Start Guide

## Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AdityaTheEmpire/trading-bots-comparison-20.git
   cd trading-bots-comparison-20
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Settings**
   ```bash
   cp config.json.example config.json
   # Edit config.json with your settings
   ```

## Running the Comparison

Simply execute:
```bash
python main.py
```

This will:
- Initialize all 20 trading bots
- Run backtests on historical data from Delta Exchange
- Calculate comprehensive performance metrics
- Generate 6 visualization charts
- Create a detailed markdown report
- Export results to JSON and CSV

## Understanding the Results

### Output Files

**Results Directory (`results/`)**
- `aggregated_results.csv` - Summary metrics for all bots
- `aggregated_results.json` - Same data in JSON format
- `detailed_trades.json` - Individual trade records

**Reports Directory (`reports/`)**
- `comparison_report.md` - Main comparison report
- `returns_comparison.png` - Bar chart of returns
- `sharpe_ratio_comparison.png` - Risk-adjusted returns
- `max_drawdown_comparison.png` - Drawdown analysis
- `win_rate_comparison.png` - Win percentages
- `profit_factor_comparison.png` - Profit/loss ratios
- `performance_heatmap.png` - Normalized metrics overview

### Key Metrics Explained

**Total Return**: Overall profit/loss percentage
- Higher is better
- Shows raw profitability

**Sharpe Ratio**: Risk-adjusted return
- > 1.0 = Good
- > 2.0 = Very Good  
- > 3.0 = Excellent
- Accounts for volatility

**Maximum Drawdown**: Worst peak-to-trough loss
- Lower is better
- Indicates downside risk

**Win Rate**: Percentage of profitable trades
- Higher = more consistent
- Not always correlated with profitability

**Profit Factor**: Gross profit / Gross loss
- > 1.0 = Profitable
- > 2.0 = Excellent
- Measures reward/risk

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific tests
pytest tests/bots/test_all_bots.py
pytest tests/integration/test_integration.py
```

## Customization

### Modify Backtest Period

Edit `config.json`:
```json
{
  "backtest_settings": {
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    ...
  }
}
```

### Change Trading Pairs

Edit `config.json`:
```json
{
  "backtest_settings": {
    "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
    ...
  }
}
```

### Adjust Initial Capital

Edit `config.json`:
```json
{
  "backtest_settings": {
    "initial_capital": 100000,
    ...
  }
}
```

## Adding Custom Bots

See README.md for detailed instructions on creating custom trading bots.

## Troubleshooting

**Import Errors**
```bash
pip install -r requirements.txt --upgrade
```

**Missing Dependencies**
```bash
pip install pandas numpy matplotlib seaborn pytest
```

**API Issues**
- Check your Delta Exchange API credentials in `config.json`
- Ensure testnet mode is enabled for testing

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review test files for examples

---

**Happy Trading! 📈**

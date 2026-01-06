"""
Report generator for creating markdown reports.
"""
import pandas as pd
from typing import Dict, List
from datetime import datetime
import os


class ReportGenerator:
    """
    Generate comprehensive markdown reports for bot comparison.
    """
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_markdown_report(self, df: pd.DataFrame, 
                                 filename: str = "comparison_report.md") -> str:
        """
        Generate a detailed markdown report.
        
        Args:
            df: DataFrame with aggregated results
            filename: Output filename
            
        Returns:
            Path to generated report
        """
        report_lines = []
        
        # Header
        report_lines.append("# Trading Bots Performance Comparison Report")
        report_lines.append("")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("## Executive Summary")
        report_lines.append("")
        report_lines.append(f"This report compares the performance of **{len(df)} trading bots** ")
        report_lines.append("across multiple performance metrics including profitability, risk-adjusted returns, ")
        report_lines.append("and trading efficiency.")
        report_lines.append("")
        
        # Top Performers
        report_lines.append("## Top Performers")
        report_lines.append("")
        
        # Best by return
        best_return = df.loc[df['total_return_pct'].idxmax()]
        report_lines.append(f"### 🏆 Highest Return: **{best_return['bot_name']}**")
        report_lines.append(f"- Total Return: **{best_return['total_return_pct']:.2f}%**")
        report_lines.append(f"- Sharpe Ratio: {best_return['sharpe_ratio']:.2f}")
        report_lines.append(f"- Max Drawdown: {best_return['max_drawdown_pct']:.2f}%")
        report_lines.append("")
        
        # Best Sharpe ratio
        best_sharpe = df.loc[df['sharpe_ratio'].idxmax()]
        report_lines.append(f"### 📊 Best Risk-Adjusted Return: **{best_sharpe['bot_name']}**")
        report_lines.append(f"- Sharpe Ratio: **{best_sharpe['sharpe_ratio']:.2f}**")
        report_lines.append(f"- Total Return: {best_sharpe['total_return_pct']:.2f}%")
        report_lines.append(f"- Win Rate: {best_sharpe['win_rate_pct']:.2f}%")
        report_lines.append("")
        
        # Lowest drawdown
        best_dd = df.loc[df['max_drawdown_pct'].idxmin()]
        report_lines.append(f"### 🛡️ Lowest Risk: **{best_dd['bot_name']}**")
        report_lines.append(f"- Max Drawdown: **{best_dd['max_drawdown_pct']:.2f}%**")
        report_lines.append(f"- Total Return: {best_dd['total_return_pct']:.2f}%")
        report_lines.append(f"- Sharpe Ratio: {best_dd['sharpe_ratio']:.2f}")
        report_lines.append("")
        
        # Complete Rankings
        report_lines.append("## Complete Rankings by Profitability")
        report_lines.append("")
        
        df_ranked = df.sort_values('total_return_pct', ascending=False).reset_index(drop=True)
        df_ranked.index = df_ranked.index + 1
        
        report_lines.append("| Rank | Bot Name | Total Return | Sharpe Ratio | Win Rate | Profit Factor | Max Drawdown |")
        report_lines.append("|------|----------|--------------|--------------|----------|---------------|--------------|")
        
        for idx, row in df_ranked.iterrows():
            pf_display = f"{row['profit_factor']:.2f}" if row['profit_factor'] != float('inf') else "∞"
            report_lines.append(
                f"| {idx} | {row['bot_name']} | "
                f"{row['total_return_pct']:.2f}% | "
                f"{row['sharpe_ratio']:.2f} | "
                f"{row['win_rate_pct']:.2f}% | "
                f"{pf_display} | "
                f"{row['max_drawdown_pct']:.2f}% |"
            )
        
        report_lines.append("")
        
        # Detailed Metrics
        report_lines.append("## Detailed Performance Metrics")
        report_lines.append("")
        
        for idx, row in df_ranked.iterrows():
            report_lines.append(f"### {idx}. {row['bot_name']}")
            report_lines.append("")
            report_lines.append("**Returns & Profitability:**")
            report_lines.append(f"- Initial Capital: ${row['initial_capital']:,.2f}")
            report_lines.append(f"- Final Value: ${row['final_value']:,.2f}")
            report_lines.append(f"- Total Return: {row['total_return_pct']:.2f}%")
            report_lines.append(f"- Total Trades: {int(row['total_trades'])}")
            report_lines.append("")
            report_lines.append("**Risk Metrics:**")
            report_lines.append(f"- Sharpe Ratio: {row['sharpe_ratio']:.2f}")
            report_lines.append(f"- Maximum Drawdown: {row['max_drawdown_pct']:.2f}%")
            report_lines.append(f"- Drawdown Duration: {int(row['duration'])} periods")
            report_lines.append("")
            report_lines.append("**Trading Efficiency:**")
            report_lines.append(f"- Win Rate: {row['win_rate_pct']:.2f}%")
            pf_display = f"{row['profit_factor']:.2f}" if row['profit_factor'] != float('inf') else "∞"
            report_lines.append(f"- Profit Factor: {pf_display}")
            report_lines.append("")
        
        # Performance Summary Statistics
        report_lines.append("## Summary Statistics")
        report_lines.append("")
        report_lines.append("| Metric | Mean | Median | Min | Max | Std Dev |")
        report_lines.append("|--------|------|--------|-----|-----|---------|")
        
        metrics_to_summarize = {
            'Total Return (%)': 'total_return_pct',
            'Sharpe Ratio': 'sharpe_ratio',
            'Win Rate (%)': 'win_rate_pct',
            'Max Drawdown (%)': 'max_drawdown_pct'
        }
        
        for metric_name, col_name in metrics_to_summarize.items():
            if col_name in df.columns:
                report_lines.append(
                    f"| {metric_name} | "
                    f"{df[col_name].mean():.2f} | "
                    f"{df[col_name].median():.2f} | "
                    f"{df[col_name].min():.2f} | "
                    f"{df[col_name].max():.2f} | "
                    f"{df[col_name].std():.2f} |"
                )
        
        report_lines.append("")
        
        # Visualizations
        report_lines.append("## Visualizations")
        report_lines.append("")
        report_lines.append("The following charts provide visual comparisons of bot performance:")
        report_lines.append("")
        report_lines.append("1. **Returns Comparison** - `returns_comparison.png`")
        report_lines.append("2. **Sharpe Ratio Comparison** - `sharpe_ratio_comparison.png`")
        report_lines.append("3. **Maximum Drawdown Comparison** - `max_drawdown_comparison.png`")
        report_lines.append("4. **Win Rate Comparison** - `win_rate_comparison.png`")
        report_lines.append("5. **Profit Factor Comparison** - `profit_factor_comparison.png`")
        report_lines.append("6. **Performance Heatmap** - `performance_heatmap.png`")
        report_lines.append("")
        
        # Methodology
        report_lines.append("## Methodology")
        report_lines.append("")
        report_lines.append("### Data Source")
        report_lines.append("- Market data obtained via Delta Exchange API")
        report_lines.append("- Historical OHLCV data used for backtesting")
        report_lines.append("")
        report_lines.append("### Performance Metrics")
        report_lines.append("")
        report_lines.append("**Sharpe Ratio:** Measures risk-adjusted returns. Higher is better. ")
        report_lines.append("Values > 1 are considered good, > 2 are very good, > 3 are excellent.")
        report_lines.append("")
        report_lines.append("**Maximum Drawdown:** The largest peak-to-trough decline. ")
        report_lines.append("Lower values indicate better risk management.")
        report_lines.append("")
        report_lines.append("**Win Rate:** Percentage of profitable trades. ")
        report_lines.append("Higher values indicate more consistent performance.")
        report_lines.append("")
        report_lines.append("**Profit Factor:** Gross profit divided by gross loss. ")
        report_lines.append("Values > 1 indicate profitability, > 2 is excellent.")
        report_lines.append("")
        
        # Conclusion
        report_lines.append("## Conclusion")
        report_lines.append("")
        report_lines.append("This comparison provides insights into the relative performance of different ")
        report_lines.append("trading strategies. The best bot depends on your risk tolerance and investment goals:")
        report_lines.append("")
        report_lines.append(f"- For **maximum returns**: {best_return['bot_name']}")
        report_lines.append(f"- For **risk-adjusted returns**: {best_sharpe['bot_name']}")
        report_lines.append(f"- For **risk management**: {best_dd['bot_name']}")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("*This report was automatically generated by the Trading Bots Comparison Framework.*")
        
        # Write report
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write('\n'.join(report_lines))
        
        print(f"Report generated: {filepath}")
        return filepath

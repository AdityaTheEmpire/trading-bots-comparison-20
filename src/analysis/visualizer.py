"""
Visualization module for creating performance charts.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict
import os


class PerformanceVisualizer:
    """
    Create visualization charts for bot performance comparison.
    """
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize visualizer.
        
        Args:
            output_dir: Directory to save charts
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        
    def plot_returns_comparison(self, df: pd.DataFrame, filename: str = "returns_comparison.png"):
        """
        Plot total returns comparison across bots.
        
        Args:
            df: DataFrame with bot results
            filename: Output filename
        """
        plt.figure(figsize=(14, 8))
        
        df_sorted = df.sort_values('total_return_pct', ascending=True)
        colors = ['red' if x < 0 else 'green' for x in df_sorted['total_return_pct']]
        
        plt.barh(df_sorted['bot_name'], df_sorted['total_return_pct'], color=colors, alpha=0.7)
        plt.xlabel('Total Return (%)', fontsize=12)
        plt.ylabel('Bot Name', fontsize=12)
        plt.title('Trading Bots Performance Comparison - Total Returns', fontsize=14, fontweight='bold')
        plt.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
        plt.grid(axis='x', alpha=0.3)
        
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: {filepath}")
        
    def plot_sharpe_ratio_comparison(self, df: pd.DataFrame, filename: str = "sharpe_ratio_comparison.png"):
        """
        Plot Sharpe ratio comparison.
        
        Args:
            df: DataFrame with bot results
            filename: Output filename
        """
        plt.figure(figsize=(14, 8))
        
        df_sorted = df.sort_values('sharpe_ratio', ascending=True)
        colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(df_sorted)))
        
        plt.barh(df_sorted['bot_name'], df_sorted['sharpe_ratio'], color=colors, alpha=0.7)
        plt.xlabel('Sharpe Ratio', fontsize=12)
        plt.ylabel('Bot Name', fontsize=12)
        plt.title('Trading Bots Sharpe Ratio Comparison', fontsize=14, fontweight='bold')
        plt.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
        plt.axvline(x=1, color='blue', linestyle='--', linewidth=0.8, alpha=0.5, label='Sharpe=1')
        plt.grid(axis='x', alpha=0.3)
        plt.legend()
        
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: {filepath}")
        
    def plot_max_drawdown_comparison(self, df: pd.DataFrame, filename: str = "max_drawdown_comparison.png"):
        """
        Plot maximum drawdown comparison.
        
        Args:
            df: DataFrame with bot results
            filename: Output filename
        """
        plt.figure(figsize=(14, 8))
        
        df_sorted = df.sort_values('max_drawdown_pct', ascending=False)
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(df_sorted)))
        
        plt.barh(df_sorted['bot_name'], df_sorted['max_drawdown_pct'], color=colors, alpha=0.7)
        plt.xlabel('Maximum Drawdown (%)', fontsize=12)
        plt.ylabel('Bot Name', fontsize=12)
        plt.title('Trading Bots Maximum Drawdown Comparison', fontsize=14, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: {filepath}")
        
    def plot_win_rate_comparison(self, df: pd.DataFrame, filename: str = "win_rate_comparison.png"):
        """
        Plot win rate comparison.
        
        Args:
            df: DataFrame with bot results
            filename: Output filename
        """
        plt.figure(figsize=(14, 8))
        
        df_sorted = df.sort_values('win_rate_pct', ascending=True)
        colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(df_sorted)))
        
        plt.barh(df_sorted['bot_name'], df_sorted['win_rate_pct'], color=colors, alpha=0.7)
        plt.xlabel('Win Rate (%)', fontsize=12)
        plt.ylabel('Bot Name', fontsize=12)
        plt.title('Trading Bots Win Rate Comparison', fontsize=14, fontweight='bold')
        plt.axvline(x=50, color='black', linestyle='--', linewidth=0.8, alpha=0.5, label='50%')
        plt.grid(axis='x', alpha=0.3)
        plt.xlim(0, 100)
        plt.legend()
        
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: {filepath}")
        
    def plot_profit_factor_comparison(self, df: pd.DataFrame, filename: str = "profit_factor_comparison.png"):
        """
        Plot profit factor comparison.
        
        Args:
            df: DataFrame with bot results
            filename: Output filename
        """
        plt.figure(figsize=(14, 8))
        
        # Cap profit factor for visualization
        df_plot = df.copy()
        df_plot['profit_factor_capped'] = df_plot['profit_factor'].apply(lambda x: min(x, 5) if x != float('inf') else 5)
        
        df_sorted = df_plot.sort_values('profit_factor_capped', ascending=True)
        colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(df_sorted)))
        
        plt.barh(df_sorted['bot_name'], df_sorted['profit_factor_capped'], color=colors, alpha=0.7)
        plt.xlabel('Profit Factor (capped at 5)', fontsize=12)
        plt.ylabel('Bot Name', fontsize=12)
        plt.title('Trading Bots Profit Factor Comparison', fontsize=14, fontweight='bold')
        plt.axvline(x=1, color='black', linestyle='--', linewidth=0.8, alpha=0.5, label='PF=1')
        plt.grid(axis='x', alpha=0.3)
        plt.legend()
        
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: {filepath}")
        
    def plot_performance_heatmap(self, df: pd.DataFrame, filename: str = "performance_heatmap.png"):
        """
        Create a heatmap of normalized performance metrics.
        
        Args:
            df: DataFrame with bot results
            filename: Output filename
        """
        plt.figure(figsize=(14, 10))
        
        # Select key metrics
        metrics = ['total_return_pct', 'sharpe_ratio', 'win_rate_pct', 'profit_factor', 'max_drawdown_pct']
        available_metrics = [m for m in metrics if m in df.columns]
        
        if not available_metrics:
            print("No metrics available for heatmap")
            return
        
        # Normalize metrics (except max_drawdown which is inverted)
        df_norm = df[['bot_name'] + available_metrics].copy()
        for metric in available_metrics:
            if metric == 'max_drawdown_pct':
                # Lower is better for drawdown
                df_norm[metric] = 100 - df_norm[metric]
            elif metric == 'profit_factor':
                # Cap and normalize profit factor
                df_norm[metric] = df_norm[metric].apply(lambda x: min(x, 5) if x != float('inf') else 5)
            
            # Normalize to 0-100 scale
            min_val = df_norm[metric].min()
            max_val = df_norm[metric].max()
            if max_val != min_val:
                df_norm[metric] = ((df_norm[metric] - min_val) / (max_val - min_val)) * 100
        
        # Create heatmap
        df_heatmap = df_norm.set_index('bot_name')[available_metrics]
        
        sns.heatmap(df_heatmap, annot=True, fmt='.1f', cmap='RdYlGn', 
                   cbar_kws={'label': 'Normalized Score (0-100)'},
                   linewidths=0.5)
        
        plt.title('Trading Bots Performance Heatmap (Normalized Metrics)', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.ylabel('Bot Name', fontsize=12)
        plt.xlabel('Performance Metric', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: {filepath}")
        
    def create_all_charts(self, df: pd.DataFrame):
        """
        Create all visualization charts.
        
        Args:
            df: DataFrame with bot results
        """
        print("Creating visualization charts...")
        
        self.plot_returns_comparison(df)
        self.plot_sharpe_ratio_comparison(df)
        self.plot_max_drawdown_comparison(df)
        self.plot_win_rate_comparison(df)
        self.plot_profit_factor_comparison(df)
        self.plot_performance_heatmap(df)
        
        print("All charts created successfully!")

"""
Specialized visualization for evaluation metrics and performance analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from sklearn.metrics import confusion_matrix, roc_curve, auc
import plotly.graph_objects as go
import plotly.express as px

class MetricsVisualizer:
    """Specialized visualizations for detection metrics and performance analysis"""
    
    def __init__(self, style: str = "whitegrid"):
        self.style = style
        sns.set_style(style)
        
        self.color_palette = {
            'excellent': '#2E8B57',  # Sea Green
            'good': '#4682B4',       # Steel Blue  
            'warning': '#FF8C00',    # Dark Orange
            'poor': '#DC143C',       # Crimson
            'neutral': '#708090'     # Slate Gray
        }
    
    def plot_confusion_matrices(self, results: Dict, figsize: Tuple[int, int] = (15, 5)) -> plt.Figure:
        """
        Plot confusion matrices for all detectors
        
        Args:
            results: Dictionary with detector results including confusion matrices
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        detectors = list(results.keys())
        n_detectors = len(detectors)
        
        fig, axes = plt.subplots(1, n_detectors, figsize=figsize)
        if n_detectors == 1:
            axes = [axes]
        
        for i, detector in enumerate(detectors):
            if 'confusion_matrix' in results[detector]:
                cm = results[detector]['confusion_matrix']
                
                # Create heatmap
                sns.heatmap(
                    cm, 
                    annot=True, 
                    fmt='d', 
                    cmap='Blues',
                    ax=axes[i],
                    xticklabels=['Benign', 'Jailbreak'],
                    yticklabels=['Benign', 'Jailbreak']
                )
                
                axes[i].set_title(f'{detector}\nAccuracy: {results[detector].get("accuracy", 0):.3f}')
                axes[i].set_xlabel('Predicted')
                axes[i].set_ylabel('Actual')
        
        plt.tight_layout()
        return fig
    
    def plot_roc_curves(self, results: Dict, figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
        """
        Plot ROC curves for all detectors
        
        Args:
            results: Dictionary with detector results including ROC data
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        colors = plt.cm.Set1(np.linspace(0, 1, len(results)))
        
        for i, (detector, data) in enumerate(results.items()):
            if 'roc_curve' in data:
                roc_data = data['roc_curve']
                ax.plot(
                    roc_data['fpr'], 
                    roc_data['tpr'],
                    color=colors[i],
                    lw=2,
                    label=f'{detector} (AUC = {roc_data["auc"]:.3f})'
                )
        
        # Plot diagonal line
        ax.plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.5)
        
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('ROC Curves - Jailbreak Detection Performance')
        ax.legend(loc="lower right")
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def plot_precision_recall_curves(self, results: Dict, figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
        """
        Plot Precision-Recall curves for all detectors
        
        Args:
            results: Dictionary with detector results including PR data
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        colors = plt.cm.Set2(np.linspace(0, 1, len(results)))
        
        for i, (detector, data) in enumerate(results.items()):
            if 'pr_curve' in data:
                pr_data = data['pr_curve']
                ax.plot(
                    pr_data['recall'], 
                    pr_data['precision'],
                    color=colors[i],
                    lw=2,
                    label=f'{detector} (AP = {pr_data["average_precision"]:.3f})'
                )
        
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.set_title('Precision-Recall Curves - Jailbreak Detection')
        ax.legend(loc="lower left")
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def plot_metrics_radar(self, results: Dict, figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Create radar chart comparing multiple metrics across detectors
        
        Args:
            results: Dictionary with detector results
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        metrics = ['precision', 'recall', 'f1', 'accuracy']
        detectors = list(results.keys())
        
        # Number of metrics
        num_metrics = len(metrics)
        angles = np.linspace(0, 2 * np.pi, num_metrics, endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='polar'))
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(detectors)))
        
        for i, detector in enumerate(detectors):
            values = [results[detector].get(metric, 0) for metric in metrics]
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, label=detector, color=colors[i])
            ax.fill(angles, values, alpha=0.25, color=colors[i])
        
        # Customize the radar chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics)
        ax.set_ylim(0, 1)
        ax.set_title('Detection Performance Radar Chart', y=1.08)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.grid(True)
        
        return fig
    
    def plot_performance_distribution(self, results: Dict, figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Plot distribution of performance metrics
        
        Args:
            results: Dictionary with detector results
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        # Prepare data for plotting
        metrics_data = []
        for detector, data in results.items():
            for metric in ['asr', 'fpr', 'precision', 'recall', 'f1']:
                if metric in data:
                    metrics_data.append({
                        'Detector': detector,
                        'Metric': metric.upper(),
                        'Value': data[metric]
                    })
        
        df = pd.DataFrame(metrics_data)
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        axes = axes.ravel()
        
        # 1. Box plot of all metrics
        sns.boxplot(data=df, x='Metric', y='Value', ax=axes[0])
        axes[0].set_title('Distribution of All Metrics')
        axes[0].set_ylim(0, 1)
        
        # 2. Bar plot comparing detectors
        pivot_df = df.pivot(index='Detector', columns='Metric', values='Value')
        pivot_df.plot(kind='bar', ax=axes[1], rot=45)
        axes[1].set_title('Performance Comparison by Detector')
        axes[1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 3. Heatmap of all metrics
        sns.heatmap(pivot_df.T, annot=True, fmt='.3f', cmap='RdYlBu_r', ax=axes[2])
        axes[2].set_title('Performance Heatmap')
        
        # 4. Scatter plot: ASR vs FPR
        asr_data = df[df['Metric'] == 'ASR']
        fpr_data = df[df['Metric'] == 'FPR']
        
        if not asr_data.empty and not fpr_data.empty:
            for detector in results.keys():
                asr_val = results[detector].get('asr', 0)
                fpr_val = results[detector].get('fpr', 0)
                axes[3].scatter(fpr_val, asr_val, s=100, label=detector)
                axes[3].annotate(detector, (fpr_val, asr_val), 
                               xytext=(5, 5), textcoords='offset points')
        
        axes[3].set_xlabel('False Positive Rate')
        axes[3].set_ylabel('Attack Success Rate')
        axes[3].set_title('ASR vs FPR Trade-off')
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_performance_summary_table(self, results: Dict) -> pd.DataFrame:
        """
        Create a comprehensive performance summary table
        
        Args:
            results: Dictionary with detector results
            
        Returns:
            Pandas DataFrame with formatted results
        """
        summary_data = []
        
        for detector, data in results.items():
            row = {
                'Detector': detector,
                'Attack Success Rate': f"{data.get('asr', 0):.3f}",
                'False Positive Rate': f"{data.get('fpr', 0):.3f}",
                'Precision': f"{data.get('precision', 0):.3f}",
                'Recall': f"{data.get('recall', 0):.3f}",
                'F1 Score': f"{data.get('f1', 0):.3f}",
                'Accuracy': f"{data.get('accuracy', 0):.3f}",
            }
            
            # Add performance grade
            f1_score = data.get('f1', 0)
            if f1_score >= 0.9:
                row['Grade'] = 'A+ (Excellent)'
            elif f1_score >= 0.8:
                row['Grade'] = 'A (Very Good)'
            elif f1_score >= 0.7:
                row['Grade'] = 'B (Good)'
            elif f1_score >= 0.6:
                row['Grade'] = 'C (Fair)'
            else:
                row['Grade'] = 'D (Needs Improvement)'
            
            summary_data.append(row)
        
        df = pd.DataFrame(summary_data)
        return df.round(3)
    
    def save_all_metric_plots(self, results: Dict, output_dir: str = "./plots/metrics"):
        """
        Generate and save all metric visualization types
        
        Args:
            results: Evaluation results dictionary
            output_dir: Directory to save plots
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Confusion matrices
            fig_cm = self.plot_confusion_matrices(results)
            fig_cm.savefig(f"{output_dir}/confusion_matrices.png", dpi=300, bbox_inches='tight')
            plt.close(fig_cm)
            
            # Performance distribution
            fig_dist = self.plot_performance_distribution(results)
            fig_dist.savefig(f"{output_dir}/performance_distribution.png", dpi=300, bbox_inches='tight')
            plt.close(fig_dist)
            
            # Radar chart
            fig_radar = self.plot_metrics_radar(results)
            fig_radar.savefig(f"{output_dir}/performance_radar.png", dpi=300, bbox_inches='tight')
            plt.close(fig_radar)
            
            # Summary table
            summary_df = self.create_performance_summary_table(results)
            summary_df.to_csv(f"{output_dir}/performance_summary.csv", index=False)
            
            print(f"✓ Metric plots saved to {output_dir}/")
            print("  - confusion_matrices.png")
            print("  - performance_distribution.png") 
            print("  - performance_radar.png")
            print("  - performance_summary.csv")
            
        except Exception as e:
            print(f"Error saving metric plots: {e}")
            
        return output_dir
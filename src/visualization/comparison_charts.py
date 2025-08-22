"""
Comparison charts for detector performance analysis and benchmarking
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class ComparisonCharts:
    """Create comprehensive comparison visualizations for detector performance"""
    
    def __init__(self, style: str = "whitegrid"):
        self.style = style
        sns.set_style(style)
        
        # Professional color scheme
        self.colors = {
            'primary': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            'secondary': ['#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
            'gradient': ['#440154', '#31688e', '#35b779', '#fde725']
        }
    
    def create_detector_comparison_chart(self, results: Dict, 
                                       metrics: List[str] = None,
                                       chart_type: str = 'bar') -> go.Figure:
        """
        Create comprehensive detector comparison chart
        
        Args:
            results: Dictionary with detector results
            metrics: List of metrics to compare
            chart_type: 'bar', 'radar', or 'heatmap'
            
        Returns:
            Plotly figure object
        """
        if metrics is None:
            metrics = ['precision', 'recall', 'f1', 'accuracy']
        
        detector_names = list(results.keys())
        
        if chart_type == 'bar':
            return self._create_grouped_bar_chart(results, metrics, detector_names)
        elif chart_type == 'radar':
            return self._create_radar_comparison(results, metrics, detector_names)
        elif chart_type == 'heatmap':
            return self._create_heatmap_comparison(results, metrics, detector_names)
        else:
            raise ValueError("chart_type must be 'bar', 'radar', or 'heatmap'")
    
    def _create_grouped_bar_chart(self, results: Dict, metrics: List[str], 
                                 detector_names: List[str]) -> go.Figure:
        """Create grouped bar chart for detector comparison"""
        fig = go.Figure()
        
        x_pos = np.arange(len(detector_names))
        bar_width = 0.15
        
        for i, metric in enumerate(metrics):
            values = [results[det].get(metric, 0) for det in detector_names]
            
            fig.add_trace(go.Bar(
                x=detector_names,
                y=values,
                name=metric.upper(),
                marker_color=self.colors['primary'][i % len(self.colors['primary'])],
                text=[f'{v:.3f}' for v in values],
                textposition='auto',
            ))
        
        fig.update_layout(
            title="Detector Performance Comparison",
            xaxis_title="Detectors",
            yaxis_title="Score",
            barmode='group',
            yaxis=dict(range=[0, 1]),
            template="plotly_white",
            height=600
        )
        
        return fig
    
    def _create_radar_comparison(self, results: Dict, metrics: List[str], 
                               detector_names: List[str]) -> go.Figure:
        """Create radar chart for detector comparison"""
        fig = go.Figure()
        
        # Create angles for radar chart
        angles = list(np.linspace(0, 2 * np.pi, len(metrics), endpoint=False))
        angles += angles[:1]  # Complete the circle
        
        for i, detector in enumerate(detector_names):
            values = [results[detector].get(metric, 0) for metric in metrics]
            values += values[:1]  # Complete the circle
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics + [metrics[0]],
                fill='toself',
                name=detector,
                line_color=self.colors['primary'][i % len(self.colors['primary'])]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Detector Performance Radar Chart",
            height=600
        )
        
        return fig
    
    def _create_heatmap_comparison(self, results: Dict, metrics: List[str], 
                                 detector_names: List[str]) -> go.Figure:
        """Create heatmap for detector comparison"""
        # Create matrix
        matrix = []
        for detector in detector_names:
            row = [results[detector].get(metric, 0) for metric in metrics]
            matrix.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=metrics,
            y=detector_names,
            colorscale='RdYlBu_r',
            text=[[f'{val:.3f}' for val in row] for row in matrix],
            texttemplate="%{text}",
            textfont={"size": 12},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Detector Performance Heatmap",
            xaxis_title="Metrics",
            yaxis_title="Detectors",
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    def create_performance_ranking(self, results: Dict, 
                                 primary_metric: str = 'f1') -> go.Figure:
        """
        Create ranking visualization based on primary metric
        
        Args:
            results: Dictionary with detector results
            primary_metric: Metric to use for ranking
            
        Returns:
            Plotly figure object
        """
        # Sort detectors by primary metric
        sorted_detectors = sorted(results.items(), 
                                key=lambda x: x[1].get(primary_metric, 0), 
                                reverse=True)
        
        detector_names = [item[0] for item in sorted_detectors]
        primary_scores = [item[1].get(primary_metric, 0) for item in sorted_detectors]
        
        # Create ranking chart
        fig = go.Figure()
        
        # Add primary metric bars
        fig.add_trace(go.Bar(
            x=detector_names,
            y=primary_scores,
            name=primary_metric.upper(),
            marker_color='lightblue',
            text=[f'{score:.3f}' for score in primary_scores],
            textposition='auto'
        ))
        
        # Add ranking annotations
        for i, (detector, score) in enumerate(zip(detector_names, primary_scores)):
            fig.add_annotation(
                x=detector,
                y=score + 0.05,
                text=f"#{i+1}",
                showarrow=False,
                font=dict(size=14, color="red"),
                bgcolor="white",
                bordercolor="red",
                borderwidth=1
            )
        
        fig.update_layout(
            title=f"Detector Ranking by {primary_metric.upper()}",
            xaxis_title="Detectors",
            yaxis_title=f"{primary_metric.upper()} Score",
            yaxis=dict(range=[0, max(primary_scores) + 0.1]),
            template="plotly_white",
            height=500
        )
        
        return fig
    
    def create_trade_off_analysis(self, results: Dict) -> go.Figure:
        """
        Create trade-off analysis between different metrics
        
        Args:
            results: Dictionary with detector results
            
        Returns:
            Plotly figure object
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Precision vs Recall Trade-off',
                'ASR vs FPR Trade-off', 
                'Speed vs Accuracy Trade-off',
                'Performance vs Complexity'
            ],
            specs=[[{"type": "scatter"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        detector_names = list(results.keys())
        
        # 1. Precision vs Recall
        precision_vals = [results[det].get('precision', 0) for det in detector_names]
        recall_vals = [results[det].get('recall', 0) for det in detector_names]
        
        fig.add_trace(
            go.Scatter(
                x=recall_vals, y=precision_vals,
                mode='markers+text',
                text=detector_names,
                textposition='top center',
                marker=dict(size=12, color='blue'),
                name='PR Trade-off'
            ),
            row=1, col=1
        )
        
        # 2. ASR vs FPR
        asr_vals = [results[det].get('asr', 0) for det in detector_names]
        fpr_vals = [results[det].get('fpr', 0) for det in detector_names]
        
        fig.add_trace(
            go.Scatter(
                x=fpr_vals, y=asr_vals,
                mode='markers+text',
                text=detector_names,
                textposition='top center',
                marker=dict(size=12, color='red'),
                name='ASR vs FPR'
            ),
            row=1, col=2
        )
        
        # 3. Speed vs Accuracy (if available)
        if any('latency' in results[det] for det in detector_names):
            latency_vals = [results[det].get('latency', 0) for det in detector_names]
            accuracy_vals = [results[det].get('accuracy', 0) for det in detector_names]
            
            fig.add_trace(
                go.Scatter(
                    x=latency_vals, y=accuracy_vals,
                    mode='markers+text',
                    text=detector_names,
                    textposition='top center',
                    marker=dict(size=12, color='green'),
                    name='Speed vs Accuracy'
                ),
                row=2, col=1
            )
        
        # 4. Performance vs Complexity (placeholder)
        f1_vals = [results[det].get('f1', 0) for det in detector_names]
        complexity_vals = [np.random.uniform(0.3, 0.9) for _ in detector_names]  # Placeholder
        
        fig.add_trace(
            go.Scatter(
                x=complexity_vals, y=f1_vals,
                mode='markers+text',
                text=detector_names,
                textposition='top center',
                marker=dict(size=12, color='purple'),
                name='Performance vs Complexity'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Performance Trade-off Analysis",
            height=800,
            showlegend=False,
            template="plotly_white"
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="Recall", row=1, col=1)
        fig.update_yaxes(title_text="Precision", row=1, col=1)
        fig.update_xaxes(title_text="False Positive Rate", row=1, col=2)
        fig.update_yaxes(title_text="Attack Success Rate", row=1, col=2)
        fig.update_xaxes(title_text="Latency (ms)", row=2, col=1)
        fig.update_yaxes(title_text="Accuracy", row=2, col=1)
        fig.update_xaxes(title_text="Complexity Score", row=2, col=2)
        fig.update_yaxes(title_text="F1 Score", row=2, col=2)
        
        return fig
    
    def create_dataset_comparison(self, results_by_dataset: Dict) -> go.Figure:
        """
        Compare detector performance across different datasets
        
        Args:
            results_by_dataset: Results organized by dataset
            
        Returns:
            Plotly figure object
        """
        datasets = list(results_by_dataset.keys())
        detectors = list(results_by_dataset[datasets[0]].keys())
        
        fig = go.Figure()
        
        # Create grouped bar chart
        for i, detector in enumerate(detectors):
            f1_scores = [results_by_dataset[dataset][detector].get('f1', 0) 
                        for dataset in datasets]
            
            fig.add_trace(go.Bar(
                x=datasets,
                y=f1_scores,
                name=detector,
                marker_color=self.colors['primary'][i % len(self.colors['primary'])],
                text=[f'{score:.3f}' for score in f1_scores],
                textposition='auto'
            ))
        
        fig.update_layout(
            title="Detector Performance Across Datasets",
            xaxis_title="Datasets",
            yaxis_title="F1 Score",
            barmode='group',
            yaxis=dict(range=[0, 1]),
            template="plotly_white",
            height=600
        )
        
        return fig
    
    def save_all_comparison_charts(self, results: Dict, output_dir: str = "./plots/comparisons"):
        """
        Generate and save all comparison chart types
        
        Args:
            results: Evaluation results dictionary
            output_dir: Directory to save plots
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Bar chart comparison
            fig_bar = self.create_detector_comparison_chart(results, chart_type='bar')
            fig_bar.write_html(f"{output_dir}/detector_comparison_bar.html")
            
            # Radar chart comparison
            fig_radar = self.create_detector_comparison_chart(results, chart_type='radar')
            fig_radar.write_html(f"{output_dir}/detector_comparison_radar.html")
            
            # Heatmap comparison
            fig_heatmap = self.create_detector_comparison_chart(results, chart_type='heatmap')
            fig_heatmap.write_html(f"{output_dir}/detector_comparison_heatmap.html")
            
            # Performance ranking
            fig_ranking = self.create_performance_ranking(results)
            fig_ranking.write_html(f"{output_dir}/performance_ranking.html")
            
            # Trade-off analysis
            fig_tradeoff = self.create_trade_off_analysis(results)
            fig_tradeoff.write_html(f"{output_dir}/trade_off_analysis.html")
            
            print(f"✓ Comparison charts saved to {output_dir}/")
            print("  - detector_comparison_bar.html")
            print("  - detector_comparison_radar.html")
            print("  - detector_comparison_heatmap.html")
            print("  - performance_ranking.html")
            print("  - trade_off_analysis.html")
            
        except Exception as e:
            print(f"Error saving comparison charts: {e}")
            
        return output_dir
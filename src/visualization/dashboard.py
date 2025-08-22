"""
Comprehensive results dashboard for jailbreak detection analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

class ResultsDashboard:
    """Create comprehensive visualization dashboards for detection results"""
    
    def __init__(self, style: str = "whitegrid", figsize: Tuple[int, int] = (15, 10)):
        """
        Initialize dashboard with styling options
        
        Args:
            style: Seaborn style ('whitegrid', 'darkgrid', 'white', 'dark', 'ticks')
            figsize: Default figure size
        """
        self.style = style
        self.figsize = figsize
        sns.set_style(style)
        plt.style.use('seaborn-v0_8')
        
        # Color palette for consistency
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72', 
            'success': '#F18F01',
            'danger': '#C73E1D',
            'warning': '#F4B942',
            'info': '#6C5CE7'
        }
    
    def create_overview_dashboard(self, results: Dict, save_path: Optional[str] = None) -> go.Figure:
        """
        Create comprehensive overview dashboard with multiple metrics
        
        Args:
            results: Dictionary containing evaluation results for multiple detectors
            save_path: Optional path to save the plot
            
        Returns:
            Plotly figure object
        """
        # Extract data
        detector_names = list(results.keys())
        metrics = ['asr', 'fpr', 'precision', 'recall', 'f1']
        
        # Create subplot structure
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=[
                'Attack Success Rate vs False Positive Rate',
                'Precision vs Recall',
                'F1 Score Comparison',
                'Detection Performance Heatmap',
                'Confusion Matrix Summary',
                'ROC Curves'
            ],
            specs=[
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "heatmap"}],
                [{"type": "bar"}, {"type": "scatter"}]
            ]
        )
        
        # 1. ASR vs FPR scatter plot
        asr_vals = [results[det]['asr'] for det in detector_names]
        fpr_vals = [results[det]['fpr'] for det in detector_names]
        
        fig.add_trace(
            go.Scatter(
                x=fpr_vals, y=asr_vals,
                mode='markers+text',
                text=detector_names,
                textposition='top center',
                marker=dict(size=12, color=self.colors['primary']),
                name='Detectors'
            ),
            row=1, col=1
        )
        
        # 2. Precision vs Recall
        precision_vals = [results[det]['precision'] for det in detector_names]
        recall_vals = [results[det]['recall'] for det in detector_names]
        
        fig.add_trace(
            go.Scatter(
                x=recall_vals, y=precision_vals,
                mode='markers+text',
                text=detector_names,
                textposition='top center',
                marker=dict(size=12, color=self.colors['secondary']),
                name='PR Space'
            ),
            row=1, col=2
        )
        
        # 3. F1 Score comparison
        f1_vals = [results[det]['f1'] for det in detector_names]
        
        fig.add_trace(
            go.Bar(
                x=detector_names, y=f1_vals,
                marker_color=self.colors['success'],
                name='F1 Score'
            ),
            row=2, col=1
        )
        
        # 4. Performance heatmap
        metrics_matrix = []
        for det in detector_names:
            metrics_matrix.append([results[det][metric] for metric in metrics])
        
        fig.add_trace(
            go.Heatmap(
                z=metrics_matrix,
                x=metrics,
                y=detector_names,
                colorscale='RdYlBu_r',
                name='Performance Matrix'
            ),
            row=2, col=2
        )
        
        # 5. Confusion matrix summary (if available)
        if 'confusion_matrix' in results[detector_names[0]]:
            cm_data = []
            for det in detector_names:
                cm = results[det]['confusion_matrix']
                cm_data.append([cm[0][0], cm[0][1], cm[1][0], cm[1][1]])
            
            cm_df = pd.DataFrame(cm_data, 
                               columns=['TN', 'FP', 'FN', 'TP'],
                               index=detector_names)
            
            for i, metric in enumerate(['TN', 'FP', 'FN', 'TP']):
                fig.add_trace(
                    go.Bar(
                        x=detector_names,
                        y=cm_df[metric],
                        name=metric,
                        marker_color=list(self.colors.values())[i]
                    ),
                    row=3, col=1
                )
        
        # 6. ROC curves (if available)
        if 'roc_curve' in results[detector_names[0]]:
            for i, det in enumerate(detector_names):
                roc_data = results[det]['roc_curve']
                fig.add_trace(
                    go.Scatter(
                        x=roc_data['fpr'],
                        y=roc_data['tpr'],
                        mode='lines',
                        name=f'{det} (AUC: {roc_data["auc"]:.3f})',
                        line=dict(color=list(self.colors.values())[i % len(self.colors)])
                    ),
                    row=3, col=2
                )
        
        # Update layout
        fig.update_layout(
            title_text="🛡️ Jailbreak Detection Results Dashboard",
            title_x=0.5,
            height=1200,
            showlegend=True,
            template="plotly_white"
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="False Positive Rate", row=1, col=1)
        fig.update_yaxes(title_text="Attack Success Rate", row=1, col=1)
        fig.update_xaxes(title_text="Recall", row=1, col=2)
        fig.update_yaxes(title_text="Precision", row=1, col=2)
        fig.update_xaxes(title_text="Detector", row=2, col=1)
        fig.update_yaxes(title_text="F1 Score", row=2, col=1)
        
        if save_path:
            fig.write_html(save_path)
            
        return fig
    
    def create_performance_timeline(self, results_history: List[Dict], 
                                  save_path: Optional[str] = None) -> go.Figure:
        """
        Create timeline visualization showing performance evolution
        
        Args:
            results_history: List of results dictionaries over time
            save_path: Optional path to save the plot
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Extract timeline data
        timestamps = [res['timestamp'] for res in results_history]
        detector_names = list(results_history[0]['results'].keys())
        
        for detector in detector_names:
            asr_timeline = [res['results'][detector]['asr'] for res in results_history]
            fpr_timeline = [res['results'][detector]['fpr'] for res in results_history]
            f1_timeline = [res['results'][detector]['f1'] for res in results_history]
            
            # ASR line
            fig.add_trace(go.Scatter(
                x=timestamps, y=asr_timeline,
                mode='lines+markers',
                name=f'{detector} ASR',
                line=dict(dash='solid'),
                yaxis='y1'
            ))
            
            # FPR line
            fig.add_trace(go.Scatter(
                x=timestamps, y=fpr_timeline,
                mode='lines+markers',
                name=f'{detector} FPR',
                line=dict(dash='dash'),
                yaxis='y1'
            ))
            
            # F1 line
            fig.add_trace(go.Scatter(
                x=timestamps, y=f1_timeline,
                mode='lines+markers',
                name=f'{detector} F1',
                line=dict(dash='dot'),
                yaxis='y2'
            ))
        
        # Update layout with dual y-axis
        fig.update_layout(
            title="Performance Evolution Over Time",
            xaxis_title="Time",
            yaxis=dict(title="ASR / FPR", side="left"),
            yaxis2=dict(title="F1 Score", side="right", overlaying="y"),
            hovermode='x unified',
            template="plotly_white"
        )
        
        if save_path:
            fig.write_html(save_path)
            
        return fig
    
    def create_attack_type_breakdown(self, results_by_attack: Dict, 
                                   save_path: Optional[str] = None) -> go.Figure:
        """
        Create breakdown visualization by attack type
        
        Args:
            results_by_attack: Results dictionary organized by attack type
            save_path: Optional path to save the plot
            
        Returns:
            Plotly figure object
        """
        attack_types = list(results_by_attack.keys())
        detector_names = list(results_by_attack[attack_types[0]].keys())
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['ASR by Attack Type', 'FPR by Attack Type', 
                          'Detection Rate Heatmap', 'Attack Success Distribution'],
            specs=[
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "heatmap"}, {"type": "pie"}]
            ]
        )
        
        # ASR by attack type
        for detector in detector_names:
            asr_vals = [results_by_attack[attack][detector]['asr'] for attack in attack_types]
            fig.add_trace(
                go.Bar(x=attack_types, y=asr_vals, name=f'{detector} ASR'),
                row=1, col=1
            )
        
        # FPR by attack type
        for detector in detector_names:
            fpr_vals = [results_by_attack[attack][detector]['fpr'] for attack in attack_types]
            fig.add_trace(
                go.Bar(x=attack_types, y=fpr_vals, name=f'{detector} FPR'),
                row=1, col=2
            )
        
        # Detection rate heatmap
        detection_matrix = []
        for attack in attack_types:
            detection_row = []
            for detector in detector_names:
                detection_rate = 1 - results_by_attack[attack][detector]['asr']
                detection_row.append(detection_rate)
            detection_matrix.append(detection_row)
        
        fig.add_trace(
            go.Heatmap(
                z=detection_matrix,
                x=detector_names,
                y=attack_types,
                colorscale='RdYlGn',
                name='Detection Rate'
            ),
            row=2, col=1
        )
        
        # Attack success distribution
        total_attacks = sum([results_by_attack[attack]['total_samples'] 
                           for attack in attack_types])
        attack_proportions = [results_by_attack[attack]['total_samples'] / total_attacks 
                            for attack in attack_types]
        
        fig.add_trace(
            go.Pie(
                labels=attack_types,
                values=attack_proportions,
                name="Attack Distribution"
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Attack Type Performance Analysis",
            height=800,
            showlegend=True,
            template="plotly_white"
        )
        
        if save_path:
            fig.write_html(save_path)
            
        return fig
    
    def save_all_plots(self, results: Dict, output_dir: str = "./plots"):
        """
        Generate and save all visualization types
        
        Args:
            results: Evaluation results dictionary
            output_dir: Directory to save plots
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Overview dashboard
        overview_fig = self.create_overview_dashboard(results)
        overview_fig.write_html(f"{output_dir}/overview_dashboard.html")
        
        print(f"✓ Plots saved to {output_dir}/")
        print("  - overview_dashboard.html: Comprehensive results overview")
        
        return output_dir
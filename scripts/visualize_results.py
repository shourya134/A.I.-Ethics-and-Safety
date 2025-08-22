#!/usr/bin/env python3
"""
Interactive results viewer for jailbreak detection evaluation
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.visualization import ResultsDashboard, MetricsVisualizer, ComparisonCharts
from src.utils.logging_utils import setup_logging

def load_results(results_file: str) -> dict:
    """Load evaluation results from JSON file"""
    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
        return results
    except Exception as e:
        print(f"Error loading results from {results_file}: {e}")
        return {}

def create_sample_results() -> dict:
    """Create sample results for demonstration"""
    return {
        "prompt_level": {
            "asr": 0.15,
            "fpr": 0.08,
            "precision": 0.89,
            "recall": 0.85,
            "f1": 0.87,
            "accuracy": 0.88,
            "confusion_matrix": [[450, 40], [75, 435]],
            "roc_curve": {
                "fpr": [0.0, 0.08, 0.15, 1.0],
                "tpr": [0.0, 0.85, 0.92, 1.0],
                "auc": 0.91
            }
        },
        "multi_turn": {
            "asr": 0.22,
            "fpr": 0.12,
            "precision": 0.82,
            "recall": 0.78,
            "f1": 0.80,
            "accuracy": 0.83,
            "confusion_matrix": [[440, 60], [110, 390]],
            "roc_curve": {
                "fpr": [0.0, 0.12, 0.25, 1.0],
                "tpr": [0.0, 0.78, 0.88, 1.0],
                "auc": 0.86
            }
        },
        "token_level": {
            "asr": 0.10,
            "fpr": 0.05,
            "precision": 0.93,
            "recall": 0.90,
            "f1": 0.91,
            "accuracy": 0.92,
            "confusion_matrix": [[475, 25], [50, 450]],
            "roc_curve": {
                "fpr": [0.0, 0.05, 0.10, 1.0],
                "tpr": [0.0, 0.90, 0.95, 1.0],
                "auc": 0.95
            }
        },
        "indirect_injection": {
            "asr": 0.18,
            "fpr": 0.10,
            "precision": 0.85,
            "recall": 0.82,
            "f1": 0.83,
            "accuracy": 0.86,
            "confusion_matrix": [[450, 50], [90, 410]],
            "roc_curve": {
                "fpr": [0.0, 0.10, 0.20, 1.0],
                "tpr": [0.0, 0.82, 0.90, 1.0],
                "auc": 0.89
            }
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Interactive results viewer for jailbreak detection")
    parser.add_argument("--results-file", "-r", 
                       help="Path to JSON results file")
    parser.add_argument("--output-dir", "-o", default="./plots",
                       help="Output directory for visualizations")
    parser.add_argument("--demo", action="store_true",
                       help="Run with sample demo data")
    parser.add_argument("--format", choices=['html', 'png', 'both'], default='html',
                       help="Output format for visualizations")
    parser.add_argument("--charts", nargs="+", 
                       choices=['dashboard', 'metrics', 'comparison', 'all'],
                       default=['all'],
                       help="Which chart types to generate")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    
    # Load results
    if args.demo or not args.results_file:
        print("🎯 Running with sample demo data...")
        results = create_sample_results()
    else:
        if not os.path.exists(args.results_file):
            print(f"❌ Results file not found: {args.results_file}")
            print("💡 Use --demo flag to run with sample data")
            return
        
        print(f"📊 Loading results from {args.results_file}...")
        results = load_results(args.results_file)
        
        if not results:
            print("❌ Failed to load results or results are empty")
            return
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎨 Creating visualizations...")
    print(f"📁 Output directory: {output_dir}")
    print(f"🔍 Detected {len(results)} detectors: {', '.join(results.keys())}")
    
    # Initialize visualizers
    dashboard = ResultsDashboard()
    metrics_viz = MetricsVisualizer()
    comparison_charts = ComparisonCharts()
    
    # Generate requested charts
    chart_types = args.charts
    if 'all' in chart_types:
        chart_types = ['dashboard', 'metrics', 'comparison']
    
    generated_files = []
    
    try:
        # 1. Dashboard
        if 'dashboard' in chart_types:
            print("📈 Generating dashboard...")
            dashboard_dir = output_dir / "dashboard"
            dashboard_dir.mkdir(exist_ok=True)
            
            # Overview dashboard
            fig_overview = dashboard.create_overview_dashboard(results)
            overview_file = dashboard_dir / "overview_dashboard.html"
            fig_overview.write_html(str(overview_file))
            generated_files.append(str(overview_file))
            
            print(f"  ✓ Overview dashboard: {overview_file}")
        
        # 2. Metrics visualizations
        if 'metrics' in chart_types:
            print("📊 Generating metrics plots...")
            metrics_dir = output_dir / "metrics"
            metrics_viz.save_all_metric_plots(results, str(metrics_dir))
            generated_files.extend([
                str(metrics_dir / "confusion_matrices.png"),
                str(metrics_dir / "performance_distribution.png"),
                str(metrics_dir / "performance_radar.png"),
                str(metrics_dir / "performance_summary.csv")
            ])
        
        # 3. Comparison charts
        if 'comparison' in chart_types:
            print("🔄 Generating comparison charts...")
            comparison_dir = output_dir / "comparisons"
            comparison_charts.save_all_comparison_charts(results, str(comparison_dir))
            generated_files.extend([
                str(comparison_dir / "detector_comparison_bar.html"),
                str(comparison_dir / "detector_comparison_radar.html"),
                str(comparison_dir / "detector_comparison_heatmap.html"),
                str(comparison_dir / "performance_ranking.html"),
                str(comparison_dir / "trade_off_analysis.html")
            ])
        
        # Create index HTML file
        create_index_html(output_dir, results, generated_files)
        
        print("\n🎉 Visualization complete!")
        print(f"📂 All files saved to: {output_dir}")
        print(f"🌐 Open {output_dir}/index.html in your browser to view results")
        
        # Print summary
        print("\n📋 Generated Files:")
        for file_path in generated_files:
            if os.path.exists(file_path):
                print(f"  ✓ {os.path.basename(file_path)}")
            else:
                print(f"  ❌ {os.path.basename(file_path)} (failed)")
    
    except Exception as e:
        print(f"❌ Error generating visualizations: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()

def create_index_html(output_dir: Path, results: dict, generated_files: list):
    """Create an index HTML file linking to all visualizations"""
    
    # Performance summary
    best_detector = max(results.keys(), key=lambda x: results[x].get('f1', 0))
    avg_f1 = sum(results[det].get('f1', 0) for det in results) / len(results)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛡️ Jailbreak Detection Results</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #eee;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .summary {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-left: 4px solid #007bff;
        }}
        .card h3 {{
            margin-top: 0;
            color: #007bff;
        }}
        .file-list {{
            list-style: none;
            padding: 0;
        }}
        .file-list li {{
            margin: 10px 0;
        }}
        .file-list a {{
            text-decoration: none;
            color: #007bff;
            padding: 8px 12px;
            background: #f8f9fa;
            border-radius: 4px;
            display: inline-block;
            transition: background-color 0.3s;
        }}
        .file-list a:hover {{
            background: #e9ecef;
        }}
        .metric {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            margin: 2px;
            font-size: 0.9em;
        }}
        .timestamp {{
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Jailbreak Detection Results</h1>
            <p class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <h2>📊 Performance Summary</h2>
            <p><strong>Best Performing Detector:</strong> {best_detector} 
               <span class="metric">F1: {results[best_detector].get('f1', 0):.3f}</span></p>
            <p><strong>Average F1 Score:</strong> <span class="metric">{avg_f1:.3f}</span></p>
            <p><strong>Detectors Evaluated:</strong> {len(results)} 
               ({', '.join(results.keys())})</p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>📈 Dashboard</h3>
                <p>Comprehensive overview with multiple metrics and visualizations</p>
                <ul class="file-list">
                    <li><a href="dashboard/overview_dashboard.html">📊 Overview Dashboard</a></li>
                </ul>
            </div>
            
            <div class="card">
                <h3>📏 Metrics Analysis</h3>
                <p>Detailed performance metrics and statistical analysis</p>
                <ul class="file-list">
                    <li><a href="metrics/confusion_matrices.png">🔢 Confusion Matrices</a></li>
                    <li><a href="metrics/performance_distribution.png">📉 Performance Distribution</a></li>
                    <li><a href="metrics/performance_radar.png">🎯 Radar Chart</a></li>
                    <li><a href="metrics/performance_summary.csv">📋 Summary Table (CSV)</a></li>
                </ul>
            </div>
            
            <div class="card">
                <h3>🔄 Comparisons</h3>
                <p>Side-by-side detector performance comparisons</p>
                <ul class="file-list">
                    <li><a href="comparisons/detector_comparison_bar.html">📊 Bar Chart Comparison</a></li>
                    <li><a href="comparisons/detector_comparison_radar.html">🎯 Radar Comparison</a></li>
                    <li><a href="comparisons/detector_comparison_heatmap.html">🔥 Heatmap Comparison</a></li>
                    <li><a href="comparisons/performance_ranking.html">🏆 Performance Ranking</a></li>
                    <li><a href="comparisons/trade_off_analysis.html">⚖️ Trade-off Analysis</a></li>
                </ul>
            </div>
        </div>
        
        <div class="card">
            <h3>ℹ️ About This Report</h3>
            <p>This report provides comprehensive analysis of jailbreak detection performance across multiple detectors and metrics. The visualizations help identify the best performing approaches and understand trade-offs between different detection strategies.</p>
            <p><strong>Key Metrics:</strong></p>
            <ul>
                <li><strong>ASR (Attack Success Rate):</strong> Lower is better</li>
                <li><strong>FPR (False Positive Rate):</strong> Lower is better</li>
                <li><strong>Precision, Recall, F1:</strong> Higher is better</li>
                <li><strong>Accuracy:</strong> Higher is better</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
    
    index_file = output_dir / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  ✓ Index page: {index_file}")

if __name__ == "__main__":
    main()
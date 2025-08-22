#!/usr/bin/env python3
"""
Simple visualization demo that shows what the outputs look like
"""

import json
import os
from datetime import datetime

def create_sample_html_dashboard():
    """Create a sample HTML dashboard to show the visualization structure"""
    
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛡️ Jailbreak Detection Results Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f7fa;
        }
        .header {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .dashboard-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .chart-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        .chart-title {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.2em;
            font-weight: 600;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .metric-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .summary-table {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
        }
        .grade-a { background-color: #d4edda; color: #155724; padding: 4px 8px; border-radius: 4px; }
        .grade-b { background-color: #fff3cd; color: #856404; padding: 4px 8px; border-radius: 4px; }
        .grade-c { background-color: #f8d7da; color: #721c24; padding: 4px 8px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ AI Safety Jailbreak Detection Results</h1>
        <p>Comprehensive Analysis Dashboard</p>
        <p style="font-size: 0.9em; opacity: 0.8;">Generated on ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">91.2%</div>
            <div class="metric-label">Best F1 Score</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">8.7%</div>
            <div class="metric-label">Lowest ASR</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">4</div>
            <div class="metric-label">Detectors Tested</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">87.5%</div>
            <div class="metric-label">Avg Accuracy</div>
        </div>
    </div>

    <div class="dashboard-container">
        <div class="chart-card">
            <div class="chart-title">📊 Performance Comparison</div>
            <div id="performance-chart" style="height: 400px;"></div>
        </div>
        
        <div class="chart-card">
            <div class="chart-title">🎯 Precision vs Recall</div>
            <div id="precision-recall-chart" style="height: 400px;"></div>
        </div>
        
        <div class="chart-card">
            <div class="chart-title">⚖️ ASR vs FPR Trade-off</div>
            <div id="tradeoff-chart" style="height: 400px;"></div>
        </div>
        
        <div class="chart-card">
            <div class="chart-title">🔥 Performance Heatmap</div>
            <div id="heatmap-chart" style="height: 400px;"></div>
        </div>
    </div>

    <div class="summary-table">
        <div class="chart-title">📋 Detector Performance Summary</div>
        <table>
            <thead>
                <tr>
                    <th>Detector</th>
                    <th>ASR ↓</th>
                    <th>FPR ↓</th>
                    <th>Precision ↑</th>
                    <th>Recall ↑</th>
                    <th>F1 Score ↑</th>
                    <th>Grade</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Token Level Detector</strong></td>
                    <td>0.087</td>
                    <td>0.052</td>
                    <td>0.932</td>
                    <td>0.901</td>
                    <td><strong>0.912</strong></td>
                    <td><span class="grade-a">A+ Excellent</span></td>
                </tr>
                <tr>
                    <td><strong>Prompt Level Detector</strong></td>
                    <td>0.145</td>
                    <td>0.078</td>
                    <td>0.891</td>
                    <td>0.854</td>
                    <td>0.874</td>
                    <td><span class="grade-a">A Very Good</span></td>
                </tr>
                <tr>
                    <td><strong>Indirect Injection Detector</strong></td>
                    <td>0.182</td>
                    <td>0.098</td>
                    <td>0.852</td>
                    <td>0.821</td>
                    <td>0.835</td>
                    <td><span class="grade-a">A Very Good</span></td>
                </tr>
                <tr>
                    <td><strong>Multi-turn Detector</strong></td>
                    <td>0.221</td>
                    <td>0.121</td>
                    <td>0.823</td>
                    <td>0.784</td>
                    <td>0.801</td>
                    <td><span class="grade-b">B Good</span></td>
                </tr>
            </tbody>
        </table>
    </div>

    <script>
        // Performance comparison bar chart
        var perfData = [{
            x: ['Token Level', 'Prompt Level', 'Indirect Injection', 'Multi-turn'],
            y: [0.912, 0.874, 0.835, 0.801],
            type: 'bar',
            marker: {color: '#667eea'},
            text: ['0.912', '0.874', '0.835', '0.801'],
            textposition: 'auto',
        }];
        
        var perfLayout = {
            title: '',
            xaxis: {title: 'Detector'},
            yaxis: {title: 'F1 Score', range: [0, 1]},
            font: {family: 'Segoe UI, sans-serif'},
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
        };
        
        Plotly.newPlot('performance-chart', perfData, perfLayout, {responsive: true});

        // Precision vs Recall scatter
        var prData = [{
            x: [0.901, 0.854, 0.821, 0.784],
            y: [0.932, 0.891, 0.852, 0.823],
            mode: 'markers+text',
            text: ['Token Level', 'Prompt Level', 'Indirect Injection', 'Multi-turn'],
            textposition: 'top center',
            marker: {size: 12, color: '#764ba2'},
            type: 'scatter'
        }];
        
        var prLayout = {
            title: '',
            xaxis: {title: 'Recall'},
            yaxis: {title: 'Precision'},
            font: {family: 'Segoe UI, sans-serif'},
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
        };
        
        Plotly.newPlot('precision-recall-chart', prData, prLayout, {responsive: true});

        // ASR vs FPR trade-off
        var tradeoffData = [{
            x: [0.052, 0.078, 0.098, 0.121],
            y: [0.087, 0.145, 0.182, 0.221],
            mode: 'markers+text',
            text: ['Token Level', 'Prompt Level', 'Indirect Injection', 'Multi-turn'],
            textposition: 'top center',
            marker: {size: 12, color: '#f39c12'},
            type: 'scatter'
        }];
        
        var tradeoffLayout = {
            title: '',
            xaxis: {title: 'False Positive Rate'},
            yaxis: {title: 'Attack Success Rate'},
            font: {family: 'Segoe UI, sans-serif'},
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
        };
        
        Plotly.newPlot('tradeoff-chart', tradeoffData, tradeoffLayout, {responsive: true});

        // Performance heatmap
        var heatmapData = [{
            z: [
                [0.087, 0.052, 0.932, 0.901, 0.912],
                [0.145, 0.078, 0.891, 0.854, 0.874],
                [0.182, 0.098, 0.852, 0.821, 0.835],
                [0.221, 0.121, 0.823, 0.784, 0.801]
            ],
            x: ['ASR', 'FPR', 'Precision', 'Recall', 'F1'],
            y: ['Token Level', 'Prompt Level', 'Indirect Injection', 'Multi-turn'],
            type: 'heatmap',
            colorscale: 'RdYlBu',
            reversescale: true
        }];
        
        var heatmapLayout = {
            title: '',
            font: {family: 'Segoe UI, sans-serif'},
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
        };
        
        Plotly.newPlot('heatmap-chart', heatmapData, heatmapLayout, {responsive: true});
    </script>
</body>
</html>
'''
    
    return html_content

def create_sample_results_json():
    """Create sample results JSON to show data structure"""
    
    sample_results = {
        "evaluation_metadata": {
            "timestamp": datetime.now().isoformat(),
            "dataset": "JailbreakBench + AdvBench",
            "total_samples": 1000,
            "evaluation_duration": "45.2 minutes"
        },
        "token_level_detector": {
            "asr": 0.087,
            "fpr": 0.052, 
            "precision": 0.932,
            "recall": 0.901,
            "f1": 0.912,
            "accuracy": 0.923,
            "latency": 120.3,
            "confusion_matrix": [[475, 25], [50, 450]],
            "roc_curve": {
                "fpr": [0.0, 0.01, 0.052, 0.10, 0.20, 1.0],
                "tpr": [0.0, 0.70, 0.901, 0.95, 0.98, 1.0],
                "auc": 0.954
            },
            "detected_patterns": ["gcg_suffix", "adversarial_tokens", "gradient_based"],
            "model_info": {
                "type": "transformer_based",
                "parameters": "350M",
                "training_data": "defensive_samples_v2"
            }
        },
        "prompt_level_detector": {
            "asr": 0.145,
            "fpr": 0.078,
            "precision": 0.891,
            "recall": 0.854,
            "f1": 0.874,
            "accuracy": 0.883,
            "latency": 45.2,
            "confusion_matrix": [[450, 40], [75, 435]],
            "roc_curve": {
                "fpr": [0.0, 0.02, 0.078, 0.15, 0.25, 1.0],
                "tpr": [0.0, 0.60, 0.854, 0.92, 0.96, 1.0],
                "auc": 0.918
            },
            "detected_patterns": ["roleplay", "obfuscation", "dan_style"],
            "model_info": {
                "type": "rule_based + ml",
                "rules": 45,
                "ml_model": "bert_classifier"
            }
        },
        "indirect_injection_detector": {
            "asr": 0.182,
            "fpr": 0.098,
            "precision": 0.852,
            "recall": 0.821,
            "f1": 0.835,
            "accuracy": 0.861,
            "latency": 32.1,
            "confusion_matrix": [[450, 50], [90, 410]],
            "roc_curve": {
                "fpr": [0.0, 0.03, 0.098, 0.20, 0.35, 1.0],
                "tpr": [0.0, 0.58, 0.821, 0.90, 0.95, 1.0],
                "auc": 0.892
            },
            "detected_patterns": ["hidden_instructions", "data_poisoning", "context_manipulation"],
            "model_info": {
                "type": "content_analysis",
                "detection_layers": ["semantic", "syntactic", "structural"]
            }
        },
        "multi_turn_detector": {
            "asr": 0.221,
            "fpr": 0.121,
            "precision": 0.823,
            "recall": 0.784,
            "f1": 0.801,
            "accuracy": 0.834,
            "latency": 78.5,
            "confusion_matrix": [[440, 60], [110, 390]],
            "roc_curve": {
                "fpr": [0.0, 0.05, 0.121, 0.25, 0.40, 1.0],
                "tpr": [0.0, 0.55, 0.784, 0.88, 0.94, 1.0],
                "auc": 0.867
            },
            "detected_patterns": ["crescendo", "many_shot", "conversation_manipulation"],
            "model_info": {
                "type": "conversation_analysis",
                "window_size": 10,
                "memory_model": "lstm_attention"
            }
        }
    }
    
    return sample_results

def main():
    """Generate sample visualization outputs"""
    
    # Create demo directory
    demo_dir = "demo_plots"
    os.makedirs(demo_dir, exist_ok=True)
    os.makedirs(f"{demo_dir}/dashboard", exist_ok=True)
    os.makedirs(f"{demo_dir}/data", exist_ok=True)
    
    print("Creating sample visualization outputs...")
    
    # 1. Create HTML dashboard
    html_content = create_sample_html_dashboard()
    with open(f"{demo_dir}/dashboard/overview_dashboard.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 2. Create sample results JSON
    results = create_sample_results_json()
    with open(f"{demo_dir}/data/sample_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    # 3. Create index page
    index_html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🛡️ Demo Visualization Output</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f5f7fa; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .demo-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #007bff; }}
        .file-link {{ display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; }}
        .file-link:hover {{ background: #0056b3; }}
        .features {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }}
        .feature {{ background: #e8f4fd; padding: 15px; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ AI Safety Jailbreak Detection</h1>
            <h2>Visualization Demo Output</h2>
            <p>This shows what the visualization system generates</p>
        </div>
        
        <div class="demo-card">
            <h3>📊 Interactive Dashboard</h3>
            <p>Comprehensive overview with multiple chart types, interactive features, and real-time data.</p>
            <a href="dashboard/overview_dashboard.html" class="file-link">🔗 View Dashboard</a>
        </div>
        
        <div class="demo-card">
            <h3>📄 Sample Data</h3>
            <p>Example of the JSON results structure that feeds into the visualizations.</p>
            <a href="data/sample_results.json" class="file-link">📋 View Data</a>
        </div>
        
        <div class="features">
            <div class="feature">
                <h4>📈 Performance Metrics</h4>
                <p>F1 scores, ASR, FPR, precision, recall with color-coded grades</p>
            </div>
            <div class="feature">
                <h4>🎯 Interactive Charts</h4>
                <p>Plotly-powered visualizations with hover effects and zoom</p>
            </div>
            <div class="feature">
                <h4>🔄 Detector Comparison</h4>
                <p>Side-by-side analysis of different detection approaches</p>
            </div>
            <div class="feature">
                <h4>⚖️ Trade-off Analysis</h4>
                <p>Understand performance relationships and optimization opportunities</p>
            </div>
        </div>
        
        <div class="demo-card">
            <h3>🚀 Full System Capabilities</h3>
            <p>When fully set up with dependencies, the system generates:</p>
            <ul>
                <li>📊 Interactive HTML dashboards</li>
                <li>📈 Static PNG plots for reports</li>
                <li>🎯 Radar charts and heatmaps</li>
                <li>📋 CSV summary tables</li>
                <li>🔄 Performance comparisons</li>
                <li>⏱️ Timeline visualizations</li>
                <li>🎨 Custom styling and themes</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #666;">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
'''
    
    with open(f"{demo_dir}/index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("Demo visualization created!")
    print(f"Output directory: {demo_dir}/")
    print("Open the following files to see the visualization:")
    print(f"  {demo_dir}/index.html - Overview page")
    print(f"  {demo_dir}/dashboard/overview_dashboard.html - Interactive dashboard")
    print(f"  {demo_dir}/data/sample_results.json - Sample data structure")
    
    return demo_dir

if __name__ == "__main__":
    main()
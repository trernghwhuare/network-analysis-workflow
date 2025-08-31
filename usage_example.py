#!/usr/bin/env python3
"""
Comprehensive usage example for the network_metrics_package.
"""

import sys
import os

# Add src to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import graph_tool.all as gt
from network_metrics_package.metrics.generator import compute_and_save_metrics
from network_metrics_package.plotting.compare_plots import (
    load_metrics, plot_violin, plot_box, plot_heatmap_corr, plot_clustermap
)

def analyze_network(graph_path, output_dir="analysis_output", prefix="network"):
    """
    Complete analysis workflow for a network.
    
    Parameters:
    graph_path (str): Path to the graph file (.gt, .graphml, etc.)
    output_dir (str): Directory to save output files
    prefix (str): Prefix for output files
    """
    print(f"Loading network from {graph_path}...")
    g = gt.load_graph(graph_path)
    print(f"Network loaded: {g.num_vertices()} vertices, {g.num_edges()} edges")
    
    # Compute metrics
    print("Computing network metrics...")
    metrics, npz_path, csv_path = compute_and_save_metrics(
        g, 
        out_dir=output_dir, 
        prefix=prefix,
        normalize=True,
        save_files=True
    )
    print(f"Metrics saved to {npz_path} and {csv_path}")
    
    # Load metrics for plotting (in case you want to do this separately)
    print("Loading metrics for visualization...")
    loaded_metrics = load_metrics(npz_path)
    
    # Generate plots
    print("Generating visualizations...")
    
    # Violin plot
    violin_file = os.path.join(output_dir, f"{prefix}_violin.png")
    plot_violin(loaded_metrics, out=violin_file)
    print(f"Violin plot saved to {violin_file}")
    
    # Box plot
    box_file = os.path.join(output_dir, f"{prefix}_box.png")
    plot_box(loaded_metrics, out=box_file)
    print(f"Box plot saved to {box_file}")
    
    # Correlation heatmap
    heatmap_file = os.path.join(output_dir, f"{prefix}_heatmap_corr.png")
    plot_heatmap_corr(loaded_metrics, out=heatmap_file)
    print(f"Correlation heatmap saved to {heatmap_file}")
    
    # Clustermap
    clustermap_file = os.path.join(output_dir, f"{prefix}_clustermap.png")
    plot_clustermap(loaded_metrics, out=clustermap_file)
    print(f"Clustermap saved to {clustermap_file}")
    
    print("Analysis complete!")
    return metrics

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python usage_example.py <graph_file> [output_dir] [prefix]")
        print("Example: python usage_example.py my_network.gt analysis_results my_analysis")
        sys.exit(1)
    
    graph_file = sys.argv[1]
    output_directory = sys.argv[2] if len(sys.argv) > 2 else "analysis_output"
    file_prefix = sys.argv[3] if len(sys.argv) > 3 else "network_analysis"
    
    # Run the analysis
    metrics = analyze_network(graph_file, output_directory, file_prefix)
    
    # Print summary statistics
    print("\nMetric Summary:")
    print("-" * 50)
    for metric_name, metric_values in metrics.items():
        print(f"{metric_name:20}: min={metric_values.min():.4f}, max={metric_values.max():.4f}, "
              f"mean={metric_values.mean():.4f}, std={metric_values.std():.4f}")
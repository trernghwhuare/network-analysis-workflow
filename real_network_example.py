#!/usr/bin/env python3
"""
Example of analyzing a real network with the network_metrics_package.
This example creates a network similar to what you might find in neuroscience research.
"""

import sys
import os

# Add src to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import graph_tool.all as gt
import numpy as np
from network_metrics_package.metrics.generator import compute_and_save_metrics
from network_metrics_package.plotting.compare_plots import (
    load_metrics, plot_violin, plot_box, plot_heatmap_corr, plot_clustermap
)

def create_sample_neural_network(n_neurons=1000, connection_prob=0.05):
    """
    Create a sample neural network similar to what might be found in neuroscience.
    
    Parameters:
    n_neurons (int): Number of neurons (vertices) in the network
    connection_prob (float): Probability of connection between any two neurons
    
    Returns:
    graph_tool.Graph: The generated network
    """
    print(f"Creating sample neural network with {n_neurons} neurons...")
    
    # Create graph
    g = gt.Graph()
    
    # Add vertices (neurons)
    g.add_vertex(n_neurons)
    
    # Add edges (synaptic connections) with a small-world-like structure
    np.random.seed(42)  # For reproducibility
    
    # First create a regular ring lattice for local connectivity
    for i in range(n_neurons):
        # Connect to nearby neurons (local connectivity)
        for j in range(1, 6):  # Connect to 5 nearest neighbors on each side
            if i + j < n_neurons:
                g.add_edge(i, i + j)
            if i - j >= 0:
                g.add_edge(i, i - j)
    
    # Add some random long-range connections (similar to brain networks)
    n_random_edges = int(n_neurons * connection_prob * 20)
    for _ in range(n_random_edges):
        source = np.random.randint(0, n_neurons)
        target = np.random.randint(0, n_neurons)
        if source != target:
            g.add_edge(source, target)
    
    print(f"Network created with {g.num_vertices()} vertices and {g.num_edges()} edges")
    return g

def analyze_neural_network(g, output_dir="neural_network_analysis", prefix="neural_net"):
    """
    Analyze a neural network using the network_metrics_package.
    
    Parameters:
    g (graph_tool.Graph): The network to analyze
    output_dir (str): Directory to save output files
    prefix (str): Prefix for output files
    """
    print("Starting neural network analysis...")
    
    # Compute metrics
    metrics, npz_path, csv_path = compute_and_save_metrics(
        g, 
        out_dir=output_dir, 
        prefix=prefix,
        normalize=True,
        save_files=True
    )
    print(f"Metrics saved to {npz_path} and {csv_path}")
    
    # Load metrics for plotting
    loaded_metrics = load_metrics(npz_path)
    
    # Generate plots
    print("Generating visualizations...")
    
    # Violin plot
    violin_file = os.path.join(output_dir, f"{prefix}_violin.png")
    plot_violin(loaded_metrics, out=violin_file)
    
    # Box plot
    box_file = os.path.join(output_dir, f"{prefix}_box.png")
    plot_box(loaded_metrics, out=box_file)
    
    # Correlation heatmap
    heatmap_file = os.path.join(output_dir, f"{prefix}_heatmap_corr.png")
    plot_heatmap_corr(loaded_metrics, out=heatmap_file)
    
    # Clustermap
    clustermap_file = os.path.join(output_dir, f"{prefix}_clustermap.png")
    plot_clustermap(loaded_metrics, out=clustermap_file)
    
    print("Analysis complete!")
    print("\nMetric Summary:")
    print("-" * 60)
    for metric_name, metric_values in metrics.items():
        print(f"{metric_name:20}: min={metric_values.min():.4f}, max={metric_values.max():.4f}, "
              f"mean={metric_values.mean():.4f}, std={metric_values.std():.4f}")
    
    return metrics

def main():
    """
    Main function to demonstrate analysis of a neural network.
    """
    # Create a sample neural network
    neural_network = create_sample_neural_network(n_neurons=500, connection_prob=0.03)
    
    # Save the network for future use
    neural_network.save("sample_neural_network.gt")
    print("Sample neural network saved as 'sample_neural_network.gt'")
    
    # Analyze the network
    metrics = analyze_neural_network(neural_network, "neural_analysis_output", "sample_neural")
    
    print("\nAnalysis files saved in 'neural_analysis_output' directory:")
    print("- sample_neural_metrics.npz (metrics in numpy format)")
    print("- sample_neural_metrics.csv (metrics in CSV format)")
    print("- sample_neural_violin.png (violin plot)")
    print("- sample_neural_box.png (box plot)")
    print("- sample_neural_heatmap_corr.png (correlation heatmap)")
    print("- sample_neural_clustermap.png (clustermap)")

if __name__ == "__main__":
    main()
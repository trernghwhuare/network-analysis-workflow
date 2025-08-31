#!/usr/bin/env python3
"""
Demo script showing how to use the network_metrics_package
"""

import os
import sys
import argparse

# Add the src directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from network_metrics_package import compute_and_save_metrics
from network_metrics_package.plotting import load_metrics, plot_violin, plot_box, plot_heatmap_corr, plot_clustermap
import graph_tool.all as gt

def main():
    parser = argparse.ArgumentParser(description="Demo of network metrics package")
    parser.add_argument("--graph", required=True, help="Path to graph-tool graph file (graphml/gt)")
    parser.add_argument("--out", default="plots", help="Output directory to save metric arrays and plots")
    parser.add_argument("--prefix", default="network", help="Prefix for output files")
    parser.add_argument("--no-normalize", dest="normalize", action="store_false", help="Disable min-max normalization")
    parser.add_argument("--threads", type=int, default=8, help="OpenMP threads for graph-tool")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.out, exist_ok=True)
    
    try:
        # Load graph
        G = gt.load_graph(args.graph)
        print(f"Loaded graph with {G.num_vertices()} vertices and {G.num_edges()} edges")
    except Exception as e:
        print(f"Failed to load graph {args.graph}: {e}")
        return
    
    # Compute and save metrics
    metrics, npz_path, csv_path = compute_and_save_metrics(
        G, 
        out_dir=args.out, 
        prefix=args.prefix, 
        normalize=args.normalize, 
        nthreads=args.threads, 
        save_files=True
    )
    
    print(f"Saved metrics to {npz_path} and {csv_path}")
    
    # Generate plots
    try:
        metrics = load_metrics(npz_path)
        base_name = os.path.splitext(os.path.basename(npz_path))[0]
        
        # Create plots directory
        plots_dir = os.path.join(args.out, "plots")
        os.makedirs(plots_dir, exist_ok=True)
        
        # Generate various plots
        plot_violin(metrics, out=os.path.join(plots_dir, f"{base_name}_violin.png"))
        print(f"Created violin plot: {base_name}_violin.png")
        
        plot_box(metrics, out=os.path.join(plots_dir, f"{base_name}_box.png"))
        print(f"Created box plot: {base_name}_box.png")
        
        plot_heatmap_corr(metrics, out=os.path.join(plots_dir, f"{base_name}_corr_heatmap.png"), annot=True)
        print(f"Created correlation heatmap: {base_name}_corr_heatmap.png")
        
        plot_clustermap(metrics, out=os.path.join(plots_dir, f"{base_name}_clustermap.png"))
        print(f"Created clustermap: {base_name}_clustermap.png")
        
        print(f"All plots saved to {plots_dir}")
        
    except Exception as e:
        print(f"Error generating plots: {e}")

if __name__ == "__main__":
    main()
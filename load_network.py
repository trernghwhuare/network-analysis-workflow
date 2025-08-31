#!/usr/bin/env python3
"""
Script to load various network formats for analysis with network_metrics_package.
"""

import sys
import os

# Add src to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import graph_tool.all as gt

def load_network_from_edgelist(filepath):
    """
    Load a network from an edge list file.
    
    Expected format:
    source1 target1
    source2 target2
    ...
    """
    g = gt.Graph()
    
    # Read edges from file
    edges = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                parts = line.strip().split()
                if len(parts) >= 2:
                    edges.append((int(parts[0]), int(parts[1])))
    
    # Add vertices (graph-tool will automatically create them when adding edges)
    for source, target in edges:
        g.add_edge(source, target)
    
    print(f"Loaded network with {g.num_vertices()} vertices and {g.num_edges()} edges")
    return g

def load_network_from_graphml(filepath):
    """
    Load a network from GraphML format.
    """
    g = gt.load_graph(filepath)
    print(f"Loaded network with {g.num_vertices()} vertices and {g.num_edges()} edges")
    return g

def load_network_from_gml(filepath):
    """
    Load a network from GML format.
    """
    g = gt.load_graph(filepath)
    print(f"Loaded network with {g.num_vertices()} vertices and {g.num_edges()} edges")
    return g

def create_network_from_adjacency_matrix(matrix_file):
    """
    Create a network from an adjacency matrix.
    
    Expected format: CSV or similar with rows as source nodes and columns as target nodes.
    """
    import numpy as np
    
    # Load matrix (assuming CSV format)
    matrix = np.loadtxt(matrix_file, delimiter=',')
    
    g = gt.Graph()
    g.add_vertex(len(matrix))
    
    # Add edges based on adjacency matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:  # Assuming non-zero values indicate edges
                g.add_edge(i, j)
    
    print(f"Created network with {g.num_vertices()} vertices and {g.num_edges()} edges")
    return g

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_network.py <network_file> [format]")
        print("Supported formats: edgelist, graphml, gml, adjacency")
        sys.exit(1)
    
    filepath = sys.argv[1]
    format_type = sys.argv[2] if len(sys.argv) > 2 else "edgelist"
    
    if format_type == "edgelist":
        g = load_network_from_edgelist(filepath)
    elif format_type == "graphml":
        g = load_network_from_graphml(filepath)
    elif format_type == "gml":
        g = load_network_from_gml(filepath)
    elif format_type == "adjacency":
        g = create_network_from_adjacency_matrix(filepath)
    else:
        print(f"Unsupported format: {format_type}")
        sys.exit(1)
    
    # Save in graph-tool format for future use
    output_file = filepath.rsplit('.', 1)[0] + ".gt"
    g.save(output_file)
    print(f"Network saved in graph-tool format: {output_file}")
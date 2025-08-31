#!/usr/bin/env python3
"""
Simple verification script to test that the network_metrics_package works correctly.
"""

import sys
import os

# Add src to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported correctly."""
    try:
        import graph_tool.all as gt
        print("✓ graph-tool imported successfully")
    except Exception as e:
        print(f"✗ Failed to import graph-tool: {e}")
        return False
    
    try:
        from network_metrics_package.metrics.generator import compute_and_save_metrics
        print("✓ compute_and_save_metrics imported successfully")
    except Exception as e:
        print(f"✗ Failed to import compute_and_save_metrics: {e}")
        return False
    
    try:
        from network_metrics_package.plotting.compare_plots import plot_violin, plot_box
        print("✓ Plotting functions imported successfully")
    except Exception as e:
        print(f"✗ Failed to import plotting functions: {e}")
        return False
    
    return True

def test_network_creation():
    """Test creating a simple network."""
    try:
        import graph_tool.all as gt
        g = gt.Graph()
        g.add_vertex(10)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        print(f"✓ Created test network with {g.num_vertices()} vertices and {g.num_edges()} edges")
        return g
    except Exception as e:
        print(f"✗ Failed to create test network: {e}")
        return None

def test_metrics_computation():
    """Test computing metrics on a simple network."""
    try:
        import graph_tool.all as gt
        from network_metrics_package.metrics.generator import compute_and_save_metrics
        
        # Create a simple test network
        g = gt.Graph()
        g.add_vertex(10)
        for i in range(9):
            g.add_edge(i, i+1)
        
        # Compute metrics
        metrics, npz_path, csv_path = compute_and_save_metrics(
            g, 
            out_dir="test_output", 
            prefix="test",
            normalize=True,
            save_files=True
        )
        
        print(f"✓ Computed metrics for test network")
        print(f"  Metrics keys: {list(metrics.keys())}")
        print(f"  Saved to: {npz_path} and {csv_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to compute metrics: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main verification function."""
    print("Verifying network_metrics_package installation...")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n✗ Import tests failed")
        return 1
    
    print()
    
    # Test network creation
    g = test_network_creation()
    if g is None:
        print("\n✗ Network creation test failed")
        return 1
    
    print()
    
    # Test metrics computation
    if not test_metrics_computation():
        print("\n✗ Metrics computation test failed")
        return 1
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! The package is working correctly.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
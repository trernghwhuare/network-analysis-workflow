#!/usr/bin/env python3
"""
Script to check if your network files exist and show basic information.
"""

import sys
import os

# Add src to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import graph_tool.all as gt
    print("✓ graph-tool successfully imported")
except ImportError as e:
    print(f"✗ Failed to import graph-tool: {e}")
    sys.exit(1)

# List of your network files
network_files = [
    "iT_max_plus.gt",
    "max_CTC_plus.gt", 
    "max_M2M1S1_plus.gt",
    "optimus_CTC_plus.gt",
    "optimus_M2M1S1_plus.gt"
]

def check_network_file(filepath):
    """
    Check if a network file exists and show basic information.
    """
    if not os.path.exists(filepath):
        print(f"✗ {filepath} not found")
        return False
    
    try:
        # Load the network
        g = gt.load_graph(filepath)
        print(f"✓ {filepath}: {g.num_vertices()} vertices, {g.num_edges()} edges")
        return True
    except Exception as e:
        print(f"✗ Error loading {filepath}: {e}")
        return False

def main():
    """
    Main function to check all network files.
    """
    print("Checking your network files...")
    print("=" * 40)
    
    # Counter for successful checks
    success_count = 0
    
    # Check each network file
    for network_file in network_files:
        if check_network_file(network_file):
            success_count += 1
    
    print("\n" + "=" * 40)
    print(f"Check complete! {success_count} out of {len(network_files)} files are accessible.")

if __name__ == "__main__":
    main()
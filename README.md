# Network Metrics Analysis Package

## Overview
The Network Metrics Analysis Package is designed to generate graph centrality metrics and create visualizations for neural network structure analysis. It provides a modular structure for metric generation, utility functions, and visualization of metric comparisons.

## Features
- Compute various graph centrality metrics using graph-tool
- Save metrics in both .npz and .csv formats
- Generate visualizations (violin plots, box plots, heatmaps, clustermaps)
- Analyze structural characteristics of neural networks

## Installation

### Prerequisites
- Python 3.8 or higher
- graph-tool library (see installation instructions below)

### Installing graph-tool
Since graph-tool is not available via pip, you need to install it separately:

#### Ubuntu/Debian:
```bash
sudo apt-get install python3-graph-tool
```

#### Conda:
```bash
conda install -c conda-forge graph-tool
```

#### Other systems:
See the official installation guide: https://graph-tool.skewed.de/

### Install from source
```bash
# Make sure graph-tool is installed first
python -c "import graph_tool.all as gt; print('graph-tool successfully imported')"

# Then install the package
cd network_metrics_package
pip install -e .
```

## Usage

### Command Line Interface
```bash
# Compute metrics for a graph
analyze-network-metrics --graph path/to/graph.gt --out output_directory --prefix network_name

# Additional options
analyze-network-metrics --graph path/to/graph.gt --out output_directory --prefix network_name --no-normalize --threads 4
```

### Python API
```python
import graph_tool.all as gt
from network_metrics_package.metrics.generator import compute_and_save_metrics
from network_metrics_package.plotting.compare_plots import load_metrics, plot_violin, plot_box, plot_heatmap_corr, plot_clustermap

# Load a graph
G = gt.load_graph("path/to/graph.gt")

# Compute and save metrics
metrics, npz_path, csv_path = compute_and_save_metrics(G, out_dir="output_directory", prefix="network_name")

# Load metrics for plotting
metrics = load_metrics(npz_path)

# Generate plots
plot_violin(metrics, out="violin_plot.png")
plot_box(metrics, out="box_plot.png")
plot_heatmap_corr(metrics, out="correlation_heatmap.png")
plot_clustermap(metrics, out="clustermap.png")
```

### Working with Different Network Formats

If your network is not already in graph-tool format (.gt), you can convert it:

```bash
# For edge list format
python load_network.py network.edgelist edgelist

# For GraphML format
python load_network.py network.graphml graphml

# For GML format
python load_network.py network.gml gml
```

### Complete Analysis Workflow

For a complete analysis with all visualizations:

```bash
python usage_example.py path/to/graph.gt output_directory network_name
```

This will:
1. Load your network
2. Compute all metrics
3. Save metrics in .npz and .csv formats
4. Generate all visualizations
5. Print summary statistics

## Working with Real Networks

### Supported Formats
The package works with networks in the following formats:
- Graph-tool (.gt) - Native format, most efficient
- GraphML (.graphml) - Standard XML-based format
- GML (.gml) - Graph Modeling Language
- Edge lists (.edges, .txt) - Simple text format
- Adjacency matrices (.csv) - Matrix representation

### Converting Your Network
If your network is in a different format, you can use the provided conversion scripts:

```bash
# Convert edge list to graph-tool format
python load_network.py my_network.edgelist edgelist

# Convert GraphML to graph-tool format
python load_network.py my_network.graphml graphml
```

### Analysis Output
The analysis produces:
1. Metrics in .npz format (for programmatic access)
2. Metrics in .csv format (for easy viewing)
3. Visualizations:
   - Violin plots showing metric distributions
   - Box plots showing metric quartiles
   - Correlation heatmaps showing metric relationships
   - Clustermaps showing metric groupings

## Package Structure
```
network_metrics_package
├── src
│   └── network_metrics_package
│       ├── __init__.py
│       ├── main.py                  # CLI entrypoint
│       ├── metrics
│       │   ├── __init__.py
│       │   ├── generator.py         # Generates metric values and aligned arrays
│       │   └── utils.py             # Helper functions for metrics and alignment
│       └── plotting
│           ├── __init__.py
│           └── compare_plots.py     # Plotting functions for metric comparison visualizations
├── tests
│   ├── test_generator.py            # Unit tests for metric generation
│   └── test_plotting.py             # Unit tests for plotting functions
├── requirements.txt                 # Project dependencies
├── pyproject.toml                   # Project configuration
├── setup.py                         # Setup script
├── .gitignore                       # Files to ignore in version control
└── README.md                        # Project documentation
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
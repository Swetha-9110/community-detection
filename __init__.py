"""Community detection on undirected graphs: Louvain and label propagation."""
from .graph import Graph
from .louvain import louvain
from .label_propagation import label_propagation
from .metrics import modularity, nmi, communities_to_labels

__all__ = ["Graph", "louvain", "label_propagation", "modularity", "nmi", "communities_to_labels"]
__version__ = "1.0.0"

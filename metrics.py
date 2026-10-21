"""Quality metrics: modularity Q (with resolution gamma) and normalized mutual information."""
from __future__ import annotations

import math
from collections import Counter
from typing import Hashable, Sequence

from .graph import Graph


def communities_to_labels(groups: Sequence[Sequence[Hashable]], graph: Graph) -> list[int]:
    """Convert a list of node-label groups into a per-node-index community vector."""
    out = [-1] * graph.n
    for cid, group in enumerate(groups):
        for node in group:
            out[graph.index[node]] = cid
    return out


def modularity(graph: Graph, comm: Sequence[int], gamma: float = 1.0) -> float:
    m2 = 2 * len(graph.edges)
    if m2 == 0:
        return 0.0
    deg = [0] * graph.n
    internal: Counter = Counter()
    for u, v in graph.edges:
        deg[u] += 1
        deg[v] += 1
        if comm[u] == comm[v]:
            internal[comm[u]] += 2
    total: Counter = Counter()
    for i in range(graph.n):
        total[comm[i]] += deg[i]
    return sum(internal[c] / m2 - gamma * (t / m2) ** 2 for c, t in total.items())


def nmi(a: Sequence[int], b: Sequence[int]) -> float:
    """Normalized mutual information with arithmetic-mean normalization (same as sklearn default)."""
    if len(a) != len(b):
        raise ValueError("label vectors must have equal length")
    n = len(a)
    if n == 0:
        return 1.0
    ca, cb = Counter(a), Counter(b)
    joint = Counter(zip(a, b))
    mi = 0.0
    for (x, y), nxy in joint.items():
        mi += (nxy / n) * math.log((nxy * n) / (ca[x] * cb[y]))
    ha = -sum((c / n) * math.log(c / n) for c in ca.values())
    hb = -sum((c / n) * math.log(c / n) for c in cb.values())
    if ha == 0 and hb == 0:
        return 1.0
    denom = (ha + hb) / 2
    return mi / denom if denom > 0 else 0.0

"""Louvain modularity optimization (Blondel et al., 2008) with a resolution parameter gamma.

Phase 1 moves each node to the neighbouring community with the largest modularity gain.
Phase 2 aggregates communities into super-nodes. The two phases repeat until no move improves Q.
"""
from __future__ import annotations

from collections import defaultdict

from .graph import Graph


def louvain(graph: Graph, gamma: float = 1.0) -> list[int]:
    """Return a community id (0..k-1) for each node index of ``graph``."""
    n = graph.n
    m2 = 2 * len(graph.edges)
    if m2 == 0:
        return list(range(n))

    adj: list[dict[int, float]] = [defaultdict(float) for _ in range(n)]
    for u, v in graph.edges:
        adj[u][v] += 1.0
        adj[v][u] += 1.0

    members = list(range(n))  # original node -> current super-node
    while True:
        m = len(adj)
        k = [sum(adj[i].values()) for i in range(m)]
        comm = list(range(m))
        tot = list(k)
        moved_any = False
        improved = True
        passes = 0
        while improved and passes < 100:
            improved = False
            passes += 1
            for i in range(m):
                ci = comm[i]
                w_to: dict[int, float] = defaultdict(float)
                for j, w in adj[i].items():
                    if j != i:
                        w_to[comm[j]] += w
                tot[ci] -= k[i]
                best, best_gain = ci, w_to.get(ci, 0.0) - gamma * tot[ci] * k[i] / m2
                for c, w in w_to.items():
                    gain = w - gamma * tot[c] * k[i] / m2
                    if gain > best_gain + 1e-12:
                        best, best_gain = c, gain
                tot[best] += k[i]
                if best != ci:
                    comm[i] = best
                    improved = True
                    moved_any = True
        if not moved_any:
            break

        relabel: dict[int, int] = {}
        for c in comm:
            if c not in relabel:
                relabel[c] = len(relabel)
        new_id = [relabel[c] for c in comm]
        members = [new_id[s] for s in members]
        n_new = len(relabel)
        if n_new == m:
            break

        new_adj: list[dict[int, float]] = [defaultdict(float) for _ in range(n_new)]
        for i in range(m):
            a = new_id[i]
            for j, w in adj[i].items():
                new_adj[a][new_id[j]] += w
        adj = new_adj

    # Compact labels to 0..k-1 in order of first appearance.
    relabel: dict[int, int] = {}
    return [relabel.setdefault(c, len(relabel)) for c in members]

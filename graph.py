"""Undirected, unweighted graph with integer node indices and original labels."""
from __future__ import annotations

from typing import Hashable, Iterable


class Graph:
    def __init__(self, edges: Iterable[tuple[Hashable, Hashable]] = ()):
        self.labels: list[Hashable] = []
        self.index: dict[Hashable, int] = {}
        self.edges: list[tuple[int, int]] = []
        seen: set[tuple[int, int]] = set()
        for u, v in edges:
            if u == v:
                continue  # self-loops are ignored
            for x in (u, v):
                if x not in self.index:
                    self.index[x] = len(self.labels)
                    self.labels.append(x)
            a, b = self.index[u], self.index[v]
            key = (a, b) if a < b else (b, a)
            if key in seen:
                continue  # collapse duplicate and reversed edges
            seen.add(key)
            self.edges.append(key)
        self.n = len(self.labels)

    @classmethod
    def from_edge_list(cls, path: str) -> "Graph":
        """Read a whitespace/comma/tab separated edge list. Lines starting with # or % are comments."""
        def pairs():
            with open(path, encoding="utf-8") as f:
                for line in f:
                    s = line.strip()
                    if not s or s[0] in "#%":
                        continue
                    parts = s.replace(",", " ").replace("\t", " ").split()
                    if len(parts) >= 2:
                        yield parts[0], parts[1]
        return cls(pairs())

    @classmethod
    def from_networkx(cls, G) -> "Graph":
        return cls(G.edges())

    def adjacency(self) -> list[list[int]]:
        adj: list[list[int]] = [[] for _ in range(self.n)]
        for u, v in self.edges:
            adj[u].append(v)
            adj[v].append(u)
        return adj

    def __repr__(self) -> str:
        return f"Graph(nodes={self.n}, edges={len(self.edges)})"

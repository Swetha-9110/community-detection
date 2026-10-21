"""Asynchronous label propagation (Raghavan et al., 2007). Fast, non-deterministic baseline."""
from __future__ import annotations

import random
from collections import Counter

from .graph import Graph


def label_propagation(graph: Graph, max_iter: int = 100, seed: int | None = 0) -> list[int]:
    rng = random.Random(seed)
    adj = graph.adjacency()
    labels = list(range(graph.n))
    order = list(range(graph.n))
    for _ in range(max_iter):
        rng.shuffle(order)
        changed = False
        for i in order:
            if not adj[i]:
                continue
            counts = Counter(labels[j] for j in adj[i])
            top = max(counts.values())
            candidates = [lab for lab, c in counts.items() if c == top]
            if labels[i] in candidates:
                continue  # keep current label when it is already among the best
            labels[i] = rng.choice(candidates)
            changed = True
        if not changed:
            break
    relabel: dict[int, int] = {}
    return [relabel.setdefault(lab, len(relabel)) for lab in labels]

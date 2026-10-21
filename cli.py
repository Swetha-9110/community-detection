"""Command-line interface.

    python -m community.cli detect data/karate.edges --algorithm louvain --gamma 1.0 --out results/karate.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
import time

from .graph import Graph
from .label_propagation import label_propagation
from .louvain import louvain
from .metrics import modularity


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="community", description="Detect communities in an edge list.")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("detect", help="run community detection on an edge list")
    d.add_argument("edge_file")
    d.add_argument("--algorithm", choices=["louvain", "lpa"], default="louvain")
    d.add_argument("--gamma", type=float, default=1.0, help="resolution parameter (Louvain only)")
    d.add_argument("--seed", type=int, default=0, help="seed for label propagation")
    d.add_argument("--out", help="CSV path for node,community assignments")
    args = p.parse_args(argv)

    graph = Graph.from_edge_list(args.edge_file)
    t0 = time.perf_counter()
    if args.algorithm == "louvain":
        comm = louvain(graph, gamma=args.gamma)
    else:
        comm = label_propagation(graph, seed=args.seed)
    elapsed = time.perf_counter() - t0
    q = modularity(graph, comm, gamma=args.gamma)
    k = len(set(comm))

    print(f"{graph}  algorithm={args.algorithm}  communities={k}  modularity={q:.4f}  time={elapsed:.3f}s")
    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["node", "community"])
            for lab, c in zip(graph.labels, comm):
                w.writerow([lab, c])
        print(f"assignments written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

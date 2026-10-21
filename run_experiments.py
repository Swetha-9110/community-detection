"""Reproduce the experiments: run Louvain (several gammas) and label propagation on each dataset.

    python scripts/run_experiments.py [extra_edge_file ...]

Writes results/summary.csv and results/karate_louvain.png. Extra edge files are analysed
without ground truth (NMI is left blank).
"""
from __future__ import annotations

import csv
import os
import random
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from community import Graph, label_propagation, louvain, modularity, nmi  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
RESULTS = os.path.join(ROOT, "results")
GAMMAS = [0.5, 1.0, 1.5, 2.0]


def planted_partition(k=4, size=50, p_in=0.25, p_out=0.01, seed=7):
    rnd = random.Random(seed)
    n = k * size
    truth = [i // size for i in range(n)]
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            p = p_in if truth[i] == truth[j] else p_out
            if rnd.random() < p:
                edges.append((i, j))
    return Graph(edges), truth


def run_one(name, graph, truth, rows):
    for algo, fn in [("louvain", None), ("lpa", None)]:
        gammas = GAMMAS if algo == "louvain" else [None]
        for gamma in gammas:
            t0 = time.perf_counter()
            if algo == "louvain":
                comm = louvain(graph, gamma=gamma)
                q = modularity(graph, comm, gamma=gamma)
            else:
                comm = label_propagation(graph, seed=0)
                q = modularity(graph, comm)
            elapsed = time.perf_counter() - t0
            score = nmi(comm, truth) if truth is not None else ""
            rows.append({
                "dataset": name, "nodes": graph.n, "edges": len(graph.edges),
                "algorithm": algo, "gamma": "" if gamma is None else gamma,
                "communities": len(set(comm)), "modularity": round(q, 4),
                "nmi": "" if score == "" else round(score, 4),
                "seconds": round(elapsed, 4),
            })
            print(f"{name:<22} {algo:<8} gamma={gamma}  k={len(set(comm)):<3} Q={q:.4f}"
                  f"  NMI={score if score == '' else round(score, 3)}  {elapsed:.3f}s")


def plot_karate(graph, comm, path):
    G = nx.karate_club_graph()
    pos = nx.spring_layout(G, seed=4)
    colors = [f"C{comm[graph.index[n]] % 10}" for n in G.nodes()]
    fig, ax = plt.subplots(figsize=(6, 5))
    nx.draw_networkx(G, pos=pos, node_color=colors, with_labels=True, font_size=7,
                     edge_color="#999999", node_size=280, ax=ax)
    ax.set_title("Zachary karate club: Louvain communities (gamma = 1.0)")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main(extra_files):
    os.makedirs(RESULTS, exist_ok=True)
    rows = []

    karate = Graph.from_networkx(nx.karate_club_graph())
    club = nx.get_node_attributes(nx.karate_club_graph(), "club")
    truth_k = [1 if club[lab] == "Mr. Hi" else 0 for lab in karate.labels]
    run_one("karate", karate, truth_k, rows)
    plot_karate(karate, louvain(karate, gamma=1.0), os.path.join(RESULTS, "karate_louvain.png"))

    pp, truth_raw = planted_partition()
    # Graph indices follow first appearance in the edge list, so map truth through labels.
    truth_pp = [truth_raw[lab] for lab in pp.labels]
    run_one("planted_4x50", pp, truth_pp, rows)

    for path in extra_files:
        g = Graph.from_edge_list(path)
        run_one(os.path.basename(path), g, None, rows)

    out = os.path.join(RESULTS, "summary.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main(sys.argv[1:])

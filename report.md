# Community Detection: Team Project #1 Report

## 1. Problem

Given an undirected network, partition its nodes into communities: groups that are densely connected internally and sparsely connected to the rest. We compare a modularity-based method (Louvain) with a fast label-based baseline (label propagation) on networks with and without ground truth.

## 2. Methods

**Louvain.** Each node starts in its own community. Nodes move to the neighbouring community that maximises the modularity gain. Communities are then aggregated into super-nodes and the process repeats until no move improves Q. A resolution parameter gamma scales the null-model penalty, so higher gamma yields more, smaller communities.

**Label propagation.** Each node adopts the label held by the largest number of its neighbours, with random tie-breaking, until labels stabilise.

## 3. Metrics

- **Modularity Q** = sum over communities of [ (intra-edges / m) - gamma * (degree sum / 2m)^2 ].
- **NMI** compares a predicted partition with ground truth; 1 means identical partitions.

## 4. Datasets

- **Karate club** (Zachary, 1977): 34 nodes, 78 edges, two known factions.
- **Planted partition**: 200 nodes in 4 blocks of 50, p_in = 0.25, p_out = 0.01 (synthetic, seed 7).
- SNAP datasets can be added through `scripts/run_experiments.py`. They were not included in the reported run.

## 5. Results

Modularity Q is gamma-scaled (Q_gamma) for Louvain rows and standard for label propagation (gamma = 1).

| Dataset | Method | Communities | Modularity Q | NMI | Time (s) |
|---|---|---:|---:|---:|---:|
| karate | louvain (γ=0.5) | 2 | 0.6218 | 0.6772 | 0.000 |
| karate | louvain (γ=1.0) | 4 | 0.4156 | 0.4977 | 0.000 |
| karate | louvain (γ=1.5) | 4 | 0.2643 | 0.5878 | 0.000 |
| karate | louvain (γ=2.0) | 7 | 0.1645 | 0.4436 | 0.000 |
| karate | lpa | 4 | 0.3813 | 0.5369 | 0.000 |
| planted_4x50 | louvain (γ=0.5) | 4 | 0.7646 | 1.0 | 0.005 |
| planted_4x50 | louvain (γ=1.0) | 4 | 0.6395 | 1.0 | 0.005 |
| planted_4x50 | louvain (γ=1.5) | 4 | 0.5143 | 1.0 | 0.004 |
| planted_4x50 | louvain (γ=2.0) | 4 | 0.3892 | 1.0 | 0.005 |
| planted_4x50 | lpa | 4 | 0.6395 | 1.0 | 0.002 |

Figure: `results/karate_louvain.png` shows the Louvain communities (gamma = 1) on the karate club.

## 6. Discussion

Modularity values in the table are gamma-scaled (Q_gamma), so they are only directly comparable within the same gamma. Across gamma values, compare partitions by NMI or by the standard Q at gamma = 1.

- **Planted partition.** Louvain and label propagation both recover the four blocks exactly (NMI = 1.0) for every tested gamma from 0.5 to 2.0. The planted structure is strong enough that resolution does not change the answer.
- **Karate club.** At gamma = 1 (standard modularity), Louvain finds four communities with Q = 0.4156, close to values reported in the literature. Its NMI against the two known factions is 0.50. Gamma = 0.5 merges the graph into two communities with NMI 0.68, a closer match to the real split, but that partition has a different objective, so its Q is not comparable. Gamma = 2.0 fragments the graph into seven communities and lowers NMI. A higher modularity score does not guarantee a closer match to a known split.
- **Label propagation.** On karate it reaches Q = 0.38 at gamma = 1 with NMI 0.54, close to Louvain on the same measures. It is much faster to reason about and is non-deterministic, so the seed is fixed. With one seed and two small graphs, this is not enough evidence to rank the two methods in general.

## 7. Limitations and future work

- Louvain is greedy and can return different local optima for different node orders. Only one ordering is used here.
- Modularity has a resolution limit. Very small communities may merge in large graphs; the gamma sweep is one way to inspect this.
- The front end runs Louvain in the browser and draws graphs up to 1,200 nodes. Larger graphs use the CLI.

## 8. Reproducibility

`python scripts/run_experiments.py` regenerates `results/summary.csv` and the figure. Label propagation uses a fixed seed. Tests: `python -m pytest -q`.

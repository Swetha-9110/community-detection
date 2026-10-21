# Community Detection (CSE4039 Team Project #1)

Community detection on undirected networks with a from-scratch Louvain implementation,
a label propagation baseline, quality metrics, experiments, tests, a CLI, and a browser front end.

## Layout

```
community/              core package
  graph.py              Graph class, edge-list loader (SNAP / comma / tab / space)
  louvain.py            Louvain modularity optimisation with resolution gamma
  label_propagation.py  asynchronous label propagation baseline
  metrics.py            modularity Q (gamma-scaled) and NMI
  cli.py                command-line entry point
scripts/run_experiments.py   reproduces results/summary.csv and the figure
tests/                  pytest suite (12 tests)
data/                   karate club edge list and ground-truth factions
frontend/index.html     single-file interactive front end (open in a browser)
results/                summary.csv, karate_louvain.png, assignments
report/report.md        write-up
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Run tests
python -m pytest -q

# Detect communities in an edge list
python -m community detect data/karate.edges --algorithm louvain --gamma 1.0 --out results/karate.csv
python -m community detect path/to/edges.txt --algorithm lpa --seed 0

# Reproduce experiments (add downloaded SNAP files as extra arguments)
python scripts/run_experiments.py path/to/com-dblp.ungraph.txt

# Front end: open frontend/index.html in a browser, then upload an edge list
```

## Datasets

The experiments use the Zachary karate club (34 nodes, 78 edges, ground-truth factions) and a
generated planted-partition graph (4 blocks of 50 nodes, p_in = 0.25, p_out = 0.01, seed 7).
Stanford SNAP datasets (for example `com-amazon.ungraph.txt` or `email-Eu-core.txt`) can be added by
passing their paths to `scripts/run_experiments.py`. SNAP files contain `#` comment lines, which the
loader skips. Their community ground truth files (`*.all.cmty.txt`) can be used for NMI if needed.

## Method summary

- **Louvain**: greedy local moves that maximise the modularity gain, then aggregation of communities
  into super-nodes. The resolution parameter gamma scales the null-model term. gamma = 1 is standard modularity.
- **Label propagation**: each node repeatedly adopts the most common label among its neighbours.
  It is fast but non-deterministic, so a seed is fixed for reproducibility.
- **Modularity Q**: fraction of intra-community edges minus the expected fraction under a configuration null model.
- **NMI**: normalized mutual information against ground truth, with arithmetic-mean normalization.

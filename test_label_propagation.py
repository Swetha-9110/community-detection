from community import Graph, label_propagation


def test_two_cliques_separated():
    edges = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    edges += [(i, j) for i in range(6, 12) for j in range(i + 1, 12)]
    edges.append((0, 6))
    g = Graph(edges)
    comm = label_propagation(g, seed=1)
    assert len({comm[i] for i in range(6)}) == 1
    assert len({comm[i] for i in range(6, 12)}) == 1
    assert comm[0] != comm[6]


def test_seed_reproducible():
    import networkx as nx
    g = Graph.from_networkx(nx.karate_club_graph())
    assert label_propagation(g, seed=3) == label_propagation(g, seed=3)

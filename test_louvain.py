import networkx as nx

from community import Graph, louvain, modularity


def test_two_cliques_split():
    edges = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    edges += [(i, j) for i in range(5, 10) for j in range(i + 1, 10)]
    edges.append((4, 5))
    g = Graph(edges)
    comm = louvain(g)
    assert len(set(comm)) == 2
    assert len({comm[i] for i in range(5)}) == 1
    assert len({comm[i] for i in range(5, 10)}) == 1


def test_karate_club_modularity():
    g = Graph.from_networkx(nx.karate_club_graph())
    comm = louvain(g)
    # Louvain on Zachary's karate club reaches Q ~= 0.42 in the literature.
    assert modularity(g, comm) > 0.38


def test_no_edges_returns_singletons():
    g = Graph([])
    assert louvain(g) == []
    g2 = Graph([("a", "a")])
    assert louvain(g2) == []


def test_higher_gamma_gives_more_communities():
    g = Graph.from_networkx(nx.karate_club_graph())
    low = len(set(louvain(g, gamma=0.5)))
    high = len(set(louvain(g, gamma=2.0)))
    assert high >= low

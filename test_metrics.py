import math

from community import Graph, modularity, nmi, communities_to_labels


def test_nmi_identical_and_permuted():
    assert math.isclose(nmi([0, 0, 1, 1], [0, 0, 1, 1]), 1.0)
    assert math.isclose(nmi([0, 0, 1, 1], [5, 5, 9, 9]), 1.0)


def test_nmi_independent_is_low():
    a = [0, 1, 0, 1, 0, 1, 0, 1]
    b = [0, 0, 1, 1, 0, 0, 1, 1]
    assert nmi(a, b) < 0.1


def test_modularity_single_community_is_zero():
    g = Graph([(0, 1), (1, 2), (2, 0)])
    assert abs(modularity(g, [0, 0, 0])) < 1e-12


def test_communities_to_labels_roundtrip():
    g = Graph([("x", "y"), ("y", "z")])
    assert communities_to_labels([["x", "y"], ["z"]], g) == [0, 0, 1]

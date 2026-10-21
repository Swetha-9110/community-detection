from community import Graph


def test_dedup_and_self_loops():
    g = Graph([("a", "b"), ("b", "a"), ("a", "a"), ("b", "c")])
    assert g.n == 3
    assert len(g.edges) == 2


def test_edge_list_parsing(tmp_path):
    f = tmp_path / "g.txt"
    f.write_text("# comment\n1 2\n2,3\n3\t4\n\n% another\n")
    g = Graph.from_edge_list(str(f))
    assert g.n == 4
    assert len(g.edges) == 3

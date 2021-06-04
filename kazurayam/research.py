from graphviz import Digraph

g = Digraph("main")
g.attr('graph', layout="dot", rank="max", rankdir="LR",
       splines="ortho", ranksep="0.5", nodesep="0.5")
g.node_attr.update(shape="note", height="0.3")
g.edge_attr.update(constraint="true", arrowhead="onormal")
# ------------------------------------------------
g.node("master", "master", shape="doubleoctagon", width="0.3")
g.edge("master", "commit_3", style="dotted", xlabel="HEAD", constraint="false")
# ------------------------------------------------
g.node("commit_3", "commit_3", shape="ellipse")
g.node("tree_3", "tree_3", shape="folder")
g.edge("commit_3", "tree_3", weight="2")
g.node("tree_hub_3", shape="point", width="0.1")
g.edge("tree_3", "tree_hub_3", arrowhead="none", weight="4")
g.node("blob_3_a", "blob_3_a", shape="note")
g.edge("tree_hub_3", "blob_3_a")
g.node("blob_3_b", "blob_3_b", shape="note")
g.edge("tree_hub_3", "blob_3_b")
g.node("blob_3_c", "blob_3_c", shape="note")
g.edge("tree_hub_3", "blob_3_c")

g.node("tree_3_d", "tree_3_d", shape="folder")
g.node("tree_hub_3_d", shape="point", width="0.1")
g.edge("tree_hub_3", "tree_3_d")
g.edge("tree_3_d", "tree_hub_3_d", arrowhead="none", weight="4")
g.node("blob_3_e", "blob_3_e", shape="note")
g.edge("tree_hub_3_d", "blob_3_e")

# ------------------------------------------------
g.node("commit_2", "commit_2", shape="ellipse")
g.node("tree_2", "tree_2", shape="folder")
g.edge("commit_2", "tree_2", weight="2")
g.node("tree_hub_2", shape="point", width="0.1")
g.edge("tree_2", "tree_hub_2", arrowhead="none", weight="4")
g.node("blob_2_a", "blob_2_a", shape="note")
g.edge("tree_hub_2", "blob_2_a")
g.node("blob_2_b", "blob_2_b", shape="note")
g.edge("tree_hub_2", "blob_2_b")
g.node("blob_2_c", "blob_2_c", shape="note")
g.edge("tree_hub_2", "blob_2_c")
# ------------------------------------------------
g.node("commit_1", "commit_1", shape="ellipse")
g.node("tree_1", "tree_1", shape="folder")
g.edge("commit_1", "tree_1", weight="2")
g.node("tree_hub_1", shape="point", width="0.1")
g.edge("tree_1", "tree_hub_1", arrowhead="none", weight="4")
g.node("blob_1_a", "blob_1_a", shape="note")
g.edge("tree_hub_1", "blob_1_a")
g.node("blob_1_b", "blob_1_b", shape="note")
g.edge("tree_hub_1", "blob_1_b")
# ------------------------------------------------


#with g.subgraph(name="cluster_commits") as c:
#    c.attr(rank="same", color="white")
#    c.node("commit_3")
#    c.node("commit_2")
#    c.edge("commit_3", "commit_2", constraint="false", style="dotted", weight="0")
#    c.node("commit_1")
#    c.edge("commit_2", "commit_1", constraint="false", style="dotted", weight="0")

g.node("commit_3")
g.node("commit_2")
g.edge("commit_3", "commit_2", constraint="false", style="dotted", weight="0")
g.node("commit_1")
g.edge("commit_2", "commit_1", constraint="false", style="dotted", weight="0")

g.render("tmp/research.png", format="png")
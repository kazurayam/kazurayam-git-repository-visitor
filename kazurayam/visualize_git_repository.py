from graphviz import Digraph
from . import gitcommands as GIT


class GitRepositoryVisualizer:

    def __init__(self):
        self.object_commit_links = {}

    def visualize(self, wt: str):
        g = Digraph("main", comment="Git Repository graph")
        g.attr('graph', layout="dot", rank="max", rankdir="LR",
               splines="ortho", ranksep="0.5", nodesep="0.5")
        g.node_attr.update(shape="note", height="0.3", style="filled", fillcolor="white",
                            fontname="arial", fontsize="10")
        g.edge_attr.update(constraint="true", arrowhead="onormal")
        g.node("master", "master", shape="doubleoctagon", width="0.3")
        # grasp the hash of the commit object aliased to HEAD of the current branch (master)
        o = GIT.revparse(wt, "HEAD")
        commit_hash = o.strip()
        self.visualize_commit(wt, commit_hash, g)
        #
        self.grayout_duplicating_nodes(g)
        #
        g.edge("master", commit_hash, style="dotted", label="HEAD")
        return g

    def visualize_commit(self, wt: str, the_commit_hash: str, g: Digraph):
        commits = [the_commit_hash]
        g.node(the_commit_hash, "commit: " + the_commit_hash[0:7], shape="ellipse")
        # look into the commit object
        GIT.catfile_t(wt, the_commit_hash)
        o = GIT.catfile_p(wt, the_commit_hash[0:7])
        """for example
tree 259f232afef1e76cb2a6f0ffb6c167e1fed33bd5
parent bb52f598e0ad27dfe7ad3ca6b59d5e92bf5f7a1f
author kazurayam <kazuaki.urayama@gmail.com> 1622515817 +0900
committer kazurayam <kazuaki.urayama@gmail.com> 1622515817 +0900

added src/good-luck.pl
        """
        # process the linked tree object
        tree_hash = o.splitlines()[0].split()[1]
        # now look into a tree object to trace its internal down
        self.visualize_tree(wt, the_commit_hash, tree_hash, "", g)
        g.edge(the_commit_hash,
               node_id(the_commit_hash, tree_hash))
        # process the commit objects as parent
        for line in o.splitlines():
            if line.startswith("parent"):
                parent_commit_hash = line.split()[1]
                self.visualize_commit(wt, parent_commit_hash, g)
                g.edge(the_commit_hash,
                       parent_commit_hash, constraint="false", style="dotted")
                commits.append(parent_commit_hash)
        # emit cluster_commits
        with g.subgraph(name="cluster_commits",) as c:
            c.attr(rank='same', color="white")
            for h in commits:
                c.node(h)

    def visualize_tree(self, wt: str, commit_hash: str, tree_hash: str, fname: str, g: Digraph):
        self.remember_link(commit_hash, tree_hash)
        tree_node_id = node_id(commit_hash, tree_hash)
        hub_node_id = tree_node_id + "__"
        g.node(tree_node_id,
               "tree: " + tree_hash[0:7] + "\n" + fname + "/",
               shape="folder")
        g.node(hub_node_id, shape="point", width="0.1")
        g.edge(tree_node_id, hub_node_id, arrowhead="none")
        o = GIT.lstree(wt, tree_hash)
        for line in o.splitlines():
            (mode, object_type, object_hash, file_name) = tuple(line.split())
            if object_type == "tree":
                self.visualize_tree(wt, commit_hash, object_hash, file_name, g)  # trace the tree recursively
                g.edge(hub_node_id, node_id(commit_hash, object_hash))
            elif object_type == "blob":
                blob_hash7 = object_hash[0:7]
                GIT.catfile_blob(wt, blob_hash7)
                self.remember_link(commit_hash, object_hash)
                g.node(node_id(commit_hash, object_hash),
                       "blob: " + object_hash[0:7] + "\n" + file_name)
                g.edge(hub_node_id,
                       node_id(commit_hash, object_hash))

    def remember_link(self, commit_hash, object_hash):
        if not (object_hash in self.object_commit_links):
            self.object_commit_links[object_hash] = []
        self.object_commit_links[object_hash].append(commit_hash)

    def grayout_duplicating_nodes(self, g: Digraph):
        for object_hash in self.object_commit_links.keys():
            commit_hash_list = self.object_commit_links.get(object_hash)
            if len(commit_hash_list) > 1:
                for commit_hash in commit_hash_list[:-1]:
                    g.node(node_id(commit_hash, object_hash), fillcolor="lightgrey")


def node_id(commit_hash, object_hash):
    return commit_hash[0:7] + "_" + object_hash[0:7]
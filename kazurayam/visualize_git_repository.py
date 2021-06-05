from graphviz import Digraph
from . import gitcommands as GIT


class GitRepositoryVisualizer:

    def __init__(self):
        self.commits = []
        self.object_commit_reverse_links = {}

    def visualize(self, wt: str):
        g = Digraph("main", comment="Git Repository graph")
        g.attr('graph', layout="dot", rank="max", rankdir="LR",
               splines="ortho", ranksep="0.5", nodesep="0.3")
        g.node_attr.update(shape="note", height="0.3", style="filled", fillcolor="white",
                            fontname="arial", fontsize="10")
        g.edge_attr.update(constraint="true", arrowhead="onormal",
                           fontname="arial", fontsize="10")
        #
        commit_hash = self.visualize_branches(wt, g)
        # place HEAD node and draw edge to the commit object
        g.node("HEAD", "HEAD", shape="doublecircle", width="0.4")
        g.edge("HEAD", commit_hash, constraint="false", style="dashed")
        # gray out the duplicating blobs and trees
        self.grayout_duplicating_nodes(g)
        # done
        return g

    def visualize_branches(self, wt: str, g:Digraph) -> str:
        # grasp the hash of the commit object aliased to HEAD of the current branch (master)
        o = GIT.revparse(wt, "HEAD")
        commit_hash = o.strip()
        #
        g.node("master", "master", shape="doubleoctagon", width="0.3")
        g.edge("master", commit_hash, constraint="false", style="dashed",
               weight="2", minlen="2")
        # draw the great tree
        self.visualize_commit(wt, commit_hash, g)
        return commit_hash

    def visualize_commit(self, wt: str, the_commit_hash: str, g: Digraph):
        self.commits.append(the_commit_hash)
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
        commit_message = get_commit_message(o)
        g.node(the_commit_hash,
               "commit: " + the_commit_hash[0:7] + "\n" + commit_message,
               shape="ellipse")
        # process the tree object as '/'
        tree_hash = o.splitlines()[0].split()[1]
        # now look into a tree object to trace its internal down
        self.visualize_tree(wt, the_commit_hash, tree_hash, "", g)
        g.edge(the_commit_hash,
               node_id(the_commit_hash, tree_hash),
               weight="2")
        # process parent commits recursively
        for line in o.splitlines():
            if line.startswith("parent"):
                parent_commit_hash = line.split()[1]
                self.visualize_commit(wt, parent_commit_hash, g)
                g.edge(the_commit_hash,
                       parent_commit_hash,
                       constraint="false",
                       style="dotted",
                       weight="0")
        # draw the commit objects
        for h in self.commits:
            g.node(h)

    def visualize_tree(self, wt: str, commit_hash: str, tree_hash: str, fname: str, g: Digraph):
        self.remember_link(commit_hash, tree_hash)
        tree_node_id = node_id(commit_hash, tree_hash)
        hub_node_id = tree_node_id + "__"
        g.node(tree_node_id,
               "tree: " + tree_hash[0:7] + "\n" + fname + "/",
               shape="folder")
        g.node(hub_node_id, shape="point", width="0.1")
        g.edge(tree_node_id, hub_node_id, arrowhead="none", weight="4")
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
        if not (object_hash in self.object_commit_reverse_links):
            self.object_commit_reverse_links[object_hash] = []
        self.object_commit_reverse_links[object_hash].append(commit_hash)

    def grayout_duplicating_nodes(self, g: Digraph):
        for object_hash in self.object_commit_reverse_links.keys():
            commit_hash_list = self.object_commit_reverse_links.get(object_hash)
            if len(commit_hash_list) > 1:
                for commit_hash in commit_hash_list[:-1]:
                    g.node(node_id(commit_hash, object_hash), fillcolor="lightgrey")


def node_id(commit_hash, object_hash):
    return commit_hash[0:7] + "_" + object_hash[0:7]


def get_commit_message(commit_content: str) -> str:
    """

    :param commit_content: like
tree 259f232afef1e76cb2a6f0ffb6c167e1fed33bd5
parent bb52f598e0ad27dfe7ad3ca6b59d5e92bf5f7a1f
author kazurayam <kazuaki.urayama@gmail.com> 1622515817 +0900
committer kazurayam <kazuaki.urayama@gmail.com> 1622515817 +0900

added src/good-luck.pl

    :return: commit message, e.g, "added src/good-luck.pl"
    """
    for line in commit_content.splitlines():
        if line.startswith("tree") or \
            line.startswith("parent") or \
            line.startswith("author") or \
            line.startswith("committer") :
            pass
        elif len(line.strip()) == 0:
            pass
        else:
            return line.strip()

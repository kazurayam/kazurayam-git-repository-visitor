from collections import deque
from graphviz import Digraph
from . import gitcommands as GIT


class GitRepositoryVisualizer:

    def __init__(self):
        self.commits = []
        self.object_commit_reverse_links = {}

    def visualize(self, wt: str) -> Digraph:
        g = Digraph("main", comment="Git Repository graph")
        g.attr('graph', layout="dot", rank="max", rankdir="LR",
               splines="ortho", ranksep="0.5", nodesep="0.3")
        g.node_attr.update(shape="note", height="0.3", style="filled", fillcolor="white",
                            fontname="arial", fontsize="10")
        g.edge_attr.update(constraint="true", arrowhead="onormal",
                           fontname="arial", fontsize="10")
        #
        g.node("HEAD", "HEAD", shape="doublecircle", width="0.5", fixedsize="true")

        # process branches
        branch_name = self.visualize_current_branch(wt, g)

        # place HEAD node and draw edge to the commit object
        g.edge("HEAD", branch_name, constraint="true", minlen="1", arrowhead="normal")

        # gray out the duplicating blobs and trees
        self.grayout_duplicating_nodes(g)
        # done
        return g

    def visualize_current_branch(self, wt: str, g:Digraph) -> str:
        branch_name = GIT.branch_show_current(wt)   # "master", "develop" etc
        # grasp the hash of the commit object aliased to the branch
        o = GIT.revparse(wt, branch_name)
        commit_hash = o.strip()
        # draw the branch name node
        g.node(branch_name, branch_name, shape="doubleoctagon", width="0.3")
        g.edge(branch_name, commit_hash, constraint="false", weight="2", minlen="1", arrowhead="normal")
        # draw the great tree
        self.traverse_commits(wt, commit_hash, True, g)
        # draw the commit objects in a subgraph
        with g.subgraph(name="cluster_commits") as c:
            c.attr('graph', color="white")
            c.node(branch_name)
            for h in self.commits:
                c.node(h)
        #
        return branch_name

    def traverse_commits(self, wt: str, top_commit_hash: str, in_detail: bool, g: Digraph):
        # create a Deque (Double-ended-queue)
        dq = deque()
        dq.append(top_commit_hash)
        # repeat until the deque gets empty
        while len(dq) > 0:
            # pop a commit_hash from the top left of the deque
            commit_hash = dq.popleft()
            if commit_hash is not None:
                self.visualize_commit(wt, commit_hash, in_detail, g)
                # append following commits into the Deque
                parent_commits = get_parent_commits(wt, commit_hash)
                for parent in parent_commits:
                    dq.append(parent)
                if len(parent_commits) >= 2:
                    in_detail = False

    def visualize_commit(self, wt: str, the_commit_hash: str, in_detail: bool, g: Digraph):
        if the_commit_hash not in self.commits:
            self.commits.append(the_commit_hash)

            # look into the commit object
            o = GIT.catfile_p(wt, the_commit_hash[0:7])
            commit_message = get_commit_message(o)
            g.node(the_commit_hash,
                   "commit: " + the_commit_hash[0:7] + "\n" + commit_message,
                   shape="ellipse")
            #g.node(the_commit_hash, xlabel="Tag x.x.x")

            if in_detail:
                # now look into the root tree object `/` to trace its internal down
                tree_hash = o.splitlines()[0].split()[1]
                g.edge(the_commit_hash,
                       node_id(the_commit_hash, tree_hash), weight="2", style="dashed")
                self.visualize_tree(wt, the_commit_hash, tree_hash, "", g)

            # select lines that start with "parent"
            parent_lines = [line for line in o.splitlines() if line.startswith("parent")]

            # if this commit object is a merge commit?
            # then print no detail of the merged commits that follow this commit
            if len(parent_lines) >= 2:
                in_detail = False

            # draw edge from this commit to the parent commits
            for line in parent_lines:
                parent_commit_hash = line.split()[1]
                g.edge(the_commit_hash, parent_commit_hash,
                       constraint="false", arrowhead="normal")

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


def get_parent_commits(wt: str, commit_hash) -> tuple:
    o = GIT.catfile_p(wt, commit_hash[0:7])
    """for example
    tree 259f232afef1e76cb2a6f0ffb6c167e1fed33bd5
    parent bb52f598e0ad27dfe7ad3ca6b59d5e92bf5f7a1f
    author kazurayam <kazuaki.urayama@gmail.com> 1622515817 +0900
    committer kazurayam <kazuaki.urayama@gmail.com> 1622515817 +0900

    added src/good-luck.pl
    """
    # select lines that start with "parent"
    parent_lines = [line for line in o.splitlines() if line.startswith("parent")]
    parent_commit_hashes = tuple([line.split()[1] for line in parent_lines])
    return parent_commit_hashes

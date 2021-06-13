from . import gitcommands as GIT


def trace(wt: str):
    # grasp the hash of the commit object aliased to HEAD
    o = GIT.revparse(wt, "HEAD").stdout
    head_hash = o.strip()
    head_hash7 = head_hash[0:7]
    # cat the HEAD commit objectgi
    GIT.catfile_t(wt, head_hash7)
    o = GIT.catfile_p(wt, head_hash7)
    # grasp the hash of the tree object that is pointed by the HEAD commit object
    tree_hash = o.splitlines()[0].split()[1]
    tree_hash7 = tree_hash[0:7]
    # now look into a tree object to trace it down
    trace_tree_or_blob(wt, tree_hash7)


def trace_tree_or_blob(wt, tree_hash):
    o = GIT.lstree(wt, tree_hash)
    for line in o.splitlines():
        (mode, object_type, object_hash, file_name) = tuple(line.split())
        if object_type == "tree":
            sub_tree_hash7 = object_hash[0:7]
            trace_tree_or_blob(wt, sub_tree_hash7)  # trace the tree recursively
        elif object_type == "blob":
            blob_hash7 = object_hash[0:7]
            GIT.catfile_blob(wt, blob_hash7, verbose=True)

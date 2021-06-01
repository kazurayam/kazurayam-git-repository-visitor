from . import gitcommands as GIT


class Main:

    @staticmethod
    def trace(wt: str):
        # grasp the hash of the commit object aliased to HEAD
        o = GIT.revparse(wt, "HEAD")
        head_hash = o.strip()
        head_hash7 = head_hash[0:7]
        # cat the HEAD commit object
        GIT.catfile_t(wt, head_hash7)
        o = GIT.catfile_p(wt, head_hash7)
        # grasp the hash of the tree object that is pointed by the HEAD commit object
        tree_hash = o.splitlines()[0].split()[1]
        tree_hash7 = tree_hash[0:7]
        #
        o = GIT.lstree(wt, tree_hash7)
        for line in o.splitlines():
            (mode, object_type, object_hash, file_name) = tuple(line.split())
            if object_type == "tree":
                tree_hash7 = object_hash[0:7]
                o = GIT.lstree(wt, tree_hash7)
        o = GIT.revparse(wt, "HEAD")
        head_hash = o.strip()
        head_hash7 = head_hash[0:7]
        GIT.catfile_t(wt, head_hash7)
        o = GIT.catfile_p(wt, head_hash7)
        tree_hash = o.splitlines()[0].split()[1]
        tree_hash7 = tree_hash[0:7]
        o = GIT.lstree(wt, tree_hash7)
        for line in o.splitlines():
            (mode, object_type, object_hash, file_name) = tuple(line.split())
            if object_type == "tree":
                tree_hash7 = object_hash[0:7]
                o = GIT.lstree(wt, tree_hash7)

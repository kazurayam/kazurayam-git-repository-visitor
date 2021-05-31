import os
from . import fileutils
from . import gitcommands as GIT


def test_trace(basedir):
    wt = os.path.join(basedir, 'test_trace')
    fileutils.init_dir(wt)
    os.chdir(wt)
    fileutils.write_file(wt, '.gitignore', '*~\n')
    f = fileutils.write_file(wt, "README.md", "# Awesome simplicity of Git\n")
    fileutils.write_file(wt, "src/greeting", "Hello, world!\n")
    fileutils.write_file(wt, "src/hello.pl", "print(\"Bon jour!\")\n")
    assert os.path.exists(f)
    GIT.init(wt, True)
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.commit(wt, "initial commit", True)
    #
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
    #
    f = fileutils.write_file(wt, "src/lucky.pl", "print('Good Luck!')\n")
    print("\n% added src/lucky.pl")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.commit(wt, "modified README", True)
    #
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

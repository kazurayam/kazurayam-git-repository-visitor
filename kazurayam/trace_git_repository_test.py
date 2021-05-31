import os
from . import fileutils
from . import gitcommands as GIT


def test_trace(basedir):
    wt = os.path.join(basedir, 'test_trace')
    fileutils.init_dir(wt)
    os.chdir(wt)
    fileutils.write_file(wt, '.gitignore', '*~\n')
    f = fileutils.write_file(wt, "README.md", "Readme tomorrow\n")
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
    GIT.lstree(wt, tree_hash7)





import os
from . import fileutils
from . import gitcommands as git


def test_trace(basedir):
    wt = os.path.join(basedir, 'test_trace')
    fileutils.init_dir(wt)
    os.chdir(wt)
    fileutils.write_file(wt, '.gitignore', '*~\n')
    f = fileutils.write_file(wt, "README.md", "Readme tomorrow\n")
    fileutils.write_file(wt, "src/greeting", "Hello, world!\n")
    fileutils.write_file(wt, "src/hello.pl", "print(\"Bon jour!\")\n")
    assert os.path.exists(f)
    git.add(wt, '.', True)
    git.commit(wt, "initial commit", True)



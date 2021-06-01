import os
from . import fileutils
from . import gitcommands as GIT
from . import trace_git_repository


def test_trace(basedir):
    wt = os.path.join(basedir, 'test_trace')
    fileutils.init_dir(wt)
    os.chdir(wt)
    #
    fileutils.write_file(wt, '.gitignore', '*~\n')
    f = fileutils.write_file(wt, "README.md", "# Awesome simplicity of Git\n")
    fileutils.write_file(wt, "src/greeting", "Hello, world!\n")
    fileutils.write_file(wt, "src/hello.pl", "print(\"Bon jour!\")\n")
    assert os.path.exists(f)
    GIT.init(wt, True)
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.commit(wt, "initial commit", True)
    trace_git_repository.Main.trace(wt)
    #
    f = fileutils.write_file(wt, "src/lucky.pl", "print('Good Luck!')\n")
    print("\n% added src/lucky.pl")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.commit(wt, "modified README", True)
    trace_git_repository.Main.trace(wt)

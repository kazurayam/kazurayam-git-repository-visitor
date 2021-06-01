import os
from . import fileutils
from . import gitcommands as GIT
from . import graph_git_repository


def test_visualize(basedir):
    wt = os.path.join(basedir, 'test_visualize')
    fileutils.init_dir(wt)
    os.chdir(wt)
    #
    GIT.init(wt, True)
    #
    fileutils.write_file(wt, '.gitignore', '*~\n')
    fileutils.write_file(wt, "README.md", "# Read me please\n")
    fileutils.write_file(wt, "src/greeting", "How do you do?\n")
    fileutils.write_file(wt, "src/hello.pl", "print(\"Hello, world!\")\n")
    #
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "initial commit", True)
    graph_git_repository.visualize(wt)
    GIT.lsfiles_stage(wt)
    #
    f = fileutils.write_file(wt, "src/good-luck.pl", "print('Good Luck!')\n")
    print("\n", "-" * 72)
    print("% added src/good-luck.pl")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "added src/good-luck.pl", True)
    graph_git_repository.visualize(wt)
    GIT.lsfiles_stage(wt)

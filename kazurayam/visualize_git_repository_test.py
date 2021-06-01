import os
from io import StringIO
from graphviz import Digraph
from . import fileutils
from . import gitcommands as GIT
from . import visualize_git_repository


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
    visualizer1 = visualize_git_repository.GitRepositoryVisualizer()
    g1: Digraph = visualizer1.visualize(wt)
    g1.render(os.path.join(basedir, "git-repository-1"), format="png")
    #
    f = fileutils.write_file(wt, "src/good-luck.pl", "print('Good Luck!')\n")
    print("\n", "-" * 72)
    print("% added src/good-luck.pl")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "added src/good-luck.pl", True)
    visualizer2 = visualize_git_repository.GitRepositoryVisualizer()
    g2: Digraph = visualizer2.visualize(wt)
    g2.render(os.path.join(basedir, "git-repository-2"), format="png")


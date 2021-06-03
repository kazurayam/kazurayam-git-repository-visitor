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
    fileutils.write_file(wt, "src/greeting.pl", "print(\"How do you do?\");\n")
    #
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "initial commit", True)
    visualizer1 = visualize_git_repository.GitRepositoryVisualizer()
    g1: Digraph = visualizer1.visualize(wt)
    g1.render(os.path.join(basedir, "git-repository-1"), format="png")
    #
    f = fileutils.write_file(wt, "README.md", "# Read me more carefully\n")
    print("\n", "-" * 72)
    print("% modified README")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "modified README.md", True)
    visualizer2 = visualize_git_repository.GitRepositoryVisualizer()
    g2: Digraph = visualizer2.visualize(wt)
    g2.render(os.path.join(basedir, "git-repository-2"), format="png")
    #
    f = fileutils.write_file(wt, "doc/TODO.txt", "Sleep well tonight.\n")
    print("\n", "-" * 72)
    print("% add doc/TODO.txt")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "add doc/TODO.txt", True)
    visualizer3 = visualize_git_repository.GitRepositoryVisualizer()
    g3: Digraph = visualizer3.visualize(wt)
    g3.render(os.path.join(basedir, "git-repository-3"), format="png")
    #

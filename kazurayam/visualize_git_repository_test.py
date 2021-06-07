import os
from graphviz import Digraph
from .fileutils import write_file
from . import gitcommands as GIT
from . import testutils
from .visualize_git_repository import GitRepositoryVisualizer as GRV


def operate_initial_commit(wt):
    write_file(wt, '.gitignore', '*~\n')
    print("% echo '*~' > .gitignore")
    write_file(wt, "README.md", "# Read me please\n")
    print("% echo '#Read me plase' > README.md")
    write_file(wt, "src/greeting.pl", "print(\"How do you do?\");\n")
    print("% echo 'print(\"How do you do?\");' > src/greeting.pl")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "initial commit", True)


def operate_modify_readme(wt):
    f = write_file(wt, "README.md", "# Read me more carefully\n")
    print("\n", "-" * 72)
    print("% echo '# Read me more carefully' > README.md")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "modified README.md", True)


def operate_add_todo(wt):
    f = write_file(wt, "doc/TODO.txt", "Sleep well tonight.\n")
    print("\n", "-" * 72)
    print("% echo 'Sleep well tonight.' > doc/TODO.txt")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "add doc/TODO.txt", True)


def test_1_object_tree(basedir):
    """
    1. initial commit and make a graph
    2. modify README.md and make a graph
    3. add doc/TODO.txt and make a graph
    on the master branch, without any branch manipulation
    :param basedir:
    :return:
    """
    (wt, gr) = testutils.create_subject_dir(basedir, '1_object_tree')
    GIT.init(wt, True)
    #
    operate_initial_commit(wt)
    GRV().visualize(wt).render(os.path.join(gr, "figure-1.1"), format="png")
    #
    operate_modify_readme(wt)
    GRV().visualize(wt).render(os.path.join(gr, "figure-1.2"), format="png")
    #
    operate_add_todo(wt)
    GRV().visualize(wt).render(os.path.join(gr, "figure-1.3"), format="png")


def test_2_branch_and_merge(basedir):
    """
    1. initial commit; make a graph
    2. create a new branch "develop"; make a graph
    3. in the new branch, modify README.md, commit it; make a graph
    :param basedir:
    :return:
    """
    (wt, gr) = testutils.create_subject_dir(basedir, '2_branch_and_merge')
    GIT.init(wt, True)
    #
    operate_initial_commit(wt)
    GRV().visualize(wt).render(os.path.join(gr, "figure-2.1"), format="png")
    #
    GIT.branch_new(wt, "develop")
    GIT.checkout(wt, "develop")
    def modifier2(g: Digraph):
        g.node('develop', fillcolor="gold")
    GRV().visualize(wt, modifier2).render(os.path.join(gr, "figure-2.2"), format="png")
    #
    operate_add_todo(wt)
    def modifier3(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD")[0:7], fillcolor="deepskyblue")
    GRV().visualize(wt, modifier3).render(os.path.join(gr, "figure-2.3"), format="png")
    #
    GIT.checkout(wt, "master")
    def modifier4(g: Digraph):
        g.node('master', fillcolor="gold")
    GRV().visualize(wt, modifier4).render(os.path.join(gr, "figure-2.4"), format="png")
    #

    operate_modify_readme(wt)
    def modifier5(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD")[0:7], fillcolor="hotpink")
    GRV().visualize(wt, modifier5).render(os.path.join(gr, "figure-2.5"), format="png")
    #
    GIT.merge(wt, "develop")
    def modifier6(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD")[0:7], fillcolor="green3")
        g.node(GIT.revparse(wt, "HEAD^2")[0:7], fillcolor="deepskyblue")
        g.node(GIT.revparse(wt, "HEAD^1")[0:7], fillcolor="hotpink")
    GRV().visualize(wt, modifier6).render(os.path.join(gr, "figure-2.6"), format="png")

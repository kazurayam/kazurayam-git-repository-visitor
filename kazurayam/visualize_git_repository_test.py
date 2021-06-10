import os
from graphviz import Digraph
from .fileutils import write_file
from . import gitcommands as GIT
from . import testutils
from .visualize_git_repository import GitRepositoryVisualizer as GRV


def operate_initial_commit(wt):
    f = write_file(wt, '.gitignore', '*~\n')
    print("% echo '*~' > .gitignore")
    f = write_file(wt, "README.md", "# Read me please\n")
    print("% echo '#Read me plase' > README.md")
    f = write_file(wt, "src/greeting.pl", "print(\"How do you do?\");\n")
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


def operate_modify_greeting(wt):
    f = write_file(wt, "src/greeting.pl", "print(\"Nice to meet you.\");\n")
    print("\n", "-" * 72)
    print("% echo 'print(\"Nice to meet you.\");' > src/greeting.pl")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "modify src/greeting.pl", True)



def test_1_object_tree(basedir):
    """
    Let me look at how commit objects + tree objects + blob objects
    in a Git repository are depicted in a Graphviz graph.

    1. create a Git repository, make the initial commit
    2. modify README.md, commit it
    3. add doc/TODO.txt, commit it
    4. draw a graph of the Git repository
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
    Let me look at how branches and merge operations
    in a Git repository are depicted in a Graphviz graph.

    1. create a Git repository
    2. create a new branch "develop"
    3. make commits in branches
    4. do merging
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


def test_3_tags(basedir):
    """
    Let me look at how Tags in a Git repository are depicted in a Graphviz graph.

    1. create a Git repository
    2. make commits, put tags
    3. visualize the Git repository with tags
    :param basedir:
    :return:
    """
    (wt, gr) = testutils.create_subject_dir(basedir, '3_tags')
    GIT.init(wt, True)
    #
    operate_initial_commit(wt)
    GRV().visualize(wt).render(os.path.join(gr, "figure-3.1"), format="png")
    #
    GIT.tag_to(wt, '0.1.0')
    def modifier2(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD")[0:7],
           xlabel='<<font color="red" face="bold" point-size="18">0.1.0</font>>')
    GRV().visualize(wt, modifier2).render(os.path.join(gr, "figure-3.2"), format="png")
    #
    GIT.branch_new(wt, "develop")
    GIT.checkout(wt, "develop")
    operate_add_todo(wt)
    GIT.tag_to(wt, '0.2.0')
    def modifier3(g: Digraph):
        g.node('develop', fillcolor="gold")
        g.node(GIT.revparse(wt, "HEAD")[0:7],
               xlabel='<<font color="red" face="bold" point-size="18">0.2.0</font>>')
    GRV().visualize(wt, modifier3).render(os.path.join(gr, "figure-3.3"), format="png")
    #
    GIT.checkout(wt, "master")
    operate_modify_greeting(wt)
    GIT.tag_to(wt, '0.1.1')
    def modifier4(g: Digraph):
        g.node('master', fillcolor="gold")
        g.node(GIT.revparse(wt, "HEAD")[0:7],
               xlabel='<<font color="red" face="bold" point-size="18">0.1.1</font>>')
    GRV().visualize(wt, modifier4).render(os.path.join(gr, "figure-3.4"), format="png")
    #
    GIT.checkout(wt, "master")
    GIT.merge(wt, "develop")
    def modifier5(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD^2")[0:7],
               xlabel='<<font color="red" face="bold" point-size="18">0.2.0</font>>')
    GRV().visualize(wt, modifier5).render(os.path.join(gr, "figure-3.5"), format="png")
    #
    operate_modify_readme(wt)
    GIT.tag_to(wt, '0.2.1')
    def modifier6(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD")[0:7],
               xlabel='<<font color="red" face="bold" point-size="18">0.2.1</font>>')
    GRV().visualize(wt, modifier6).render(os.path.join(gr, "figure-3.6"), format="png")


def test_4_index(basedir):
    """
    Let me look at how the Git Index is depicted in a Graphviz graph.

    1. create a Git repository
    2. make commits
    3. visualize the Git Index
    :param basedir:
    :return:
    """
    (wt, gr) = testutils.create_subject_dir(basedir, '4_index')
    GIT.init(wt, True)
    #
    operate_initial_commit(wt)
    GRV().visualize_index(wt).render(os.path.join(gr, "figure-4.1"), format="png")



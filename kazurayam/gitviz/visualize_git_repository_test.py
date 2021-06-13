import os
from graphviz import Digraph
from .fileutils import write_file
from . import gitcommands as GIT, shellcommand as SH, testutils
from .visualize_git_repository import GitRepositoryVisualizer as GRV


def operate_initial_commit(wt):
    f = write_file(wt, '.gitignore', '*~\n')
    print("% echo '*~' > .gitignore")
    f = write_file(wt, "README.md", "# Read me please\n")
    print("% echo '#Read me plase' > README.md")
    f = write_file(wt, "src/greeting.pl", "print(\"How do you do?\");\n")
    print("% echo 'print(\"How do you do?\");' > src/greeting.pl")
    GIT.add(wt, '.', verbose=True)
    GIT.status(wt, verbose=True)
    GIT.lsfiles_stage(wt, verbose=True)
    GIT.commit(wt, "initial commit", verbose=True)


def operate_modify_readme(wt):
    f = write_file(wt, "README.md", "# Read me more carefully\n")
    print("\n", "-" * 72)
    print("% echo '# Read me more carefully' > README.md")
    GIT.add(wt, '.', verbose=True)
    GIT.status(wt, verbose=True)
    GIT.lsfiles_stage(wt, verbose=True)
    GIT.commit(wt, "modified README.md", verbose=True)


def operate_add_todo(wt):
    f = write_file(wt, "doc/TODO.txt", "Sleep well tonight.\n")
    print("\n", "-" * 72)
    print("% echo 'Sleep well tonight.' > doc/TODO.txt")
    GIT.add(wt, '.', verbose=True)
    GIT.status(wt, verbose=True)
    GIT.lsfiles_stage(wt, verbose=True)
    GIT.commit(wt, "add doc/TODO.txt", verbose=True)


def operate_modify_greeting(wt):
    f = write_file(wt, "src/greeting.pl", "print(\"Nice to meet you.\");\n")
    print("\n", "-" * 72)
    print("% echo 'print(\"Nice to meet you.\");' > src/greeting.pl")
    GIT.add(wt, '.', verbose=True)
    GIT.status(wt, verbose=True)
    GIT.lsfiles_stage(wt, verbose=True)
    GIT.commit(wt, "modify src/greeting.pl", verbose=True)



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
    GIT.init(wt, verbose=True)
    #
    operate_initial_commit(wt)
    GRV().visualize_history(wt).render(os.path.join(gr, "figure-1.1"), format="png")
    #
    operate_modify_readme(wt)
    GRV().visualize_history(wt).render(os.path.join(gr, "figure-1.2"), format="png")
    #
    operate_add_todo(wt)
    GRV().visualize_history(wt).render(os.path.join(gr, "figure-1.3"), format="png")


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
    GIT.init(wt, verbose=True)
    #
    operate_initial_commit(wt)
    GRV().visualize_history(wt).render(os.path.join(gr, "figure-2.1"), format="png")
    #
    GIT.branch_new(wt, "develop", verbose=True)
    GIT.checkout(wt, "develop", verbose=True)
    def modifier2(g: Digraph):
        g.node('develop', fillcolor="gold")
    GRV().visualize_history(wt, modifier2).render(os.path.join(gr, "figure-2.2"), format="png")
    #
    operate_add_todo(wt)
    def modifier3(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD").stdout[0:7], fillcolor="deepskyblue")
    GRV().visualize_history(wt, modifier3).render(os.path.join(gr, "figure-2.3"), format="png")
    #
    GIT.checkout(wt, "master")
    def modifier4(g: Digraph):
        g.node('master', fillcolor="gold")
    GRV().visualize_history(wt, modifier4).render(os.path.join(gr, "figure-2.4"), format="png")
    #

    operate_modify_readme(wt)
    def modifier5(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD").stdout[0:7], fillcolor="hotpink")
    GRV().visualize_history(wt, modifier5).render(os.path.join(gr, "figure-2.5"), format="png")
    #
    GIT.merge(wt, "develop")
    def modifier6(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD").stdout[0:7], fillcolor="green3")
        g.node(GIT.revparse(wt, "HEAD^2").stdout[0:7], fillcolor="deepskyblue")
        g.node(GIT.revparse(wt, "HEAD^1").stdout[0:7], fillcolor="hotpink")
    GRV().visualize_history(wt, modifier6).render(os.path.join(gr, "figure-2.6"), format="png")


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
    GIT.init(wt, verbose=True)
    #
    operate_initial_commit(wt)
    GRV().visualize_history(wt).render(os.path.join(gr, "figure-3.1"), format="png")
    #
    GIT.tag_to(wt, '0.1.0', verbose=True)
    def modifier2(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD").stdout[0:7],
           xlabel='<<font color="red" face="bold" point-size="18">0.1.0</font>>')
    GRV().visualize_history(wt, modifier2).render(os.path.join(gr, "figure-3.2"), format="png")
    #
    GIT.branch_new(wt, "develop", verbose=True)
    GIT.checkout(wt, "develop", verbose=True)
    operate_add_todo(wt)
    GIT.tag_to(wt, '0.2.0', verbose=True)
    def modifier3(g: Digraph):
        g.node('develop', fillcolor="gold")
        g.node(GIT.revparse(wt, "HEAD").stdout[0:7],
               xlabel='<<font color="red" face="bold" point-size="18">0.2.0</font>>')
    GRV().visualize_history(wt, modifier3).render(os.path.join(gr, "figure-3.3"), format="png")
    #
    GIT.checkout(wt, "master", verbose=True)
    operate_modify_greeting(wt)
    GIT.tag_to(wt, '0.1.1', verbose=True)
    def modifier4(g: Digraph):
        g.node('master', fillcolor="gold")
        g.node(GIT.revparse(wt, "HEAD").stdout[0:7],
               xlabel='<<font color="red" face="bold" point-size="18">0.1.1</font>>')
    GRV().visualize_history(wt, modifier4).render(os.path.join(gr, "figure-3.4"), format="png")
    #
    GIT.checkout(wt, "master", verbose=True)
    GIT.merge(wt, "develop", verbose=True)
    def modifier5(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD^2").stdout[0:7],
               xlabel='<<font color="red" face="bold" point-size="18">0.2.0</font>>')
    GRV().visualize_history(wt, modifier5).render(os.path.join(gr, "figure-3.5"), format="png")
    #
    operate_modify_readme(wt)
    GIT.tag_to(wt, '0.2.1', verbose=True)
    def modifier6(g: Digraph):
        g.node(GIT.revparse(wt, "HEAD").stdout[0:7],
               xlabel='<<font color="red" face="bold" point-size="18">0.2.1</font>>')
    GRV().visualize_history(wt, modifier6).render(os.path.join(gr, "figure-3.6"), format="png")


def test_4_index(basedir):
    """
    Let me look at how the Git Index is depicted in a Graphviz graph.
    1. create a work tree with a few text files, create a Git repository; draw the 1st graph (emtpy index, no objects yet)
    2. do `git add .`; draw the 3rd graph (index is filled, blob objects, no commits, no trees)
    3. do `git commit`; draw the 4th graph (index remains the same, commits+trees+blobs are linked)
    4. create and add a text file; draw the 5th graph (index is updated, a new blob is added, commits + trees stay unchanged)
    5. do `git commit`; draw the 6th graph (index remains the same, 2 commits+trees+blobs are linked)
    6. modify README and do `git add .`; draw the 7th graph
    7. modify README again and do the `git add .`; draw the 8th graph (1 lonesome blob stands)
    :param basedir:
    :return:
    """
    (wt, gr) = testutils.create_subject_dir(basedir, '4_index')
    f = write_file(wt, '.gitignore', '*~\n')
    print("% echo '*~' > .gitignore")
    f = write_file(wt, "README.md", "# Read me please\n")
    print("% echo '#Read me plase' > README.md")
    f = write_file(wt, "src/greeting.pl", "print(\"How do you do?\");\n")
    print("% echo 'print(\"How do you do?\");' > src/greeting.pl")
    # step1
    sh_quotation = execute_tree_command(wt)
    GIT.init(wt, verbose=True)
    SH.shell_command(wt, ['ls', '-la', '.'], verbose=True)
    SH.shell_command(wt, ['ls', '-la', './.git'], verbose=True)
    GRV().visualize_index(wt, sh_quotation, label='ステップ1 git initした後でgit addする前').render(
        os.path.join(gr, "figure-4.1"), format="png")
    # step2
    GIT.add(wt, '.', verbose=True)
    GRV().visualize_index(wt, sh_quotation, label='ステップ2 git addしたらインデックスとblobが更新された').render(
        os.path.join(gr, "figure-4.2"), format="png")
    # step3
    GIT.commit(wt, 'initial commit', verbose=True)
    GRV().visualize_index(wt, sh_quotation, label='ステップ3 git commitしたらblobがツリーにつながった').render(
        os.path.join(gr, "figure-4.3"), format="png")
    # step4
    f = write_file(wt, "doc/TODO.txt", "Sleep well tonight.\n")
    sh_quotation = execute_tree_command(wt)
    def modifier4(g: Digraph):
        g.node("w_6", fillcolor="gold")
    GRV().visualize_index(wt, sh_quotation, modifier4, label='ステップ4 TODO.txtファイルを追加してgit addする前').render(
        os.path.join(gr, "figure-4.4"), format="png")
    # step5
    GIT.add(wt, '.', verbose=True)
    def modifier5(g: Digraph):
        g.node("x_de13371", fillcolor="gold")
        g.node("j_de13371", fillcolor="gold")
    GRV().visualize_index(wt, sh_quotation, modifier5, label='ステップ5 git addしたらインデックスとblobが更新された').render(
        os.path.join(gr, "figure-4.5"), format="png")
    # step6
    GIT.commit(wt, 'add doc/TODO.txt', verbose=True)
    def modifier6(g: Digraph):
        g.node("j_de13371", fillcolor="gold")
    GRV().visualize_index(wt, sh_quotation, modifier6, label='ステップ6 git commitしたらblobがツリーにつながった').render(
        os.path.join(gr, "figure-4.6"), format="png")
    # step7
    f = write_file(wt, "README.md", "# Read me more carefully\n")
    def modifier7(g: Digraph):
        g.node("w_4", fillcolor="hotpink")
        g.node("j_5a79541", fillcolor="hotpink")
        g.node("x_5a79541", fillcolor="hotpink")
        g.node("j_aadb69a", fillcolor="lightgrey")
    GIT.add(wt, '.', verbose=True)
    GRV().visualize_index(wt, sh_quotation, modifier7, label='ステップ7 READMEファイルを修正してgit addした').render(
        os.path.join(gr, "figure-4.7"), format="png")
    # step8
    f = write_file(wt, "README.md", "# I know you didnt read me.\n")
    GIT.add(wt, '.', verbose=True)
    GIT.status(wt, verbose=True)
    def modifier8(g: Digraph):
        g.node("w_4", fillcolor="deepskyblue")
        g.node("j_5a79541", fillcolor="black", fontcolor="white")
        g.node("j_9230643", fillcolor="deepskyblue")
        g.node("x_9230643", fillcolor="deepskyblue")
        g.node("j_aadb69a", fillcolor="lightgrey")
    GRV().visualize_index(wt, sh_quotation, modifier8, label='ステップ8 READMEファイルをもう一度修正してgit addした').render(
        os.path.join(gr, "figure-4.8"), format="png")
    # step9
    GIT.commit(wt, 'modified README.md', verbose=True)
    def modifier9(g: Digraph):
        g.node("j_5a79541", fillcolor="black", fontcolor="white")
        g.node("j_9230643", fillcolor="gold")
        g.node("j_aadb69a", fillcolor="lightgrey")
    GRV().visualize_index(wt, sh_quotation, modifier9, label='ステップ9 READMEファイルをgit commitした').render(
        os.path.join(gr, "figure-4.9"), format="png")


def execute_tree_command(wt: str) -> list:
    args = ['tree', '-afni', '-I', '.git']
    completed_process = SH.shell_command(wt, args)
    commandline = [' '.join(args)]
    commandline.extend(completed_process.stdout.splitlines())
    commandline[0] = '% ' + commandline[0]
    return commandline

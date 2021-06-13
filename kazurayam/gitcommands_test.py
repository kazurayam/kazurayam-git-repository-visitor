import pytest
import re
from . import fileutils
from . import gitcommands as GIT
from . import testutils
from .shellcommand import shell_command


@pytest.fixture(scope="module")
def wt_with_initial_commit(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'gitcommands_test')
    GIT.init(wt)
    fileutils.write_file(wt, '.gitignore', '*~\n')
    fileutils.write_file(wt, "README.md", "# Read me please\n")
    fileutils.write_file(wt, "src/greeting.pl", "print(\"How do you do?\");\n")
    GIT.add(wt, '.')
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "initial commit")
    GIT.tag_to(wt, '0.1.0')
    yield wt


def test_init(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'test_init')
    stdout = GIT.init(wt)
    assert stdout.startswith("hint:")


def test_add(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'test_add')
    fileutils.write_file(wt, '.gitignore', '*~\n')
    stdout = GIT.init(wt)
    stdout = GIT.add(wt, '.')
    assert stdout == ""


def test_status(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'test_status')
    fileutils.write_file(wt, '.gitignore', '*~\n')
    stdout = GIT.init(wt)
    stdout = GIT.status(wt)
    assert stdout.startswith("On branch master")


def test_commit(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'test_commit')
    fileutils.write_file(wt, '.gitignore', '*~\n')
    stdout = GIT.init(wt)
    stdout = GIT.add(wt, '.')
    stdout = GIT.commit(wt, 'add .gitignore')
    assert '.gitignore' in stdout


def test_catfile_t(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'test_catfile_t')
    fileutils.write_file(wt, '.gitignore', '*~\n')
    stdout = GIT.init(wt)
    stdout = GIT.add(wt, '.')
    stdout = GIT.commit(wt, 'add .gitignore')
    stdout = GIT.catfile_t(wt, 'HEAD')
    assert stdout == 'commit'


def test_catfile_p(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'test_catfile_p')
    fileutils.write_file(wt, '.gitignore', '*~\n')
    stdout = GIT.init(wt)
    stdout = GIT.add(wt, '.')
    stdout = GIT.commit(wt, 'add .gitignore')
    stdout = GIT.catfile_p(wt, 'HEAD')
    """
    tree ...
    author ...
    committer ...
    
    message
    """
    assert stdout.startswith('tree')


def test_catfile_blob(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'test_catfile_blob')
    fileutils.write_file(wt, '.gitignore', '*~\n')
    stdout = GIT.init(wt)
    stdout = GIT.add(wt, '.')
    stdout = GIT.commit(wt, 'add .gitignore')
    cp = shell_command(wt, ['git', 'ls-tree', '-r', 'HEAD'])
    """
    $ git ls-tree -r HEAD
    100644 blob fb7c93af634239c075b1b0c8c6c19bbeede0ed54    .DS_Store
    100644 blob 3e152b50e7ea36b543d598cf626fcd631cdc6c49    .gitignore
    ...
    """
    for line in cp.stdout.splitlines():
        if line.split()[3] == '.gitignore':
            gitignore_hash = line.split()[2]
    assert gitignore_hash is not None
    stdout = GIT.catfile_p(wt, gitignore_hash)
    assert stdout.startswith('*~')


def test_showref_heads(wt_with_initial_commit):
    o = GIT.showref_heads(wt_with_initial_commit, verbose=False)
    # o will be something like:
    # 5a2ff8b69af20008486fab4423894b895c9aee77 refs/heads/master
    assert re.match(r'^[0-9a-f]{40}', o)
    assert 'refs/heads/master' in o


def test_branch_new_then_checkout(wt_with_initial_commit):
    o = GIT.branch_new(wt_with_initial_commit, "develop")
    o = GIT.checkout(wt_with_initial_commit, "develop")
    assert "Switched to branch 'develop'" in o
    o = GIT.branch_show_current(wt_with_initial_commit)
    assert "develop" in o


def test_tag_points_at(wt_with_initial_commit):
    commit_object = GIT.revparse(wt_with_initial_commit, "HEAD")[0].strip()
    t = GIT.tag_points_at(wt_with_initial_commit, commit_object)
    assert t[1] == 0
    assert t[0] == '0.1.0'


def test_catfile_batchcheck_batchallobjects(wt_with_initial_commit):
    completed_process = GIT.catfile_batchcheck_batchallobjects(wt_with_initial_commit)
    assert completed_process.returncode == 0
    lines = completed_process.stdout.splitlines()
    assert len(lines) == 6
    # 1 commit, 2 trees, 3 blobs = 6 objects

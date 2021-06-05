import pytest
import re
from . import fileutils
from . import gitcommands as GIT
from . import testutils

@pytest.fixture(scope="module")
def wt_with_initial_commit(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'gitcommands_test')
    GIT.init(wt, True)
    fileutils.write_file(wt, '.gitignore', '*~\n')
    fileutils.write_file(wt, "README.md", "# Read me please\n")
    fileutils.write_file(wt, "src/greeting.pl", "print(\"How do you do?\");\n")
    GIT.add(wt, '.', True)
    GIT.status(wt)
    GIT.lsfiles_stage(wt)
    GIT.commit(wt, "initial commit", True)
    yield wt


def test_showref_heads(wt_with_initial_commit):
    o = GIT.showref_heads(wt_with_initial_commit, verbose=False)
    print(o)
    # o will be something like:
    # 5a2ff8b69af20008486fab4423894b895c9aee77 refs/heads/master
    assert re.match(r'^[0-9a-f]{40}', o)
    assert 'refs/heads/master' in o


def test_branch_new_then_checkout(wt_with_initial_commit):
    o = GIT.branch_new(wt_with_initial_commit, "develop")
    print(o)
    o = GIT.checkout(wt_with_initial_commit, "develop")
    print(o)
    assert "Switched to branch 'develop'" in o
    o = GIT.branch_show_current(wt_with_initial_commit)
    assert "develop" in o

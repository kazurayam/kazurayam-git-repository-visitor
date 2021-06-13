import pytest
import re
from . import fileutils
from . import gitcommands as GIT
from . import testutils
from .shellcommand import shell_command


@pytest.fixture(scope="function")
def wt_with_initial_commit(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'gitcommands_test')
    GIT.init(wt)
    fileutils.write_file(wt, '.gitignore', '*~\n')
    fileutils.write_file(wt, "README.md", "# Read me please\n")
    fileutils.write_file(wt, "src/greeting.pl", "print(\"How do you do?\");\n")
    GIT.add(wt, '.')
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


def test_commit(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'test_commit')
    fileutils.write_file(wt, '.gitignore', '*~\n')
    stdout = GIT.init(wt)
    stdout = GIT.add(wt, '.')
    stdout = GIT.commit(wt, 'add .gitignore')
    assert '.gitignore' in stdout


def test_status(wt_with_initial_commit):
    stdout = GIT.status(wt_with_initial_commit)
    assert stdout.startswith("On branch master")


def test_catfile_t(wt_with_initial_commit):
    stdout = GIT.catfile_t(wt_with_initial_commit, 'HEAD')
    """
    $ git cat-file -t HEAD
    commit
    """
    assert stdout == 'commit'


def test_catfile_p(wt_with_initial_commit):
    stdout = GIT.catfile_p(wt_with_initial_commit, 'HEAD')
    """
    $ git cat-file -p HEAD
    tree ...
    author ...
    committer ...
    
    message
    """
    assert stdout.startswith('tree')


def test_catfile_blob(wt_with_initial_commit):
    cp = shell_command(wt_with_initial_commit, ['git', 'ls-tree', '-r', 'HEAD'])
    """
    $ git ls-tree -r HEAD
    100644 blob fb7c93af634239c075b1b0c8c6c19bbeede0ed54    .DS_Store
    100644 blob 3e152b50e7ea36b543d598cf626fcd631cdc6c49    .gitignore
    ...
    """
    blob_hash = None
    for line in cp.stdout.splitlines():
        if line.split()[3] == '.gitignore':
            blob_hash = line.split()[2]
    assert blob_hash is not None
    stdout = GIT.catfile_p(wt_with_initial_commit, blob_hash)
    assert stdout.startswith('*~')


def test_revparse(wt_with_initial_commit):
    # cp stands for subprocess.CompletedProcess
    cp = GIT.revparse(wt_with_initial_commit, 'HEAD')
    """
    $ git rev-parse HEAD
    1e29db36da84624f599357777d986fa37aa5869d
    """
    assert re.match(r'^[0-9a-f]{40}', cp.stdout)


def test_lstree(wt_with_initial_commit):
    stdout = GIT.lstree(wt_with_initial_commit, 'HEAD')
    """
    $ git ls-tree HEAD
100644 blob fb7c93af634239c075b1b0c8c6c19bbeede0ed54    .DS_Store
100644 blob 3e152b50e7ea36b543d598cf626fcd631cdc6c49    .gitignore
...
    """
    assert len(stdout.splitlines()) > 0
    assert re.match(r'^[0-9a-f]{40}', stdout.splitlines()[0].split()[2])


def test_lsfiles_stage(wt_with_initial_commit):
    stdout = GIT.lsfiles_stage(wt_with_initial_commit)
    """
    $ git ls-files --stage
100644 fb7c93af634239c075b1b0c8c6c19bbeede0ed54 0       .DS_Store
100644 3e152b50e7ea36b543d598cf626fcd631cdc6c49 0       .gitignore
...
    """
    assert len(stdout.splitlines()) > 0
    assert re.match(r'^[0-9a-f]{40}', stdout.splitlines()[0].split()[1])


def test_showref_heads(wt_with_initial_commit):
    stdout = GIT.showref_heads(wt_with_initial_commit, verbose=False)
    """
    $ git show-ref --heads
    b114566da8f14ed186efba10388d47979c78e4f5 refs/heads/develop
    b114566da8f14ed186efba10388d47979c78e4f5 refs/heads/master
    """
    assert len(stdout.splitlines()) > 0
    assert re.match(r'^[0-9a-f]{40}', stdout.splitlines()[0].split()[0])
    assert 'refs/heads/master' in stdout


def test_branch_new(wt_with_initial_commit):
    o = GIT.branch_new(wt_with_initial_commit, "develop")
    """
    $ git branch develop
    (shows nothing in stdout)
    """
    cp = shell_command(wt_with_initial_commit, ['git', 'branch'])
    """
    $ git branch
      develop
    * master
    """
    assert len(cp.stdout.splitlines()) == 2
    assert 'develop' in cp.stdout
    assert 'master' in cp.stdout


def test_checkout(wt_with_initial_commit):
    o = GIT.branch_new(wt_with_initial_commit, "develop")
    """
    $ git branch develop
    (shows nothing in stdout)
    """
    o = GIT.checkout(wt_with_initial_commit, "develop")
    """
    $ git checkout
    Switched to branch 'develop'
    """
    assert "Switched to branch 'develop'" in o


def test_branch_show_current(wt_with_initial_commit):
    o = GIT.branch_show_current(wt_with_initial_commit)
    """
    $ git branch --show--current
    master
    """
    assert "master" in o


def test_merge(wt_with_initial_commit):
    o = GIT.branch_new(wt_with_initial_commit, "develop")
    content = "# Read me very crefully"
    fileutils.write_file(wt_with_initial_commit, "README.md", content)
    o = GIT.add(wt_with_initial_commit, '.')
    o = GIT.commit(wt_with_initial_commit, "modified README.md")
    o = GIT.checkout(wt_with_initial_commit, 'master')
    o = GIT.merge(wt_with_initial_commit, 'develop')
    blob_hash = None
    for line in GIT.lstree(wt_with_initial_commit, 'HEAD').splitlines():
        """
        $ git ls-tree HEAD
        100644 blob 3e152b50e7ea36b543d598cf626fcd631cdc6c49    .gitignore
        ...
        """
        if "README.md" in line:
            blob_hash = line.split()[2]
    assert blob_hash is not None
    assert re.match(r'^[0-9a-f]{40}', blob_hash)
    assert content in GIT.catfile_p(wt_with_initial_commit, blob_hash)


def test_tag_to(wt_with_initial_commit):
    o = GIT.tag_to(wt_with_initial_commit, '0.1.0')
    cp = shell_command(wt_with_initial_commit, ['git', 'tag'])
    assert len(cp.stdout.splitlines()) == 1
    assert cp.stdout.splitlines()[0] == '0.1.0'


def test_tag_points_at(wt_with_initial_commit):
    commit_object = GIT.revparse(wt_with_initial_commit, "HEAD").stdout.strip()
    cp = GIT.tag_points_at(wt_with_initial_commit, commit_object)
    assert cp.returncode == 0
    assert cp.stdout == '0.1.0'


def test_catfile_batchcheck_batchallobjects(wt_with_initial_commit):
    completed_process = GIT.catfile_batchcheck_batchallobjects(wt_with_initial_commit)
    assert completed_process.returncode == 0
    lines = completed_process.stdout.splitlines()
    assert len(lines) == 6
    # 1 commit, 2 trees, 3 blobs = 6 objects

import subprocess
from subprocess import PIPE, STDOUT
from .shellcommand import decode_stdout, print_msg
from .shellcommand import shell_command


def add(wt, path, verbose=False) -> subprocess.CompletedProcess:
    args = ["git", "add", path]
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def branch_new(wt, branch_name: str, verbose=False) -> subprocess.CompletedProcess:
    args = ['git', 'branch', branch_name]
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def branch_show_current(wt, verbose=False) -> subprocess.CompletedProcess:
    args = ['git', 'branch', '--show-current']
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def catfile_batchcheck_batchallobjects(wt:str, verbose=False) -> subprocess.CompletedProcess:
    """
    executes `git cat-file --batch-check --batch-all-objects`
    this command list all objects in the .git/objects directory regardless
    if each of them is reachable from the commits.
    In other words, this command can list the blob objects
    which have been added but not het commited.
    :param wt:
    :param verbose:
    :return: subprocess.CompletedProcess object
    the stdout could be for example:

$ git cat-file --batch-check --batch-all-objects
aadb69a077c74818e3aff608c0c60c56c6c7c6c9 blob 17
b25c15b81fae06e1c55946ac6270bfdb293870e8 blob 3
b371df9d9194821c4a54f0e3a77f89bbcee62f7e blob 25

    """
    args = ['git', 'cat-file', '--batch-check', '--batch-all-objects']
    return shell_command(wt, args, verbose)


def catfile_blob(wt, gitobject: str, verbose=False) -> subprocess.CompletedProcess:
    args = ['git', 'cat-file', 'blob', gitobject]
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def catfile_p(wt, gitobject: str, verbose=False) -> subprocess.CompletedProcess:
    args = ['git', 'cat-file', '-p', gitobject]
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def catfile_t(wt, gitobject: str, verbose=False) -> subprocess.CompletedProcess:
    args = ['git', 'cat-file', '-t', gitobject]
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def checkout(wt, branch_name: str, verbose=False) -> subprocess.CompletedProcess:
    args = ['git', 'checkout', branch_name]
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def commit(wt, msg, verbose=False) -> subprocess.CompletedProcess:
    args = ['git', 'commit', '-m', msg]
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def init(wt: str, verbose=False) -> subprocess.CompletedProcess:
    # cp stands for Completed Process as defined in Python subprocess
    args = ['git', 'init']
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def lsfiles_stage(wt, verbose=False) -> str:
    """
    execute `git ls-file --stage` command
    this command shows the content of the Index
    :param wt:
    :param verbose:
    :return:
    """
    args = ['git', 'ls-files', '--stage']
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def lstree(wt, gitobject: str, verbose=False) -> str:
    args = ['git', 'ls-tree', gitobject]
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def merge(wt, branch_name: str, verbose=False) -> str:
    args = ['git', 'merge', branch_name]
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def revparse(wt, gitobject: str, verbose=False) -> subprocess.CompletedProcess:
    args = ['git', 'rev-parse', gitobject]
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def showref_heads(wt, verbose=False) -> str:
    """
    execute `git show-ref --heads` command
    this command shows something like this:
    ```
    b114566da8f14ed186efba10388d47979c78e4f5 refs/heads/develop
    b114566da8f14ed186efba10388d47979c78e4f5 refs/heads/master
    ```
    :param wt:
    :param verbose:
    :return:
    """
    args = ['git', 'show-ref', '--heads']
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def status(wt, verbose=False) -> str:
    args = ['git', 'status']
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def tag_points_at(wt, object: str, verbose=False) -> subprocess.CompletedProcess:
    """
    execute `git tag --points-at <object>` command.
    retrieves tag_name that refers to the object.
    If the tag was found, will return an instance of subprocess.CompletedProcess
    with the returncode == 0 and the stdout (=tag name).
    If the tag was NOT found, will return an instance of subprocess.CompletedProcess
    with the returncode != 0. You should not refer to the stdout.
    :param wt:
    :param object:
    :param verbose:
    :return: subprocess.CompletedProcess
    """
    args = ['git', 'tag', '--points-at', object]
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def tag_to(wt, tag_name: str, refer_to: str = 'HEAD', verbose=False) -> str:
    args = ['git', 'tag', tag_name, refer_to]
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout

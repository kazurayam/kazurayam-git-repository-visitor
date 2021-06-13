import subprocess
from subprocess import PIPE, STDOUT
from .shellcommand import decode_stdout, print_msg
from .shellcommand import shell_command


def init(wt: str, verbose=False) -> str:
    """
    execute `git init` command in a new process
    :param wt:
    :param verbose:
    :return: STDOUT+STDERROR emitted by the process where the git command was executed
    """
    # cp stands for Completed Process as defined in Python subprocess
    args = ['git', 'init']
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def add(wt, path, verbose=False) -> str:
    args = ["git", "add", path]
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def status(wt, verbose=False) -> str:
    args = ['git', 'status']
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def commit(wt, msg, verbose=False) -> str:
    args = ['git', 'commit', '-m', msg]
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def catfile_t(wt, gitobject: str, verbose=False) -> str:
    args = ['git', 'cat-file', '-t', gitobject]
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def catfile_p(wt, gitobject: str, verbose=False) -> str:
    args = ['git', 'cat-file', '-p', gitobject]
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


def catfile_blob(wt, gitobject: str, verbose=False) -> str:
    completed_process = subprocess.run(['git', 'cat-file', 'blob', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git cat-file blob", gitobject)
        print_msg(completed_process)
    return decode_stdout(completed_process)


def revparse(wt, gitobject: str, verbose=False) -> subprocess.CompletedProcess:
    args = ['git', 'rev-parse', gitobject]
    cp = shell_command(wt, args, verbose=verbose)
    return cp


def lstree(wt, gitobject: str, verbose=False) -> str:
    args = ['git', 'ls-tree', gitobject]
    cp = shell_command(wt, args, verbose=verbose)
    return cp.stdout


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
    completed_process = subprocess.run(['git', 'show-ref', '--heads'], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git show-ref --heads")
        print_msg(completed_process)
    return decode_stdout(completed_process)


def branch_new(wt, branch_name: str, verbose=False) -> str:
    """
    execute `git branch <brancc_name>` command
    :param wt:
    :param branch_name: e.g, "develop", "main" etc
    :param verbose:
    :return:
    """
    completed_process = subprocess.run(['git', 'branch', branch_name], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git branch", branch_name)
        print_msg(completed_process)
    return decode_stdout(completed_process)


def branch_show_current(wt, verbose=False) -> str:
    """
    execute `git branch --show-current` command
    this will show the current branch which you are on currently
    :param wt:
    :param verbose:
    :return:
    """
    completed_process = subprocess.run(['git', 'branch', '--show-current'], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git branch", "--show-current")
        print_msg(completed_process)
    return decode_stdout(completed_process)


def checkout(wt, branch_name: str, verbose=False) -> str:
    """
    execute `git checkout <branch_name>` command
    :param wt:
    :param branch_name:
    :param verbose:
    :return:
    """
    completed_process = subprocess.run(['git', 'checkout', branch_name], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git checkout", branch_name)
        print_msg(completed_process)
    return decode_stdout(completed_process)


def merge(wt, branch_name: str, verbose=False) -> str:
    """
    execute `git merge <branch_name>` command
    :param wt:
    :param branch_name:
    :param verbose:
    :return:
    """
    completed_process = subprocess.run(['git', 'merge', branch_name], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git merge", branch_name)
        print_msg(completed_process)
    return decode_stdout(completed_process)


def tag_to(wt, tag_name: str, refer_to: str = 'HEAD', verbose=False) -> str:
    """
    execute `git tag <tag_name> <refer_to>` command
    :param wt:
    :param tag_name:
    :param refer_to:
    :param verbose:
    :return:
    """
    completed_process = subprocess.run(['git', 'tag', tag_name, refer_to], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git tag", tag_name, refer_to)
        print_msg(completed_process)
    return decode_stdout(completed_process)


def tag_points_at(wt, object: str, verbose=False) -> tuple:
    """
    execute `git tag --points-at <object>` command.
    retrieves tag_name that refers to the object.
    if the tag was found returns a tuple of (tag_name, 0).
    if not found returns a tuple of ("error: malformed object name 'xxxx'", non-0 integer)
    the caller should check the return code first and read the tag_name only when it is found.
    :param wt:
    :param object:
    :param verbose:
    :return: a tuple of (stdout, return_code)
    """
    completed_process = subprocess.run(['git', 'tag', '--points-at', object],
                            cwd=wt, stdout=PIPE, stderr=STDOUT,
                            check=False)
    if verbose:
        print("\n% git tag --points-at", object)
        print_msg(completed_process)
    return decode_stdout(completed_process), completed_process.returncode


def catfile_batchcheck_batchallobjects(wt:str, verbose=False):
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

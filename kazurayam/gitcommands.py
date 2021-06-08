import os
import subprocess
from subprocess import PIPE, STDOUT, Popen


def get_git_msg(completed_process) -> str:
    try:
        msg = completed_process.stdout.decode("ascii").strip()
        return msg
    except UnicodeDecodeError:
        return "!!!! stdout is a binary sequence !!!!"


def print_git_msg(completed_process):
    print("{}".format(get_git_msg(completed_process)))


def init(wt: str, verbose=True) -> str:
    """
    execute `git init` command in a new process
    :param wt:
    :param verbose:
    :return: STDOUT+STDERROR emitted by the process where the git command was executed
    """
    completed_process = subprocess.run('git init'.split(), cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git init")
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def add(wt, path, verbose=True) -> str:
    completed_process = subprocess.run(['git', 'add', path], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git add", path)
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def status(wt, verbose=True) -> str:
    completed_process = subprocess.run(['git', 'status'], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git status")
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def commit(wt, msg, verbose=True):
    completed_process = subprocess.run(['git', 'commit', '-m', msg], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git commit -m \"{}\"".format(msg))
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def catfile_t(wt, gitobject: str, verbose=True) -> str:
    completed_process = subprocess.run(['git', 'cat-file', '-t', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git cat-file -t", gitobject)
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def catfile_p(wt, gitobject: str, verbose=True) -> str:
    completed_process = subprocess.run(['git', 'cat-file', '-p', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git cat-file -p", gitobject)
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def catfile_blob(wt, gitobject: str, verbose=True) -> str:
    completed_process = subprocess.run(['git', 'cat-file', 'blob', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git cat-file blob", gitobject)
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def revparse(wt, gitobject: str, verbose=True) -> str:
    completed_process = subprocess.run(['git', 'rev-parse', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git rev-parse", gitobject)
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def lstree(wt, gitobject: str, verbose=True) -> str:
    completed_process = subprocess.run(['git', 'ls-tree', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git ls-tree", gitobject)
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def lsfiles_stage(wt, verbose=True) -> str:
    """
    execute `get ls-file --stage` command
    this command shows the content of the Index
    :param wt:
    :param verbose:
    :return:
    """
    completed_process = subprocess.run(['git', 'ls-files', '--stage'], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git ls-files --stage")
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def showref_heads(wt, verbose=True) -> str:
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
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def branch_new(wt, branch_name: str, verbose=True) -> str:
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
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def branch_show_current(wt, verbose=True) -> str:
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
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def checkout(wt, branch_name: str, verbose=True) -> str:
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
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def merge(wt, branch_name: str, verbose=True) -> str:
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
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def tag_to(wt, tag_name: str, refer_to: str = 'HEAD', verbose=True) -> str:
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
        print_git_msg(completed_process)
    return get_git_msg(completed_process)


def tag_points_at(wt, object: str, verbose=True) -> tuple:
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
        print_git_msg(completed_process)
    return get_git_msg(completed_process), completed_process.returncode

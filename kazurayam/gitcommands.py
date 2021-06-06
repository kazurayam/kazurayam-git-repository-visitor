import os
import subprocess
from subprocess import PIPE, STDOUT


def get_git_msg(output) -> str:
    try:
        msg = output.stdout.decode("ascii").strip()
        return msg
    except UnicodeDecodeError:
        return "!!!! binary file, unable to decode as ascii characters !!!!"


def print_git_msg(output):
    print("{}".format(get_git_msg(output)))


def init(wt: str, verbose=False) -> str:
    """
    execute `git init` command in a new process
    :param wt:
    :param verbose:
    :return: STDOUT+STDERROR emitted by the process where the git command was executed
    """
    output = subprocess.run('git init'.split(), cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git init")
        print_git_msg(output)
    return get_git_msg(output)


def add(wt, path, verbose=False) -> str:
    output = subprocess.run(['git', 'add', path], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git add", path)
        print_git_msg(output)
    return get_git_msg(output)


def status(wt, verbose=True) -> str:
    output = subprocess.run(['git', 'status'], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git status")
        print_git_msg(output)
    return get_git_msg(output)


def commit(wt, msg, verbose=False):
    output = subprocess.run(['git', 'commit', '-m', msg], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git commit -m \"{}\"".format(msg))
        print_git_msg(output)
    return get_git_msg(output)


def catfile_t(wt, gitobject: str, verbose=True) -> str:
    output = subprocess.run(['git', 'cat-file', '-t', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git cat-file -t", gitobject)
        print_git_msg(output)
    return get_git_msg(output)


def catfile_p(wt, gitobject: str, verbose=True) -> str:
    output = subprocess.run(['git', 'cat-file', '-p', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git cat-file -p", gitobject)
        print_git_msg(output)
    return get_git_msg(output)


def catfile_blob(wt, gitobject: str, verbose=True) -> str:
    output = subprocess.run(['git', 'cat-file', 'blob', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git cat-file blob", gitobject)
        print_git_msg(output)
    return get_git_msg(output)


def revparse(wt, gitobject: str, verbose=True) -> str:
    output = subprocess.run(['git', 'rev-parse', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git rev-parse", gitobject)
        print_git_msg(output)
    return get_git_msg(output)


def lstree(wt, gitobject: str, verbose=True) -> str:
    output = subprocess.run(['git', 'ls-tree', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git ls-tree", gitobject)
        print_git_msg(output)
    return get_git_msg(output)


def lsfiles_stage(wt, verbose=True) -> str:
    """
    execute `get ls-file --stage` command
    this command shows the content of the Index
    :param wt:
    :param verbose:
    :return:
    """
    output = subprocess.run(['git', 'ls-files', '--stage'], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git ls-files --stage")
        print_git_msg(output)
    return get_git_msg(output)


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
    output = subprocess.run(['git', 'show-ref', '--heads'], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git show-ref --heads")
        print_git_msg(output)
    return get_git_msg(output)


def branch_new(wt, branch_name: str, verbose=False) -> str:
    """
    execute `git branch <brancc_name>` command
    :param wt:
    :param branch_name: e.g, "develop", "main" etc
    :param verbose:
    :return:
    """
    output = subprocess.run(['git', 'branch', branch_name], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git branch", branch_name)
        print_git_msg(output)
    return get_git_msg(output)

def branch_show_current(wt, verbose=True) -> str:
    """
    execute `git branch --show-current` command
    this will show the current branch which you are on currently
    :param wt:
    :param verbose:
    :return:
    """
    output = subprocess.run(['git', 'branch', '--show-current'], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git branch", "--show-current")
        print_git_msg(output)
    return get_git_msg(output)


def checkout(wt, branch_name: str, verbose=False) -> str:
    """
    execute `git checkout <branch_name>` command
    :param wt:
    :param branch_name:
    :param verbose:
    :return:
    """
    output = subprocess.run(['git', 'checkout', branch_name], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git checkout", branch_name)
        print_git_msg(output)
    return get_git_msg(output)


def merge(wt, branch_name: str, verbose=False) -> str:
    """
    execute `git merge <branch_name>` command
    :param wt:
    :param branch_name:
    :param verbose:
    :return:
    """
    output = subprocess.run(['git', 'merge', branch_name], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git merge", branch_name)
        print_git_msg(output)
    return get_git_msg(output)

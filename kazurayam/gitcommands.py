import os
import subprocess
from subprocess import PIPE, STDOUT


def get_git_msg(output) -> str:
    msg = output.stdout.decode("ascii").strip()
    return msg


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
        print("\n> git cat-file -t", gitobject)
        print_git_msg(output)
    return get_git_msg(output)


def catfile_p(wt, gitobject: str, verbose=True) -> str:
    output = subprocess.run(['git', 'cat-file', '-p', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n> git cat-file -p", gitobject)
        print_git_msg(output)
    return get_git_msg(output)


def revparse(wt, gitobject: str, verbose=True) -> str:
    output = subprocess.run(['git', 'rev-parse', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n> git rev-parse", gitobject)
        print_git_msg(output)
    return get_git_msg(output)


def lstree(wt, gitobject: str, verbose=True) -> str:
    output = subprocess.run(['git', 'ls-tree', gitobject], cwd=wt, stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n> git ls-tree", gitobject)
        print_git_msg(output)
    return get_git_msg(output)

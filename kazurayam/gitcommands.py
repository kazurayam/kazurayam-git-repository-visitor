import os
import subprocess
from subprocess import PIPE, STDOUT


def get_git_msg(output) -> str:
    msg = output.stdout.decode("ascii").strip()
    return msg


def print_git_msg(output):
    print("{}".format(get_git_msg(output)))


def init(wt: str, verbose=False) -> str:
    os.chdir(wt)
    output = subprocess.run('git init'.split(), stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git init")
        print_git_msg(output)
    return get_git_msg(output)


def add(wt, path, verbose=False) -> str:
    os.chdir(wt)
    output = subprocess.run(['git', 'add', path], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git add", path)
        print_git_msg(output)
    return get_git_msg(output)


def status(wt, verbose=True) -> str:
    os.chdir(wt)
    output = subprocess.run(['git', 'status'], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git status")
        print_git_msg(output)
    return get_git_msg(output)


def commit(wt, msg, verbose=False):
    os.chdir(wt)
    output = subprocess.run(['git', 'commit', '-m', msg], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n% git commit -m \"{}\"".format(msg))
        print_git_msg(output)
    return get_git_msg(output)


def catfile_t(wt, object: str, verbose=True) -> str:
    os.chdir(wt)
    output = subprocess.run(['git', 'cat-file', '-t', object], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n> git cat-file -t", object)
        print_git_msg(output)
    return get_git_msg(output)


def catfile_p(wt, object: str, verbose=True) -> str:
    os.chdir(wt)
    output = subprocess.run(['git', 'cat-file', '-p', object], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n> git cat-file -p", object)
        print_git_msg(output)
    return get_git_msg(output)


def revparse(wt, object: str, verbose=True) -> str:
    os.chdir(wt)
    output = subprocess.run(['git', 'rev-parse', object], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n> git rev-parse", object)
        print_git_msg(output)
    return get_git_msg(output)


def lstree(wt, object: str, verbose=True) -> str:
    os.chdir(wt)
    output = subprocess.run(['git', 'ls-tree', object], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("\n> git ls-tree", object)
        print_git_msg(output)
    return get_git_msg(output)

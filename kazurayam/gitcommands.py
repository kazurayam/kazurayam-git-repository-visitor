import os
import subprocess
from subprocess import PIPE, STDOUT


def get_git_msg(output) -> str:
    msg = output.stdout.decode("ascii").strip()
    return msg


def print_git_msg(output):
    print("{}".format(get_git_msg(output)))


def init(wt: str, path: str, verbose=False):
    output = subprocess.run('git init'.split(), stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("> git init")
        print_git_msg(output)


def add(wt, path, verbose=False):
    output = subprocess.run(['git', 'add', path], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("> git add", path)
        print_git_msg(output)


def commit(wt, msg, verbose=False):
    output = subprocess.run(['git', 'commit', '-m', msg], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print("> git commit -m \"{}\"".format(msg))
        print_git_msg(output)

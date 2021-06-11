import subprocess
from subprocess import PIPE, STDOUT


def get_msg(completed_process) -> str:
    try:
        msg = completed_process.stdout.decode("ascii").strip()
        return msg
    except UnicodeDecodeError:
        return "!!!! stdout is a binary sequence !!!!"


def print_msg(completed_process):
    print("{}".format(get_msg(completed_process)))


def shellcommand(wt: str, args: list, verbose=True) -> tuple:
    """
    execute a anonymous shell command in Python subprocess.
    :param wt:
    :param args:
    :param verbose:
    :return: a tuple of (stdout, return_code)
    """
    completed_process = subprocess.run(args,
                                       cwd=wt, stdout=PIPE, stderr=STDOUT,
                                       check=False)
    if verbose:
        print("\n% " + ' '.join(
            ["'{}'".format(str(e)) if ' ' in str(e) else str(e) for e in args]))
        print_msg(completed_process)
    return get_msg(completed_process), completed_process.returncode

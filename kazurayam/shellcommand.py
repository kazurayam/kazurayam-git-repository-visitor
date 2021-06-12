import subprocess
from subprocess import PIPE, STDOUT


def shell_command(wt: str, args: list, verbose=False) -> tuple:
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
        echo_args(args)
        print_msg(completed_process)
    return decode_completed_process(completed_process)


def echo_args(args: list):
    print("\n% " + ' '.join(["'{}'".format(str(e)) if ' ' in str(e) else str(e) for e in args]))


def decode_stdout(completed_process) -> str:
    try:
        msg = completed_process.stdout.decode("utf-8").strip()
        return msg
    except UnicodeDecodeError:
        return "!!!! stdout is a binary sequence !!!!"


def print_msg(completed_process):
    print("{}".format(decode_stdout(completed_process)))


def decode_completed_process(completed_process):
    """
    modify subprocess.CompletedProcess object slightly:
    decode the stdout
    :param completed_process:
    :return:
    """
    completed_process.stdout = decode_stdout(completed_process)
    return completed_process

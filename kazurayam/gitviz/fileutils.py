import os
import pathlib
import shutil


def init_dir(path: str):
    """
    create a directory as path if not present.
    if the directory exists already, delete it recursively and recreate it.
    you will have an empty directory

    :param path:
    :return:
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def write_file(wt: str, path: str, text: str):
    """
    write the text into a file as path.
    if the path contains sub-directories which don't yet exist,
    then will make them

    :param wt:
    :param path:
    :param text:
    :return:
    """
    f = pathlib.Path(os.path.join(wt, path))
    os.makedirs(f.parent, exist_ok=True)
    with open(os.path.join(wt, path), 'w') as file:
        file.write(text)
    return f

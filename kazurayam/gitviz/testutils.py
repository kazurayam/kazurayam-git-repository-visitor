import os
from kazurayam.gitviz import fileutils


def create_subject_dir(basedir, subject_dir_name):
    subject_dir = os.path.join(basedir, subject_dir_name)
    fileutils.init_dir(subject_dir)
    wt = os.path.join(subject_dir, "wt")
    os.makedirs(wt)
    gr = os.path.join(subject_dir, "gr")
    os.makedirs(gr)
    return wt, gr

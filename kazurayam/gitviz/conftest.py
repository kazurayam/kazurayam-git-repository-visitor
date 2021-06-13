import os
import pytest
from kazurayam.gitviz import fileutils


@pytest.fixture(scope='session')
def basedir():
    project_dir = os.getcwd()
    base = os.path.join(project_dir, "./build")
    fileutils.init_dir(base)
    yield base


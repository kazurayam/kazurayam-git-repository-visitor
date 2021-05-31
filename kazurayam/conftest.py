import os
import pytest
from . import fileutils


@pytest.fixture(scope='session')
def basedir():
    project_dir = os.getcwd()
    base = os.path.join(project_dir, "./tmp")
    fileutils.init_dir(base)
    yield base
    os.chdir(project_dir)

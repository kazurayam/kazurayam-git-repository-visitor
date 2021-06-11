import pytest
import re
from . import fileutils
from . import shellcommand as SH
from . import testutils


@pytest.fixture(scope="module")
def wt_with_data(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'shellcommand_test')
    fileutils.write_file(wt, '.gitignore', '*~\n')
    fileutils.write_file(wt, "README.md", "# Read me please\n")
    fileutils.write_file(wt, "src/greeting.pl", "print(\"How do you do?\");\n")
    yield wt

def test_shellcommand_echo(wt_with_data):
    t = SH.shellcommand(wt_with_data, ['echo', 'Hello, world!'])
    assert t[0] == 'Hello, world!'
    assert t[1] == 0

def test_shellcommand_tree(wt_with_data):
    t = SH.shellcommand(wt_with_data, ['tree', '-afni'])
    assert len(t[0].splitlines()) >= 3
    assert '.gitignore' in t[0]
    assert 'README.md' in t[0]
    assert 'src' in t[0]
    assert 'greeting.pl' in t[0]
    assert t[1] == 0

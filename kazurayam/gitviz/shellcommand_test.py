import pytest
from kazurayam.gitviz import fileutils, shellcommand as SH, testutils


@pytest.fixture(scope="module")
def wt_with_data(basedir):
    (wt, gr) = testutils.create_subject_dir(basedir, 'shellcommand_test')
    fileutils.write_file(wt, '.gitignore', '*~\n')
    fileutils.write_file(wt, "README.md", "# Read me please\n")
    fileutils.write_file(wt, "src/greeting.pl", "print(\"How do you do?\");\n")
    yield wt


def test_echo(wt_with_data):
    # cp : Completed Process, decoded
    cp = SH.shell_command(wt_with_data, ['echo', 'Hello, world!'])
    assert cp.stdout == 'Hello, world!'
    assert cp.returncode == 0


def test_tree(wt_with_data):
    cp = SH.shell_command(wt_with_data, ['tree', '-afni'])
    assert len(cp.stdout.splitlines()) >= 3
    assert '.gitignore' in cp.stdout
    assert 'README.md' in cp.stdout
    assert 'src' in cp.stdout
    assert 'greeting.pl' in cp.stdout
    assert cp.returncode == 0

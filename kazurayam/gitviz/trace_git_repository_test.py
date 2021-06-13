import os
from kazurayam.gitviz import gitcommands as GIT, trace_git_repository, fileutils


def test_trace(basedir):
    wt = os.path.join(basedir, 'test_trace')
    fileutils.init_dir(wt)
    #
    GIT.init(wt, True)
    #
    fileutils.write_file(wt, '.gitignore', '*~\n')
    fileutils.write_file(wt, "README.md", "# Read me please\n")
    fileutils.write_file(wt, "src/greeting", "How do you do?\n")
    fileutils.write_file(wt, "src/hello.pl", "print(\"Hello, world!\")\n")
    #
    GIT.add(wt, '.', True)
    GIT.status(wt, verbose=True)
    GIT.lsfiles_stage(wt, verbose=True)
    GIT.commit(wt, "initial commit", True)
    trace_git_repository.trace(wt)
    GIT.lsfiles_stage(wt, verbose=True)
    #
    f = fileutils.write_file(wt, "src/good-luck.pl", "print('Good Luck!')\n")
    print("\n", "-" * 72)
    print("% added src/good-luck.pl")
    GIT.add(wt, '.', True)
    GIT.status(wt, verbose=True)
    GIT.lsfiles_stage(wt, verbose=True)
    GIT.commit(wt, "added src/good-luck.pl", True)
    trace_git_repository.trace(wt)
    GIT.lsfiles_stage(wt, verbose=True)

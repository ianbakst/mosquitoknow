import sys
from pathlib import Path
from invoke import task


def _find_packages(path: Path):
    for pkg in path.iterdir():
        if pkg.is_dir() and len(list(pkg.glob("**/*.py"))) >= 1:
            yield pkg


def _find_scripts(path: Path):
    return path.glob("**/*.py")


@task
def lint(c):
    c.run("flake8 .", echo=True, pty=True)


@task
def format(c, fix=False, diff=False):
    # check precondition
    if fix and diff:
        print("Please use only --diff OR --fix, but not both, when calling format.")
        sys.exit(1)

    if fix:
        arg = ""
    elif diff:
        arg = "--diff"
    else:
        arg = "--check"

    c.run(f"black {arg} . --line-length=99", echo=True, pty=True)


@task
def test(c):
    c.run("pytest", echo=True, pty=True)

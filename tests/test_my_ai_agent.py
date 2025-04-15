import os
import subprocess
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def cd(p: Path):
    now = Path.cwd()
    try:
        os.chdir(str(p))
        yield
    finally:
        os.chdir(str(now))


def run(cmd: str | list[str], dir: Path, *args, **kwargs) -> subprocess.CompletedProcess:
    with cd(dir):
        return subprocess.run(cmd, check=True, *args, **kwargs)


def test_e2e():
    pwd = Path.cwd()
    run(["pipenv", "run", "dist"], pwd)
    run(
        [
            "pip",
            "install",
            "dist/my_ai_agent-0.4.0.tar.gz",
        ],
        pwd,
    )
    run(
        ["python", "-m", "my_ai_agent.cli", "--help"],
        pwd,
        text=True,
        capture_output=True,
    )

import subprocess
import os

repos = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "repos"))


def git_clone(repo):
    cmd = ["git", "clone", "--depth", "1", None, None]
    cmd[4] = repo
    basename = os.path.basename(cmd[4])
    name, _ = os.path.splitext(basename)
    cmd[5] = os.path.join(repos, name)
    subprocess.call(cmd)
    return name


if __name__ == "__main__":
    repo.git_clone(sys.argv[1])

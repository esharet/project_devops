import argparse
import os
import git
from prettytable import PrettyTable


def find_all_repos_in_directory(dir: str):
    """
    find all repositories inside a directory
    """
    repos = []
    dirs = os.listdir(args.base_dir)
    for path in [os.path.join(args.base_dir, d) for d in dirs]:
        try:
            repos.append(git.Repo(path))
        except git.InvalidGitRepositoryError:
            pass

    return repos


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("base_dir")
    args = p.parse_args()

    print(find_all_repos_in_directory(args.base_dir))


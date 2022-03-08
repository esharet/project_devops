import logging
import argparse
import os
from sys import exc_info
import git
from prettytable import PrettyTable

log = logging.getLogger()
logging.basicConfig(level=logging.INFO)

def find_all_repos_in_directory(dir: str) -> list[git.Repo]:
    """
    find all repositories inside a directory
    """
    repos = []
    dirs = os.listdir(dir)
    for path in [os.path.join(dir, d) for d in dirs]:
        try:
            repos.append(git.Repo(path))
        except git.InvalidGitRepositoryError:
            pass

    return repos


def checkout_repos_to_new_branch(repos: list[git.Repo], branch_name: str, *, create_new_branch: bool = False) -> bool:
    """
    checkout all repos to a given branch name, and report the success of the operation
    """
    for repo in repos:
        try:
            if create_new_branch:
                repo.git.checkout('-b', branch_name)
            else:
                repo.git.checkout(branch_name)
        except git.GitCommandError:
            log.error(
                f"git checkout failed for repo {repo.working_tree_dir}, to branch '{branch_name}'", exc_info=True)
            return False
        return True


def get_submodules(repo: git.Repo):
    return(repo.submodules)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("base_dir")
    args = p.parse_args()

    repos = find_all_repos_in_directory(args.base_dir)
    print(f"all repos: {repos}")
    print("-------")
    for repo in repos:
        print(f"for repo {repo.working_tree_dir} : ")
        print(repo.submodules)
        print("-----")

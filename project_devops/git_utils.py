import logging
import argparse
import os
import git

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

def are_all_repos_clean(repos: list[git.Repo]): 
    return [False] * len(repos) == [repo.is_dirty() for repo in repos]

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


def push_all_repos_branch(repos: list[git.Repo], branch_name: str, *, create_upstream_with_this_branch_name: bool = False) -> bool:
    for repo in repos:
        assert repo.remotes.origin.exists()
        repo.git.checkout(branch_name)
        try:
            if create_upstream_with_this_branch_name:
                repo.git.push('--set-upstream', 'origin', repo.active_branch)
            else:
                repo.remotes.origin.push().raise_if_error()
        except git.GitCommandError:
            log.error(
                f"git push failed for repo {repo.working_tree_dir}, to branch '{branch_name}'", exc_info=True)
            return False
    return True


def tag_all_repos_branch(repos: list[git.Repo], branch_name: str, *, tag_name: str, commit_msg: str, push_to_remote: bool = False) -> bool:
    for repo in repos:
        repo.git.checkout(branch_name)
        try:
            repo.create_tag(tag_name, ref=repo.active_branch,
                            message=commit_msg)
            if push_to_remote: 
                repo.remotes.origin.push(tag_name)
        except git.GitCommandError:
            log.error(
                f"git tag failed for repo {repo.working_tree_dir}, to branch '{branch_name}'", exc_info=True)
            return False
    return True


if __name__ == "__main__":
    # p = argparse.ArgumentParser()
    # p.add_argument("base_dir")
    # args = p.parse_args()

    # repos = find_all_repos_in_directory(args.base_dir)
    # print(f"all repos: {repos}")
    # print("-------")
    # for repo in repos:
    #     print(f"for repo {repo.working_tree_dir} : ")
    #     print(repo.submodules)
    #     print("-----")
    # -------------------------------

    # test_git_workdir = "/home/user/projects/project_devops/test/test_repos_folder/gitpython_test_repo"
    # repo = git.Repo(test_git_workdir)
    # head = repo.active_branch
    # print(head, type(head))
    # ------------------------

    test_git_workdir = "/home/user/projects/project_devops/test/test_repos_folder/gitpython_test_repo"
    repo = git.Repo(test_git_workdir)
    # tag_all_repos_branch([repo], "dev", tag_name="v0.0.3",# 
    #                      commit_msg="only tagging test", push_to_remote=True)
    print(are_all_repos_clean([repo]))

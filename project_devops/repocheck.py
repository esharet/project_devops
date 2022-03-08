import argparse
import os
import git
from prettytable import PrettyTable

if __name__ == "__main__":
	p = argparse.ArgumentParser()
	p.add_argument("base_dir")
	args = p.parse_args()

	repos = []
	dirs = os.listdir(args.base_dir)
	for path in [os.path.join(args.base_dir, d) for d in dirs]:
		print("Loading repo %s" % path)
		try:
			repos.append(git.Repo(path))
		except git.InvalidGitRepositoryError:
			pass

	x = PrettyTable(("Path", "Clean"))
	x.align["Path"] = "l"
	clean = []
	dirty = []
	error = []
	for repo in repos:
		print("Checking repo %s" % repo.working_tree_dir)
		try:
			if repo.is_dirty():
				dirty.append(repo)
			else:
				clean.append(repo)
		except git.errors.GitCommandError:
			error.append(repo)

	for repo in sorted(error, key=lambda x: x.working_tree_dir):
		x.add_row((repo.working_tree_dir, "Error!"))
	for repo in sorted(dirty, key=lambda x: x.working_tree_dir):
		x.add_row((repo.working_tree_dir, "Dirty"))
	for repo in sorted(clean, key=lambda x: x.working_tree_dir):
		x.add_row((repo.working_tree_dir, "Clean"))

	print(x)
	print ("%d errored, %d dirty, %d clean, %d total" % (
		len(error),
		len(dirty),
		len(clean),
		len(repos)
	))

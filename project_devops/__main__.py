import sys
import argparse
from hashlib import new
import json
import os 
import project_devops.git_utils as git_utils

config_file_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'git_command_config.json')
with open(config_file_full_path) as config_file:
    projects_config = json.load(config_file)

def update_config_file(new_config: dict): 
    with open(config_file_full_path, 'w') as write_config_file: 
        json.dump(new_config, write_config_file, indent=4)

def do_you_wish_to_continue(repos):
    if not git_utils.are_all_repos_clean(repos):
        not_continue_flag = True
        while(not_continue_flag):
            to_continue = input("not all repos are clean. do you wish to continue? [y/n]")
            if to_continue == 'n':
                sys.exit(0)
            elif to_continue == 'y': 
                not_continue_flag = False
    
parser = argparse.ArgumentParser()
# available actions
git_action = parser.add_mutually_exclusive_group()
git_action.add_argument('--checkout', action='store_true', help="checkout all repos to a given branch")
git_action.add_argument('--push', action='store_true', help="push all repos of a given branch")
git_action.add_argument('--tag', action='store_true', help="tag all repos in a given branch")
git_action.add_argument('--update-repos-location', type=str, help="update repos location in config file")

# arguments
parser.add_argument('-f', '--force', action='store_true', help="force an action - create branch / create remote branch with the same name")
parser.add_argument('-b', '--branch', type=str, help="branch name")
parser.add_argument('-t', '--tag_name', type=str, help="tag name if using tag")
parser.add_argument('-m', '--commit_msg', type=str, help="commit message")
parser.add_argument('-v', '--verbose', action='store_true', help="verbose")

def main(): 
    args = parser.parse_args()
    if args.verbose: 
        print(args)
    if args.update_repos_location: 
        projects_config["git_repos_location"] = args.update_repos_location
        update_config_file(projects_config)
        sys.exit(0)
    
    repos = git_utils.find_all_repos_in_directory(projects_config["git_repos_location"])
    do_you_wish_to_continue(repos)
    if args.checkout: 
        git_utils.checkout_repos_to_new_branch(repos, args.branch, create_new_branch=args.force)
    elif args.push: 
        git_utils.push_all_repos_branch(repos, args.branch, create_upstream_with_this_branch_name=args.force)
    elif args.tag: 
        git_utils.tag_all_repos_branch(repos, args.branch, tag_name=args.tag_name, commit_msg=args.commit_msg, push_to_remote=True)

    
if __name__ == "__main__": 
    sys.exit(main())

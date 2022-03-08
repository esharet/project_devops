import unittest
import git
import os
import project_devops.general_utils as git_utils

class GeneralUtilsTest(unittest.TestCase): 

    def setUp(self) -> None:
        self.base_dir = "/home/user/projects/project_devops/test/test_repos_folder"
        self.repos_working_dirs = [os.path.join(self.base_dir, d) for d in os.listdir(self.base_dir)]
    
    def test_find_all_git_repos(self,): 
        repos_found = git_utils.find_all_repos_in_directory(self.base_dir)
        repos_directories = [repo.working_tree_dir for repo in repos_found]
        self.assertEqual(repos_directories, self.repos_working_dirs, "repos found isn't correct")
    
    def test_failure_checkout_branch(self,): 
        test_repo = git.Repo(os.path.join(self.base_dir, "gitpython_test_repo"))
        checkout_success = git_utils.checkout_repos_to_new_branch([test_repo], "dev", create_new_branch=True) 
        self.assertFalse(checkout_success, "checkout to existing branch didn't failed! (although dev branch should exist) ")

    def test_checkout_branch(self,): 
        test_repo = git.Repo(os.path.join(self.base_dir, "gitpython_test_repo"))
        checkout_success = git_utils.checkout_repos_to_new_branch([test_repo], "dev") 
        self.assertTrue(checkout_success, "checkout to branch failed ! ")

    def test_push_branch(self,): 
        test_repo = git.Repo(os.path.join(self.base_dir, "gitpython_test_repo"))
        checkout_success = git_utils.push_all_repos_branch([test_repo], "dev", create_upstream_with_this_branch_name=True) 
        self.assertTrue(checkout_success, "pushing branch failed ! ")
    

if __name__ == '__main__':
    unittest.main()

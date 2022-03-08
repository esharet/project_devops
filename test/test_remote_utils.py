import unittest
import git
import os
import project_devops.git_utils as git_utils

class GeneralUtilsTest(unittest.TestCase): 

    def setUp(self) -> None:
        self.base_dir = "/home/user/projects/project_devops/test/test_repos_folder"
        self.repos_working_dirs = [os.path.join(self.base_dir, d) for d in os.listdir(self.base_dir)]
    
    def test_push_branch(self,): 
        test_repo = git.Repo(os.path.join(self.base_dir, "gitpython_test_repo"))
        checkout_success = git_utils.push_all_repos_branch([test_repo], "dev", create_upstream_with_this_branch_name=True) 
        self.assertTrue(checkout_success, "pushing branch failed ! ")


if __name__ == '__main__':
    unittest.main()
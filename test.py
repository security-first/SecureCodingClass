#!/usr/bin/python

# This is the test class for running unit tests on all coded methods/functions
# All tests can be run quickly and automatically (from the root, project folder) with:
#    python -m unittest test

import unittest
import sys
sys.path.insert(0,'./lib')
import commands, directories

class Test(unittest.TestCase):
    def setUp(self):
        self.root_folder = directories.Directory('/', None, [])
        root_home = self.root_folder.add('root')
        var = self.root_folder.add('var')
        var_log = var.add('log')
        root_home.add('Documents')

        self.tree = commands.DirectoryTree(self.root_folder)
        pass

    def test_command_ls(self):
        self.assertEqual(self.tree.ls(), ['root', 'var'])


if __name__ == '__main__':
    unittest.main()

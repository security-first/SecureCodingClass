#!/usr/bin/python

# This is the test class for running unit tests on all coded methods/functions
# All tests can be run quickly and automatically (from the root, project folder) with:
#    python -m unittest test

import unittest
import sys
sys.path.insert(0,'./lib')
import commands, directories

class TestPhase0(unittest.TestCase):
    def setUp(self):
        self.root_folder = directories.Directory('/', None, [])
        root_home = self.root_folder.add('root')
        var = self.root_folder.add('var')
        var_log = var.add('log')
        root_home.add('Documents')

        self.tree = commands.DirectoryTree(self.root_folder)

    def test_command_ls(self):
        self.assertEqual(self.tree.ls(), ['root', 'var'])

    def test_command_cd_once_through_root(self):
        self.tree.cd('root')
        self.assertEqual(self.tree.ls(), ['Documents'])

    def test_command_cd_twice_through_root(self):
        self.tree.cd('root')
        self.tree.cd('Documents')
        self.assertEqual(self.tree.ls(), [])

    def test_command_cd_once_through_var(self):
        self.tree.cd('var')
        self.assertEqual(self.tree.ls(), ['log'])

    def test_command_cd_twice_through_var(self):
        self.tree.cd('var')
        self.tree.cd('log')
        self.assertEqual(self.tree.ls(), [])

    def test_command_cd_down_and_back_once(self):
        self.tree.cd('root')
        self.tree.cd('..')
        self.tree.cd('var')
        self.tree.cd('..')

        self.assertEqual(self.tree.ls(), ['root', 'var'])

    def test_command_cd_down_and_back_twice(self):
        self.tree.cd('root')
        self.tree.cd('Documents')
        self.tree.cd('..')
        self.tree.cd('..')
        self.tree.cd('var')
        self.tree.cd('log')
        self.tree.cd('..')
        self.tree.cd('..')

        self.assertEqual(self.tree.ls(), ['root', 'var'])

    def test_command_cd_full_filepath(self):
        self.assertEqual(self.tree.ls(), ['root', 'var'])
        self.tree.cd('root/Documents')
        self.assertEqual(self.tree.ls(), [])
        self.tree.cd('../..')
        self.assertEqual(self.tree.ls(), ['root', 'var'])
        self.tree.cd('var/log')
        self.assertEqual(self.tree.ls(), [])

if __name__ == '__main__':
    unittest.main()

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

    def test_command_cd_nonexistent_directory(self):
        self.assertEqual(self.tree.ls(), ['root', 'var'])
        self.assertEqual(self.tree.cd('doesnotexist'), '-bash: cd: doesnotexist: No such file or directory')

class TestPhase1(unittest.TestCase):
    def setUp(self):
        self.root_folder = directories.Directory('/', None, [])
        root_home = self.root_folder.add('root')
        self.root_folder.add('home')
        var = self.root_folder.add('var')
        var_log = var.add('log')
        var_log.add_file('access.log', '''

    2016-04-03 14:13:34 [AUTHENTICATION] John Smith successfully logged in using the password "P@ssword!"
    2016-04-03 15:16:12 [AUTHENTICATION] Mary Adams failed to log in using the password "securityR0cks!"
    2016-04-03 15:16:34 [AUTHENTICATION] Mary Adams successfully logged in using the password "SecurityR0cks!"
    2016-04-03 16:02:56 [AUTHENTICATION] Matthew Jones failed to log in using the password "B@ltim0re!"
    2016-04-03 16:03:16 [AUTHENTICATION] Matthew Jones failed to log in using the password "Baltim0re!"
    2016-04-03 16:03:45 [AUTHENTICATION] Matthew Jones failed to log in using the password "b@ltlm0re!"
    2016-04-03 16:03:46 [AUTHENTICATION] Matthew Jones's account has been locked out -- 3 unsuccessful attempts

        ''', ['root'])
        root_home.add('Documents')

        self.tree = commands.DirectoryTree(self.root_folder)

    def test_command_cat_file_exists(self):
        self.tree.cd('var/log')
        self.assertEqual(self.tree.cat('access.log', 'root'), '''

    2016-04-03 14:13:34 [AUTHENTICATION] John Smith successfully logged in using the password "P@ssword!"
    2016-04-03 15:16:12 [AUTHENTICATION] Mary Adams failed to log in using the password "securityR0cks!"
    2016-04-03 15:16:34 [AUTHENTICATION] Mary Adams successfully logged in using the password "SecurityR0cks!"
    2016-04-03 16:02:56 [AUTHENTICATION] Matthew Jones failed to log in using the password "B@ltim0re!"
    2016-04-03 16:03:16 [AUTHENTICATION] Matthew Jones failed to log in using the password "Baltim0re!"
    2016-04-03 16:03:45 [AUTHENTICATION] Matthew Jones failed to log in using the password "b@ltlm0re!"
    2016-04-03 16:03:46 [AUTHENTICATION] Matthew Jones's account has been locked out -- 3 unsuccessful attempts

        ''')

    def test_command_cat_file_does_not_exist(self):
        self.assertEqual(self.tree.cat('access.log', 'root'), '-bash: cd: access.log: No such file or directory')
        self.tree.cd('var')
        self.assertEqual(self.tree.cat('access.log', 'root'), '-bash: cd: access.log: No such file or directory')
        self.tree.cd('log')
        self.assertEqual(self.tree.cat('doesnotexist.log', 'root'), '-bash: cd: doesnotexist.log: No such file or directory')

    def test_command_cat_permission_fail(self):
        self.tree.cd('var/log')
        self.assertEqual(self.tree.cat('access.log', 'user'), 'cat: access.log: Permission denied')

    def test_command_adduser_root_user(self):
        self.assertEqual(self.tree.adduser('root', 'user1'), [True, '''
Adding user '{0}' ...
Adding new group '{0}' (1001) ...
Adding new user '{0}' (1001) with group '{0}' ...
Creating home directory '/home/{0}' ...
Copying files from '/etc/skel' ...
passwd: password updated successfully
Changing the user information for {0}
            '''.format('user1')])
        self.assertEqual(self.tree.adduser('root', 'user2'), [True, '''
Adding user '{0}' ...
Adding new group '{0}' (1001) ...
Adding new user '{0}' (1001) with group '{0}' ...
Creating home directory '/home/{0}' ...
Copying files from '/etc/skel' ...
passwd: password updated successfully
Changing the user information for {0}
            '''.format('user2')])

    def test_command_adduser_not_root_user(self):
        self.assertEqual(self.tree.adduser('user1', 'user2'), [False, '-bash: adduser user2: Permission denied'])
        self.assertEqual(self.tree.adduser('user1', 'root'), [False, '-bash: adduser root: Permission denied'])
        self.assertEqual(self.tree.adduser('', 'user2'), [False, '-bash: adduser user2: Permission denied'])
        self.assertEqual(self.tree.adduser('user1', ''), [False, '-bash: adduser : Permission denied'])

class TestPhase2(unittest.TestCase):
    def setUp(self):
        self.root_folder = directories.Directory('/', None, [])
        self.root_folder.add('root')
        home = self.root_folder.add('home')
        home.add('user').add_file('text.txt', 'ababa', ['root'])
        var = self.root_folder.add('var')
        var.add('mail')
        var.add('lib')
        var.add('backups')
        var_log = var.add('log')
        usr = self.root_folder.add('usr')
        usr.add_file('.secrets.txt', '1000101\n'*750 + 'password=securityisfun\n' + '10011101\n'*1500, ['all'])
        usr.add('bin')
        usr.add('lib')
        usr.add('sbin')

        self.tree = commands.DirectoryTree(self.root_folder, current=self.root_folder.find_by_name('user'))

    def test_initial_folder(self):
        self.assertEqual(self.tree.current.name, 'user')

    def test_command_ls_hidden_files(self):
        self.tree.cd('../../usr')
        self.assertEqual(self.tree.current.name, 'usr')
        self.assertEqual(self.tree.ls(), ['bin', 'lib', 'sbin'])
        self.assertEqual(self.tree.ls(hidden=True), ['.secrets.txt', 'bin', 'lib', 'sbin'])

    def test_command_grep_correct_usage(self):
        self.tree.cd('../../usr')
        self.assertEqual(self.tree.grep('password', '.secrets.txt', 'user'), 'password=securityisfun')

    def test_command_grep_incorrect_usage(self):
        self.assertEqual(self.tree.grep('password', '.secrets.txt', 'user'), 'grep: .secrets.txt: No such file or directory')
        self.tree.cd('..')
        self.assertEqual(self.tree.grep('password', 'user', 'user'), 'grep: user: Is a directory')
        self.tree.cd('user')
        self.assertEqual(self.tree.grep('aba', 'text.txt', 'user'), 'grep: text.txt: Permission denied')


if __name__ == '__main__':
    unittest.main()

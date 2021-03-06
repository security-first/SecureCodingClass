from directories import *

class DirectoryTree():
    def __init__(self, directory, current=None):
        if current:
            self.current = current
        else:
            self.current = directory
        self.root = directory

    def current_path(self):
        path = [self.current.name]
        temp = self.current
        while temp.parent and not temp.parent.name == '/':
            temp = temp.parent
            path.insert(0, temp.name)
        return '/'.join(path)

    # Kind of emulates the basic "mkdir" linux command (Needs more work)
    def mkdir(self, new_dir, parent='.'):
        if '/' in new_dir:
            # needs implementing
            return None
        else:
            if parent == '.':
                self.current.add(new_dir)
            else:
                p = self.root.find_by_name(parent)
                if p:
                    p.add(new_dir)
                else:
                    return None

    # Emulates the basic "ls" linux command (without flags)
    # Input: None
    # Output: Returns all of the children names of the current directory
    def ls(self, hidden=False):
        if hidden:
            return [x.name for x in self.current.children]
        else:
            return [x.name for x in self.current.children if not x.name.startswith('.')]

    # Emulates the basic "cd" linux command
    # Input: target directory
    # Output: If error, outputs error message. Else, outputs None
    def cd(self, target):
        # print '[*] Attempting to change from %s to %s' % (self.current.name, target)
        if '/' in target:
            temp = self.current
            for dir in target.split('/'):
                if dir == '.':
                    continue
                elif dir == '..':
                    if temp.parent:
                        temp = temp.parent
                    else:
                        continue
                else:
                    if dir and dir in temp.getChildren():
                        for child in temp.children:
                            if child.name == dir and isinstance(child, Directory):
                                temp = child
                            elif child.name == dir:
                                return '-bash: cd: %s: Not a directory' % dir
                    elif dir:
                        return '-bash: cd: %s: No such file or directory' % target
            self.current = temp
            return None # No errors
        elif target == '.': # current directory
            return None
        elif target == '..': # parent directory
            if self.current.parent:
                self.current = self.current.parent
            return None
        else:
            if target in self.current.getChildren():
                found = False
                for child in self.current.children:
                    if child.name == target and isinstance(child, Directory):
                        self.current = child
                        found = True
                    elif child.name == target:
                        return '-bash: cd: %s: Not a directory' % target
                if not found:
                    return '-bash: cd: %s: No such file or directory' % target
                else:
                    return None # No errors
            else:
                return '-bash: cd: %s: No such file or directory' % target

    # Emulates the linux "cat" command (wrt reading text files, no concatenation yet)
    # Input: Target file, username
    # Output: The contents of that file, if it exists, or the error message if it does not
    def cat(self, filename, user):
        if filename in self.current.getChildren(): # has to be in current directory
            for file in self.current.children:
                if file.name == filename and isinstance(file, File) and ('all' in file.viewable_by_user or user in file.viewable_by_user):
                    return file.contents
                elif file.name == filename and isinstance(file, File):
                    return 'cat: %s: Permission denied' % filename
                else:
                    continue
        elif filename in self.current.getChildren():
            return 'cat: %s: Is a directory' % filename
        else:
            return '-bash: cd: %s: No such file or directory' % filename

    # Emulates the "adduser" linux command (took some shortcuts though - results are mostly static)
    # Input: Current user; username to add
    # Output: New user setup messages; Error message if not
    def adduser(self, current_user, new_user):
        if not current_user == 'root':
            return [False, '-bash: adduser %s: Permission denied' % new_user] # unsuccessful
        else:
            return [True, '''
Adding user '{0}' ...
Adding new group '{0}' (1001) ...
Adding new user '{0}' (1001) with group '{0}' ...
Creating home directory '/home/{0}' ...
Copying files from '/etc/skel' ...
passwd: password updated successfully
Changing the user information for {0}
            '''.format(new_user)]

    # Emulates the "grep" linux command
    # Input: Pattern; filename
    # Output: Typical grep output, or error message
    def grep(self, pattern, filename, username):
        if filename in self.current.getChildren():
            for file in self.current.children:
                if file.name == filename and isinstance(file, File) and ('all' in file.viewable_by_user or username in file.viewable_by_user):
                    results = []
                    for line in file.contents.split('\n'):
                        if pattern in line:
                            results.append(line)
                    return '\n'.join(results)
                elif file.name == filename and isinstance(file, File):
                    return 'grep: %s: Permission denied' % filename
                elif file.name == filename:
                    return 'grep: %s: Is a directory' % filename
                else:
                    continue
        else:
            return 'grep: %s: No such file or directory' % filename
